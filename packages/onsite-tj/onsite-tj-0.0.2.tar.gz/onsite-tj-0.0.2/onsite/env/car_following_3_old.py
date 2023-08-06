import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from env.env_base import EnvBase

class CarFollowing(EnvBase):

    def __init__(self):
        self.scenario_shape = 3
        self.car_length = 4.924
        self.car_width = 1.872
        self.l = 4  # 车辆轴距，单位：m
        print('carFollowing场景，输入参数fv,dif_v,dis！')

    def init(self, scenario):
        [v1, dif_v, dis] = [scenario[:, i]
                            for i in range(self.scenario_shape)]
        v0 = v1 - dif_v
        dis = np.clip(dis, 0, 1e5)
        v0 = np.clip(v0, 0, 1e5)
        x0 = np.zeros((scenario.shape[0],))
        x1 = dis.copy()
        y0, y1, dir0, dir1 = [np.zeros((scenario.shape[0],)) for i in range(4)]
        length0, length1 = [
            np.ones((scenario.shape[0],))*self.car_length for i in range(2)]
        width0, width1 = [
            np.ones((scenario.shape[0],))*self.car_width for i in range(2)]
        # state 9*6 x,y,v,dir,length,width
        state = np.full([scenario.shape[0], 9, 6], np.nan)
        item_list_0 = [x0, y0, v0, dir0, length0, width0]
        item_list_1 = [x1, y1, v1, dir1, length1, width1]
        for i in range(state.shape[2]):
            state[:, 0, i] = item_list_0[i]
            state[:, 1, i] = item_list_1[i]
        return state

    def update(self, state, action):
        # 根据前向欧拉更新，根据旧速度更新位置，然后更新速度
        # x0,y0,v0,dir0,length0
        # 更新x
        a,rot = action
        for i in [0,1]:
            state[:, i, 0] += state[:, i, 2]*0.1*np.cos(state[:, i, 3]) #*np.pi/180
            state[:, i, 1] += state[:, i, 2]*0.1*np.sin(state[:, i, 3]) #*np.pi/180
        # 更新dir
        state[:, 0, 3] += state[:,0,2]/self.l*np.tan(rot) * 0.1
        # 更新v
        state[:, 0, 2] += a * 0.1
        state[:, 0, 2] = np.clip(state[:, 0, 2], 0, 1e5)
        danger_index = self.judge(state)

        return state, danger_index

    def judge(self, state):
        danger_index = ((state[:, 1, 0]-state[:, 0, 0]) < self.car_length)
        return danger_index

    def test(self, scenario, sut,  plot_key=False):
        scenario = scenario.reshape(-1, self.scenario_shape)
        assert(scenario.shape[1] == self.scenario_shape)
        if plot_key:
            plt.ion()
        result = np.zeros([scenario.shape[0]])
        state = self.init(scenario)
        for i in range(30):
            a, rot = sut.deside_all(state)
            state, danger_index = self.update(state, [a, rot])
            result[danger_index] = 1
            if plot_key:
                plt.cla()
                self.plot_all(state)
                plt.pause(1e-2)
                plt.show()
        return result


if __name__ == "__main__":
    from sut.idm import IDM
    from sut.rot_test import ROT
    print("start")
    # sut = IDM()
    sut = ROT(rot_speed=5*np.pi/180)
    env = carFollowing()
    # 场景参数定义在此处
    test_sample = np.array([
        [4.88619646, -5.51864016, 27.06436162],
        [4.81720291, 0.42054838, 10.26410715],
        [7.92313679, -2.37679344, 15.78525394],
        [5.84214011, 0.72061848, 12.35805587],
        [7.25463418, -0.0982501, 14.04462361],
    ])
    for scenario in test_sample:
        res = env.test(scenario, sut,  plot_key=True)
        print(res)
    print(env.test(test_sample, sut))
    # print(env.test(test_sample[2],sut))
