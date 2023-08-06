import sys

import matplotlib.pyplot as plt
import numpy as np

from .env_base import EnvBase
from SAAS_base.sut.idm import IDM

class CarFollowing(EnvBase):
    """三参数的跟驰场景，
       场景由[前车速度,前车-本车速度,两车距离]定义

    """

    def __init__(self,sut=None):
        self.scenario_shape = 3
        self.car_length = 4.924
        self.car_width = 1.872
        self.l = 3  # 车辆轴距，单位：m
        self.dt = 0.1
        self.metric = 'danger'
        print('carFollowing场景，输入参数fv,dif_v,dis！')
        if sut == None:
            self.sut = IDM(5)
        else:
            self.sut = sut
        self.count = 0

    def init(self, scenario):
        scenario = scenario.copy()
        self.result = np.zeros([scenario.shape[0]])
        self.done = np.zeros([scenario.shape[0]])
        [v1, dif_v, dis] = [scenario[:, i]
                            for i in range(self.scenario_shape)]
        v0 = v1 - dif_v
        dis = np.clip(dis, 0, 1e5)
        v0 = np.clip(v0, 0, 1e5)
        x0 = np.zeros((scenario.shape[0],))
        x1 = dis.copy()

        # Encode to array, shape (0,0,6)
        y0, y1, dir0, dir1 = [np.zeros((scenario.shape[0],)) for i in range(4)]
        length0, length1 = [
            np.ones((scenario.shape[0],)) * self.car_length for i in range(2)]
        width0, width1 = [
            np.ones((scenario.shape[0],)) * self.car_width for i in range(2)]

        self.vehicle_list = ['ego', 'f']
        self.vehicle_array = np.zeros(
            (scenario.shape[0], len(self.vehicle_list), 6))
        item_list_0 = [x0, y0, v0, dir0, length0, width0]
        item_list_1 = [x1, y1, v1, dir1, length1, width1]
        for i in range(self.vehicle_array.shape[2]):
            self.vehicle_array[:, 0, i] = item_list_0[i]
            self.vehicle_array[:, 1, i] = item_list_1[i]
        state = self.get_state('ego')
        return state

    def update(self, action):
        # 根据前向欧拉更新，根据旧速度更新位置，然后更新速度
        # x0,y0,v0,dir0,length0
        # 更新x
        a, rot = action
        for i in range(len(self.vehicle_list)):
            self.vehicle_array[:, i, 0] += self.vehicle_array[:, i,
                                           2] * self.dt * np.cos(
                self.vehicle_array[:, i, 3])  # *np.pi/180
            self.vehicle_array[:, i, 1] += self.vehicle_array[:, i,
                                           2] * self.dt * np.sin(
                self.vehicle_array[:, i, 3])  # *np.pi/180
        # 更新dir
        self.vehicle_array[:, 0, 3] += self.vehicle_array[:, 0,
                                       2] / self.l * np.tan(rot) * self.dt
        # 更新v
        self.vehicle_array[:, 0, 2] += a * self.dt
        self.vehicle_array[:, 0, 2] = np.clip(self.vehicle_array[:, 0, 2], 0,
                                              1e5)
        judge_value,done = self.judge()

        return judge_value,done

    def judge(self):
        if self.metric in ['danger','danger_union','danger_v','dqn','minimum_adjusted_TTC']:
            poly_ego = self.get_poly('ego')
            poly_f = self.get_poly('f')
            intersection = []
            for ego, f in zip(poly_ego, poly_f):
                intersection += [ego.intersection(f).area]
        if self.metric == "danger":
            self.result[np.array(intersection) > 0] = 1
            self.done[np.array(intersection) > 0] = 1
        elif self.metric == 'danger_v':
            danger_ind = (np.array(intersection) > 0)
            if danger_ind.sum() != self.done.sum():
                danger_ind = (danger_ind != self.done)
                v_diff = self.vehicle_array[danger_ind,0,2]-self.vehicle_array[danger_ind,1,2]
                p = 1/(1+np.exp(-(-0.068+0.1*v_diff+-0.6234)))
                self.result[danger_ind] = np.max(
                    np.concatenate(
                        (self.result[danger_ind].reshape(-1, 1),
                        (p.reshape(-1,1))),
                        axis=1))
            self.done[danger_ind] = 1
        elif self.metric == "danger_union":
            self.result = np.max(
                np.concatenate(
                    (self.result.reshape(-1, 1),
                     np.array(intersection).reshape(-1, 1)),
                    axis=1), axis=1)
            self.done = np.zeros([self.result.shape[0]])
        elif self.metric == "dqn":
            self.result = 0.01-np.abs(self.vehicle_array[:,0,2]-22)/2200
            self.result[np.array(intersection) > 0] = -1
            self.done[np.array(intersection) > 0] = 1
        elif self.metric == 'minimum_adjusted_TTC':
            # minimum TTC + collision 时计算碰撞概率
            # TTC计算采用option 2
            # 先计算TTC
            state = self.get_state('ego')
            v_diff = (state[:, 0, 2] - state[:, 1, 2])
            v_diff[np.isnan(v_diff)] = -1
            dis_x = (state[:, 1, 0] - state[:, 0, 0]-state[:, 0, 4]/2) #-state[:, 1, 4]/2
            dis_x = np.clip(dis_x,0,1e2)
            ttc_front = dis_x/(v_diff+1e-6)
            ttc_front = -ttc_front.copy()
            ttc_front[v_diff <= 0] = -1e2
            
            danger_ind = (np.array(intersection) > 0)

            if danger_ind.sum() > 0 : # 有碰撞
                # 当本车中心点越过前车中心点时，会出现nan值，因此下方代码针对异常值进行了处理
                exist_trigger_1 = np.isnan(state[danger_ind,1,2]) # 前车是否不存在
                v_diff_2 = 0
                v_after_c = 0.5*(state[danger_ind,0,2] + state[danger_ind,1,2]) 
                v_diff_1 =  (state[danger_ind,0,2] - v_after_c)*3.6 # 公式单位是千米/时，因此进行单位转换
                v_diff = v_diff_1.copy()
                v_diff[exist_trigger_1] = v_diff_2
                # 根据公式计算P值
                p = 1/(1+np.exp(-(-6.068+0.1*v_diff-0.6234)))
                ttc_front[danger_ind] = p
                self.done[danger_ind] = 1
            self.result[self.result==0] = -1e2
            self.result = np.max(
                np.concatenate(
                    (self.result.reshape(-1, 1),
                     np.array(ttc_front).reshape(-1, 1)),
                    axis=1), axis=1)
        else:
            print("metric not define!")
        return self.result,self.done

    def test(self, scenario, sut=None, metric='danger', plot_key=False, train=False):
        scenario = np.array(scenario)
        scenario = scenario.reshape(-1, self.scenario_shape).copy()
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
                self.plot_all()
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

