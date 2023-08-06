import sys

sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from itertools import combinations
from shapely.ops import cascaded_union
from env.env_base import EnvBase
from sut.idm import IDM
from sut.curve_pursuit import CP
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings


class CutIn(EnvBase):

    def __init__(self,a_bound=5,sut=None):
        self.scenario_shape = 6
        self.background_control = CP(a_bound=a_bound)
        self.car_length = 4.924
        self.car_width = 1.872
        self.curve = None
        self.l = 3  # 车辆轴距，单位：m
        self.dt = 0.1
        self.metric = 'danger'
        print("输入场景参数: dif_v7_v0, dif_v1_v7, v1, dif_x7_x0, dif_y7_y0, dif_x1_x7")
        if sut == None:
            self.sut = IDM(5)
        else:
            self.sut = sut        
        self.count = 0

    def init(self, scenario):
        self.result = np.zeros([scenario.shape[0]])
        self.done = np.zeros([scenario.shape[0]])
        self.location_curve = np.zeros([scenario.shape[0]])
        self.y7_sum = np.zeros([scenario.shape[0]])
        [dif_v7_v0, dif_v1_v7, v1, dif_x7_x0, dif_y7_y0, dif_x1_x7] = [scenario[:, i] for i in range(
                                                                        self.scenario_shape)]
        # 初始化前车，侧向车与本车的速度
        v7 = v1 - dif_v1_v7
        v0 = v7 - dif_v7_v0
        if ((v0 <= 0) | (v1 <= 0) | (v7 <= 0)).sum() > 0:
            v1[v1 <= 0] = 0
            v7 = v1 - dif_v1_v7
            v7[v7 <= 0] = 0
            v0 = v7 - dif_v7_v0
            v0[v0 <= 0] = 0

        # 初始化本车位置
        y0 = np.zeros([scenario.shape[0]])
        x0 = np.zeros([scenario.shape[0]])

        # 初始化侧向车位置
        x7 = x0 + dif_x7_x0
        y7 = y0 + dif_y7_y0

        # 初始化前车位置
        if (dif_x1_x7 <= 0).sum() > 0:
            warnings.warn('初始时刻，侧向车在前车前面!', UserWarning)
            dif_x1_x7[dif_x1_x7 <= 0] = self.car_length
        x1 = x7 + dif_x1_x7
        y1 = np.zeros([scenario.shape[0]])
        # y1[y1<=self.car_length] = self.car_length + 3

        # 记录侧向车初始位置
        self.x7_ori = x7.copy()
        self.y7_ori = y7.copy()

        # 得到贝塞尔曲线
        bezier_7 = pd.DataFrame(-dif_y7_y0)
        curve = np.array(list(map(self.BezierCurve, bezier_7[0])))
        self.curve = curve.reshape(scenario.shape[0], -1, 2)
        self.curve[:, :, 0] += x7.reshape(-1, 1)
        self.curve[:, :, 1] += y7.reshape(-1, 1)

        straight_curve = np.concatenate(
            (np.linspace(0, 150, 100).reshape(-1, 1),
             np.zeros(100).reshape(-1, 1)), axis=1)
        straight_curve = np.expand_dims(
            straight_curve, 0).repeat(self.curve.shape[0], axis=0)
        straight_curve += self.curve[:, -1,
                          :].reshape(self.curve.shape[0], 1, -1)
        self.curve = np.concatenate((self.curve, straight_curve), axis=1)

        # Encode to array, shape (0,0,6)
        self.vehicle_list = ['ego', 'f', 'l']
        self.vehicle_array = np.zeros(
            (scenario.shape[0], len(self.vehicle_list), 6))
        for i, x, y, v in zip(range(len(self.vehicle_list)), [x0, x1, x7],
                              [y0, y1, y7], [v0, v1, v7]):
            self.vehicle_array[:, i, 0] = x
            self.vehicle_array[:, i, 1] = y
            self.vehicle_array[:, i, 2] = v
            self.vehicle_array[:, i, 3] = np.zeros((scenario.shape[0]))
            self.vehicle_array[:, i, 4] = np.ones(
                (scenario.shape[0])) * self.car_length
            self.vehicle_array[:, i, 5] = np.ones(
                (scenario.shape[0])) * self.car_width
        state = self.get_state('ego')
        return state

    def update(self, action):
        a0, rot0 = action
        state_7 = self.get_state('l')
        a7, rot7 = self.background_control.deside_all(state_7, self.curve)
        # 更新x,y
        for i in ['ego', 'l', 'f']:
            array_sub = self.vehicle_array[:, self.vehicle_list.index(i), :]
            array_sub[:, 0] += array_sub[:, 2] * self.dt * np.cos(
                array_sub[:, 3])
            array_sub[:, 1] += array_sub[:, 2] * self.dt * np.sin(
                array_sub[:, 3])
        ##############
        # 更新v与dir
        for i, a, rot in zip(['ego', 'l'], [a0, a7], [rot0, rot7]):
            array_sub = self.vehicle_array[:, self.vehicle_list.index(i), :]
            array_sub[:, 3] += array_sub[:, 2] / \
                               array_sub[:, 4] * np.tan(rot) * self.dt
            array_sub[:, 2] += a * self.dt
            array_sub[:, 2] = np.clip(array_sub[:, 2], 0, 1e5)
        danger_index,done = self.judge()
        
        return danger_index,done

    def judge(self):
        if self.metric in ['danger','danger_union','problity_injury','dqn','minimum_adjusted_TTC']:
            poly_ego = self.get_poly('ego')
            poly_l = self.get_poly('l')
            poly_f = self.get_poly('f')
            intersection = []
            for ego, f, l in zip(poly_ego, poly_f, poly_l):
                polys = [
                    ego,
                    f,
                    l
                ]
                intersect = [a.intersection(b).area for a, b in combinations(polys, 2)]
                intersection += [sum(intersect)]

        if self.metric == "danger":
            self.result[np.array(intersection) > 0] = 1
            self.done[np.array(intersection) > 0] = 1
        
        elif self.metric == "danger_union":
            self.result = np.max(
                np.concatenate(
                    (self.result.reshape(-1, 1),
                     np.array(intersection).reshape(-1, 1)),
                    axis=1), axis=1)
        
        elif self.metric == 'problity_injury':
            danger_ind = (np.array(intersection) > 0)
            if danger_ind.sum() != self.done.sum():
                for sce_ind in np.where(danger_ind == True)[0]:
                    sce_ind = int(sce_ind)
                    if self.done[sce_ind] != 1:
                        v_diff = 0
                        polys = [
                            poly_ego[sce_ind],
                            poly_f[sce_ind],
                            poly_l[sce_ind]
                        ]
                        for (a,b),(c,d) in zip(combinations(polys,2),combinations(self.vehicle_list,2)):
                            intersect = a.intersection(b).area
                            if intersect > 0:
                                v_diff = max(np.abs(self.vehicle_array[sce_ind,self.vehicle_list.index(c),2] - self.vehicle_array[sce_ind,self.vehicle_list.index(d),2]),v_diff)
                                # 参数取值 论文66页
                                p = 1/(1+np.exp(-(-0.068+0.1*v_diff+-0.6234)))
                                self.result[sce_ind] = max(self.result[sce_ind],p)
            self.done[danger_ind] = 1
        
        elif self.metric == 'minimum_adjusted_TTC':
            # minimum TTC + collision 时计算碰撞概率
            # TTC计算采用option 2
            # 先计算TTC
            state = self.get_state('ego')
            v_diff = (state[:, 0, 2] - state[:, 1, 2])
            v_diff[np.isnan(v_diff)] = -1
            dis_x = (state[:, 1, 0] - state[:, 0, 0]-state[:, 0, 4]/2) #-state[:, 1, 4]/2
            dis_x = np.clip(dis_x,0,1e2)
            ttc_front = dis_x/v_diff
            ttc_front = -ttc_front.copy()
            ttc_front[v_diff <= 0] = -20
            
            danger_ind = (np.array(intersection) > 0)

            if danger_ind.sum() > 0 :
                exist_trigger_1 = np.isnan(state[danger_ind,1,2]) # 如果一号车没有，则用二号车数据，其实也不太合理
                exist_trigger_2 = np.isnan(state[danger_ind,2,2])
                # if exist_trigger_1.sum() > 0:
                v_after_c_2 = (state[danger_ind,0,2] - state[danger_ind,2,2])/2
                v_after_c_1 = (state[danger_ind,0,2] - state[danger_ind,1,2])/2
                v_diff_2 = np.abs(state[danger_ind,0,2] - v_after_c_2)*3.6 # 公式单位是千米/时，因此进行单位转换
                v_diff_1 = np.abs(state[danger_ind,0,2] - v_after_c_1)*3.6 # 如果一号车没有，则用二号车数据
                v_diff = v_diff_1.copy()
                v_diff[exist_trigger_1] = v_diff_2[exist_trigger_1]
                # else: 
                    # v_diff = np.abs(state[danger_ind,0,2] - state[danger_ind,1,2])
                p = 1/(1+np.exp(-(-6.068+0.1*v_diff-0.6234)))
                ttc_danger = p
                ttc_danger[exist_trigger_1 & exist_trigger_2] = -20
                ttc_front[danger_ind] = ttc_danger
                self.done[danger_ind] = 1
            self.result[self.result==0] = -20
            self.result = np.max(
                np.concatenate(
                    (self.result.reshape(-1, 1),
                     np.array(ttc_front).reshape(-1, 1)),
                    axis=1), axis=1)
            # print("v_diff",v_diff[0],"dis_x",dis_x[0],"ttc",ttc_front,"result",self.result[0])
            
        elif self.metric == 'dqn':
            state = self.get_state('ego')
            # self.time_count[state[:,0,2]<1] += 1
            # self.time_count[state[:,0,2]>5] = 0
            # done[self.time_count > 20] = 1
            self.done[np.array(intersection) > 0] = 1
            self.done[state[:,0,2]>44] = 1
            self.result = 0.01-np.abs(self.vehicle_array[:,0,2]-22)/2200
            # self.result[self.time_count > 20] = -1
            self.result[np.array(intersection) > 0] = -1
        
        else:
            print("metric not define!")
        return self.result,self.done

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

    def test(self, scenario, sut=None, metric='danger', plot_key=False, train=False):
        scenario = scenario.reshape(-1, self.scenario_shape)
        assert(scenario.shape[1] == self.scenario_shape)
        self.metric = metric
        if sut == None:
            sut = self.sut
        if plot_key:
            plt.ion()
        new_state = self.init(scenario)
        self.count += scenario.shape[0]
        reward_sum = 0
        self.have_done = np.zeros(scenario.shape[0])
        for i in range(50):
            state = new_state.copy()
            action = sut.deside_all(state)
            reward,done = self.update(action)
            self.have_done[done==1] = 1
            reward_sum += reward[0]
            if plot_key:
                plt.cla()
                self.plot_all(ego=True)
                plt.plot(self.curve[0,:,0],self.curve[0,:,1],'--',alpha=0.3)
                plt.ylim(-40, 40)
                x_center = self.vehicle_array[0,:,0].mean()
                plt.xlim(x_center-70, x_center+70)
                plt.annotate("reward:%.4f"%reward[0],xy=(x_center+30,35))
                plt.annotate("v:%.4f"%state[0,0,2],xy=(x_center+30,30))
                plt.annotate("acc:%.4f"%action[0][0],xy=(x_center+30,25))
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

class ENV(CutIn):
    pass

if __name__ == "__main__":
    from sut.cth import CTH
    print("start")
    sut = CTH()
    # sut = IDM()
    env = CutIn()
    test_sample = np.array([
        [  7.84444444, -16.62499925,   9.44955711,  36.00000167,
          3.208     ,  20.97489056],
        [-5.26634901, -0.26945213, 12.90870356, 8.9958841, 4.51825779,
         11.64973024],
        [-7.51267328, 5.05717046, 17.09979332, 9.76305306, 4.26489982,
         6.05592187],
        [-4.64263618, 2.0785457, 10.68826384, 8.61815371, 4.33900535,
         5.82512958],
        [-5.19969237, 0.26378113, 9.76023079, 9.42338896, 4.27302348
        ,
         7.91196126],
        [-7.84547098, 2.17954859, 21.39272083, 14.28696349, 4.49184155,
         9.27397672],
    ]
    )
    # data = pd.read_csv("data/cut_in_6.csv")
    # test_sample = np.array(data.sample(10))
    res = env.test(test_sample, sut, metric="minimum_adjusted_TTC")
    # print(res)
    for scenario in test_sample:
        res = env.test(scenario, sut, metric='minimum_adjusted_TTC',plot_key=True)
        print(res)
