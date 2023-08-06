import sys
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.ops import cascaded_union

sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from env.env_base import EnvBase
from sut.idm import IDM
from sut.curve_pursuit import CP

class LaneChange(EnvBase):

    def __init__(self,sut=None,a_bound=5):
        self.scenario_shape = 8
        self.car_length = 4.924
        self.car_width = 1.872
        self.l = 3  # 车辆轴距，单位：m
        self.dt = 0.1
        self.background_control = IDM(a_bound=a_bound) # 背景车加速度！！
        self.metric = 'danger'
        self.curve = None
        self.curve_tag = None
        self.vehicle_array = None
        self.vehicle_list = None  # ['ego', 'f', 'r', 'rf']
        # 间隙选择模型参数
        self.x_front_param = np.array([1, 0.2*0.447, 0.35*0.447, 0.25*0.447])
        self.x_back_param = np.array([1.5, 0.15*0.447, 0.45*0.447, 0.3*0.447])
        self.x_front = None
        self.x_back = None
        if sut == None:
            self.sut = CP(5)
        else:
            self.sut = sut
        print(
            'laneChange场景，输入参数v1,v3,dif_v3_v4,dif_v1_v0,dif_x1_x0,dif_x3_x4,dif_x0_x4,dif_y0_y4')
        print('背景车加速度:',a_bound)
        self.count = 0

    def init(self, scenario):
        self.time_count = np.zeros([scenario.shape[0]])
        self.result = np.zeros([scenario.shape[0]])
        straight_curve = np.concatenate(
            (np.linspace(0, 200, 150).reshape(-1, 1),
             np.zeros(150).reshape(-1, 1)), axis=1)
        straight_curve = np.expand_dims(
            straight_curve, 0).repeat(scenario.shape[0], axis=0)
        self.curve = straight_curve.copy()
        self.curve_tag = np.zeros((scenario.shape[0]))
        [v1, v3, dif_v3_v4, dif_v1_v0, dif_x1_x0, dif_x3_x4, dif_x0_x4,
         dif_y0_y4] = [scenario[:, i]
                       for i in range(self.scenario_shape)]
        # 设置v
        [v1, v3] = [np.clip(v, 0, 1e5) for v in [v1, v3]]
        v4 = v3 - dif_v3_v4
        v0 = v1 - dif_v1_v0
        [v0, v4] = [np.clip(v, 0, 1e5) for v in [v0, v4]]
        # 设置x
        x0 = np.zeros((scenario.shape[0],))
        x1 = x0 + dif_x1_x0
        x4 = x0 - dif_x0_x4
        x3 = x4 + dif_x3_x4
        # 设置y
        y0, y1 = [np.zeros((scenario.shape[0],)) for i in range(2)]
        y4 = y0 - dif_y0_y4
        y3 = y4.copy()
        # 设置dir
        dir0, dir1, dir3, dir4 = [np.zeros((scenario.shape[0],)) for i in
                                  range(4)]
        # 设置length
        length0, length1, length3, length4 = [
            np.ones((scenario.shape[0],)) * self.car_length for i in range(4)]
        # 设置width
        width0, width1, width3, width4 = [
            np.ones((scenario.shape[0],)) * self.car_width for i in range(4)]

        # Encode to array, shape (0,0,6)
        self.vehicle_list = ['ego', 'f', 'r', 'rf']
        self.vehicle_array = np.zeros(
            (scenario.shape[0], len(self.vehicle_list), 6))
        item_list_0 = [x0, y0, v0, dir0, length0, width0]
        item_list_1 = [x1, y1, v1, dir1, length1, width1]
        item_list_3 = [x3, y3, v3, dir3, length3, width3]
        item_list_4 = [x4, y4, v4, dir4, length4, width4]
        for i in range(self.vehicle_array.shape[2]):
            self.vehicle_array[:, 0, i] = item_list_0[i]
            self.vehicle_array[:, 1, i] = item_list_1[i]
            self.vehicle_array[:, 2, i] = item_list_4[i]
            self.vehicle_array[:, 3, i] = item_list_3[i]

        self.x_front = np.tile(self.x_front_param, self.vehicle_array.shape[0]).reshape(self.vehicle_array.shape[0], -1)
        self.x_back = np.tile(self.x_back_param, self.vehicle_array.shape[0]).reshape(self.vehicle_array.shape[0], -1)

        self.update_curve()
        state = self.get_state('ego')
        return state

    def update(self, action):
        # 根据前向欧拉更新，根据旧速度更新位置，然后更新速度
        # x0,y0,v0,dir0,length0
        # 更新x
        a0, rot0 = action
        state_4 = self.get_state('r')
        a4, rot4 = self.background_control.deside_all(state_4)
        state_3 = self.get_state('rf')
        a3, rot3 = self.background_control.deside_all(state_3)
        state_1 = self.get_state('f')
        a1, rot1 = self.background_control.deside_all(state_1)
        for i in range(len(self.vehicle_list)):
            self.vehicle_array[:, i, 0] += self.vehicle_array[:, i,
                                           2] * self.dt * np.cos(
                self.vehicle_array[:, i, 3])
            self.vehicle_array[:, i, 1] += self.vehicle_array[:, i,
                                           2] * self.dt * np.sin(
                self.vehicle_array[:, i, 3])
        # 更新dir,v
        for i, a, rot in zip(['ego', 'r', 'rf','f'], [a0, a4, a3,a1],
                             [rot0, rot4, rot3,rot1]):
            array_sub = self.vehicle_array[:, self.vehicle_list.index(i), :]
            array_sub[:, 3] += array_sub[:, 2] / \
                               array_sub[:, 4] * np.tan(rot) * self.dt
            array_sub[:, 2] += a * self.dt
            array_sub[:, 2] = np.clip(array_sub[:, 2], 0, 1e5)
        self.update_curve()
        danger_index,done = self.judge()
        return danger_index,done

    def judge(self):
        poly_zip = [self.get_poly(param) for param in self.vehicle_list]
        intersection = []
        for polys in zip(poly_zip[0], poly_zip[1], poly_zip[2], poly_zip[3]):
            intersect = cascaded_union(
                [a.intersection(b) for a, b in combinations(polys, 2)]
            )
            intersection += [intersect.area]
        if self.metric == "danger":
            self.result[np.array(intersection) > 0] = 1
            done = np.zeros([self.result.shape[0]])
        elif self.metric == "danger_union":
            self.result = np.max(
                np.concatenate(
                    (self.result.reshape(-1, 1),
                     np.array(intersection).reshape(-1, 1)),
                    axis=1), axis=1)
            done = np.zeros([self.result.shape[0]])
        elif self.metric == 'dqn':
            done = np.zeros([self.result.shape[0]])
            state = self.get_state('ego')
            # self.time_count[state[:,0,2]<1] += 1
            # self.time_count[state[:,0,2]>5] = 0
            # done[self.time_count > 20] = 1
            done[np.array(intersection) > 0] = 1
            done[state[:,0,2]>44] = 1
            self.result = 0.01-np.abs(self.vehicle_array[:,0,2]-22)/2200
            # self.result[self.time_count > 20] = -1
            self.result[np.array(intersection) > 0] = -1
        else:
            print("metric not define!")
            
        return self.result,done

    def test(self, scenario, sut=None, metric='danger', plot_key=False, train=False):
        scenario = scenario.reshape(-1, self.scenario_shape)
        assert (scenario.shape[1] == self.scenario_shape)
        self.metric = metric
        if sut == None:
            sut = self.sut
        if plot_key:
            plt.ion()
        new_state = self.init(scenario)
        self.count += scenario.shape[0]
        reward_sum = 0
        self.have_done = np.zeros(scenario.shape[0])
        for i in range(100):
            state = new_state.copy()
            action = sut.deside_all(state, self.curve)
            reward,done = self.update(action)
            self.have_done[done==1] = 1
            reward_sum += reward[0]
            if plot_key:
                plt.cla()
                self.plot_all()
                plt.plot(self.curve[0,:,0],self.curve[0,:,1],'--',alpha=0.3)
                plt.ylim(-40, 40)
                x_center = self.vehicle_array[0,:,0].mean()
                plt.xlim(x_center-70, x_center+70)
                plt.annotate("reward:%.4f"%reward[0],xy=(x_center+30,35))
                plt.annotate("v:%.4f"%state[0,0,2],xy=(x_center+30,30))
                plt.annotate("acc:%.4f"%action[0],xy=(x_center+30,25))
                plt.annotate("reward_sum:%.4f"%(reward_sum),xy=(x_center+30,20))
                plt.annotate("reward_avg:%.4f"%(reward_sum/(i+1)),xy=(x_center+30,15))
                plt.annotate("done:%.4f"%done[0],xy=(x_center+30,10))
                plt.annotate("test_num:%d"%(self.count),xy=(x_center+30,5))
                plt.pause(1e-3)
                plt.show()
            new_state = self.get_state('ego')
            if sut.trainable and train is True:
                sut.train(state,new_state,action,reward,done)
            if self.have_done.sum() == scenario.shape[0]:
                break
        self.reward_avg = reward_sum/(i+1)
        return self.result

    def update_curve(self):
        # vehicle_list : ['ego', 'f', 'r', 'rf']
        # x0, y0, v0, dir0, length0, width0
        sample_shape = self.vehicle_array.shape[0]
        ego_x = self.vehicle_array[:, 0, 0].copy()
        tag_front = np.zeros((sample_shape,)).astype(np.int)
        tag_back = np.zeros((sample_shape,)).astype(np.int)

        tag_array = np.array([2, 3])
        dis_x_array = self.vehicle_array[:, tag_array, 0] - ego_x.reshape(-1, 1)  # shape (场景数, 车数)

        array_sub = dis_x_array.copy()
        ind = (dis_x_array > 0)
        exist = (ind.sum(axis=1) != 0)
        array_sub[ind == False] = np.nan
        key = np.nanargmin(array_sub[exist], axis=1)
        tag_front[exist] = tag_array[key]

        array_sub = dis_x_array.copy()
        ind = (dis_x_array < 0)
        exist = (ind.sum(axis=1) != 0)
        array_sub[ind == False] = np.nan
        key = np.nanargmax(array_sub[exist], axis=1)
        tag_back[exist] = tag_array[key]
        dis_front = self.vehicle_array[range(sample_shape), tag_front, 0] - ego_x - self.vehicle_array[:, 0, 4] / 2 - \
                    self.vehicle_array[range(sample_shape), tag_front, 4] / 2
        dis_back = -self.vehicle_array[range(sample_shape), tag_back, 0] + ego_x - self.vehicle_array[:, 0, 4] / 2 - \
                   self.vehicle_array[range(sample_shape), tag_back, 4] / 2
        dis_front[tag_front == 0] = 100
        dis_back[tag_back == 0] = 100
        # self.x_front, self.x_back
        beta_0 = np.ones((self.vehicle_array.shape[0], 1)) * 1
        dis_front_cap = None
        dis_back_cap = None
        for tag, minus, x, step in zip([tag_front, tag_back], [1, -1],
                                       [self.x_front, self.x_back], [1, 0]):
            delta_v = minus * (self.vehicle_array[:, 0, 2] - self.vehicle_array[range(sample_shape), tag, 2])
            beta_1 = np.clip(delta_v, 0, 1e5).reshape(-1, 1)
            beta_2 = np.clip(delta_v, -1e5, 0).reshape(-1, 1)
            beta_3 = self.vehicle_array[range(sample_shape), tag, 2].reshape(-1, 1)
            beta = np.concatenate((beta_0, beta_1, beta_2, beta_3), axis=1)
            if step:
                dis_front_cap = np.multiply(beta, x).sum(axis=1)
            else:
                dis_back_cap = np.multiply(beta, x).sum(axis=1)
        dis_front_cap[tag_front == 0] = 0
        dis_back_cap[tag_back == 0] = 0
        tag_curve = (dis_front > dis_front_cap) & (dis_back > dis_back_cap) & (self.curve_tag == 0)

        if tag_curve.sum() > 0:
            bezier = pd.DataFrame(self.vehicle_array[tag_curve, 2, 1])
            curve = np.array(list(map(self.BezierCurve, bezier[0])))
            curve = curve.reshape(tag_curve.sum(), -1, 2)
            straight_curve = np.concatenate(
                (np.linspace(0, 400, 100).reshape(-1, 1),
                 np.zeros(100).reshape(-1, 1)), axis=1)
            straight_curve = np.expand_dims(
                straight_curve, 0).repeat(curve.shape[0], axis=0)
            straight_curve += curve[:, -1,
                              :].reshape(curve.shape[0], 1, -1)
            self.curve[tag_curve, :, :] = np.concatenate((curve, straight_curve), axis=1)
            self.curve[tag_curve, :, 0] += ego_x[tag_curve].reshape(-1, 1)
            self.curve[tag_curve, :, 1] += self.vehicle_array[tag_curve, 0, 1].reshape(-1, 1)
            self.curve_tag[tag_curve] = 1
        # # 只在绘图中用到
        # self.dis_front_cap = dis_front_cap
        # self.dis_back_cap = dis_back_cap
        # self.dis_front = dis_front
        # self.dis_back = dis_back

    @staticmethod
    def BezierCurve(end_py, start_px=0, start_py=0, end_px=30, start_heading=0,
                    end_heading=0):
        """根据起终点坐标、方向角生成一段贝塞尔曲线

        :param end_py:终点y轴坐标
        :param start_px:起点x轴坐标
        :param start_py:起点y轴坐标
        :param end_px:终点x轴坐标
        :param start_heading:起点转向角
        :param end_heading:终点转向角
        :return
            curve
        """
        t = np.linspace(0, 1, num=int(50))
        x1 = start_px * 2.0 / 3 + end_px * 1.0 / 3  # vector (sample.shape,1)
        x2 = start_px * 1.0 / 3 + end_px * 2.0 / 3  # vector (sample.shape,1)
        y1 = start_py * 2.0 / 3 + end_py * 1.0 / 3  # vector (sample.shape,1)
        y2 = start_py * 1.0 / 3 + end_py * 2.0 / \
             3  # 三等分点 # vector (sample.shape,1)
        p1_x = (y1 - start_py - np.tan(start_heading + np.pi / 2) * x1 + np.tan(
            start_heading) * start_px) / \
               (np.tan(start_heading) - np.tan(start_heading +
                                               np.pi / 2))  # vector (sample.shape,1)
        p1_y = np.tan(start_heading) * (p1_x - start_px) + \
               start_py  # vector (sample.shape,1)
        p2_x = (y2 - end_py - np.tan(end_heading + np.pi / 2) * x2 + np.tan(
            end_heading) * end_px) / \
               (np.tan(end_heading) - np.tan(end_heading +
                                             np.pi / 2))  # vector (sample.shape,1)
        p2_y = np.tan(end_heading) * (p2_x - end_px) + \
               end_py  # vector (sample.shape,1)
        Bx = start_px * (1 - t) ** 3 + 3 * p1_x * t * (1 - t) ** 2 + \
             3 * p2_x * t ** 2 * (1 - t) + end_px * \
             t ** 3  # vector (sample.shape,1)
        By = start_py * (1 - t) ** 3 + 3 * p1_y * t * (1 - t) ** 2 + \
             3 * p2_y * t ** 2 * (1 - t) + end_py * \
             t ** 3  # vector (sample.shape,1)
        return np.array([Bx.tolist(), By.tolist()]).T  # 转换成list格式，轨迹离散点

class ENV(LaneChange):
    pass

if __name__ == "__main__":
    # from sut.lane_change import LC
    from sut.dqn import DQN
    print("start")
    rot_sut = CP()
    sut = DQN(trainable=False,a_bound=5,rot_sut=rot_sut,loadpath="output/dqn/lane_change.h5")
    env = ENV()
    # env.background_control = sut
    # 场景参数定义在此处
    data = pd.read_csv("data/lane_change_created.csv")
    # data = data[data.iloc[:,-1]==1]

    test_sample = np.array(data.sample(10))
    res_all = env.test(test_sample, metric="danger")
    # print(res_all,sum(res_all))
    # print(env.reward_avg)
    test_count = 0
    res_rec = []
    for scenario in test_sample:
        res = env.test(scenario, sut, plot_key=True, metric="dqn")
        print(test_count,res,scenario)
        res_rec += [res]
        test_count += 1
