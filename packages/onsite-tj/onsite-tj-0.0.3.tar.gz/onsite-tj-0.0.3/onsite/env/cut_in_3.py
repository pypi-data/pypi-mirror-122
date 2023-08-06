import sys

sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from itertools import combinations
from shapely.ops import cascaded_union
from env.env_base import EnvBase
from env.cut_in_6 import CutIn
from sut.idm import IDM
from sut.curve_pursuit import CP
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings


class CutIn3(CutIn):

    def __init__(self, a_bound=5,sut=None):
        self.scenario_shape = 3
        self.background_control = CP(a_bound=a_bound)
        self.car_length = 4.924
        self.car_width = 1.872
        self.curve = None
        self.l = 3  # 车辆轴距，单位：m
        self.dt = 0.1
        self.metric = 'danger'
        print("输入场景参数: dif_v7_v0, dif_v1_v7, dif_x7_x0")
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
        [dif_v7_v0, dif_v1_v7, dif_x7_x0] = [scenario[:, i]
                                             for i in range(
                self.scenario_shape)]

        # 初始化前车，侧向车与本车的速度
        v1 = np.ones([scenario.shape[0]]) * 15
        v7 = v1 - dif_v1_v7
        v0 = v7 - dif_v7_v0
        if ((v0 <= 0) | (v1 <= 0) | (v7 <= 0)).sum() > 0:
            v1[v1 <= 0] = 0
            v7 = v1 - dif_v1_v7
            v7[v7 <= 0] = 0
            v0 = v7 - dif_v7_v0
            v0[v0 <= 0] = 0

        # 前车与侧向车纵向距离
        dif_x1_x7 = np.ones([scenario.shape[0]]) * 35

        # 本车与侧向车横向距离
        dif_y7_y0 = np.ones([scenario.shape[0]]) * 3.5

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

class ENV(CutIn3):
    pass

if __name__ == "__main__":
    print("start")

    sut = IDM()
    # sut = ROT(rot_speed=10*np.pi/180)
    env = CutIn3()
    test_sample = np.array([
        # [-0.935513833, -13.52682938, 13.62226994],
        # [-6.4,9.99,3.38],
        [-9.4 ,  9.99, 6.38],
        # [-1.646032093, -17.04708008, 15.05895378],
        # [-5.144133455, 4.477844891, 10.51108026],
    ]
    )
    for i in test_sample:
        print(env.test(i.reshape(1, -1), sut, metric='minimum_adjusted_TTC',
                       plot_key=True))