class ENV(CarFollowing):
    pass

if __name__ == "__main__":
    print("start")
    # from sut.dqn import DQN
    from sut.idm import IDM
    sut = IDM()
    # sut = DQN(trainable=False,a_bound=5,rot_sut=rot_sut,loadpath="output/dqn/lane_change.h5")
    env = CarFollowing()
    # 场景参数定义在此处
    test_sample = np.array([
    #     [  5. , -10. ,  20. ],
    #    [ 12.5, -15. ,  30. ],
    #    [ 25. , -30. ,  30. ],
       [ 29. , -7. ,  10. ],
       [ 35, -7. ,  10. ],
    #    [ 18. , -10. ,  10. ],
    #    [ 19.5, -10. ,  10. ],
    #    [ 20. , -10. ,  10. ],
    #    [ 22.5, -10. ,  10. ],
    #    [ 25. , -10. ,  10. ],
        # [0, -5.51864016, 7],
        # [4.81720291, 0.42054838, 10.26410715],
        # [7.92313679, -2.37679344, 15.78525394],
        # [5.84214011, 0.72061848, 12.35805587],
        # [7.25463418, -0.0982501, 14.04462361],
    ])
    print(env.test(test_sample,sut=sut,metric="minimum_adjusted_TTC",plot_key=False))
    for scenario in test_sample:
        res = env.test(scenario,sut=sut,metric="minimum_adjusted_TTC", plot_key=True)
        print(res)
    
