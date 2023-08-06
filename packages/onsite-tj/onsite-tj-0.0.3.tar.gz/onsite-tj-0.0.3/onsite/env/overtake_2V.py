import sys
sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from itertools import combinations
from shapely.ops import cascaded_union
from shapely.geometry import Polygon
from env.env_base import EnvBase
from sut.idm import IDM
from sut.curve_pursuit import CP
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import math


class cutIn(EnvBase):


    def __init__(self):
        self._scenario_shape = 3
        self.background_crontrol = CP(a_bound=10)
        self.car_length = 4.924
        self.car_width = 1.872
        self.curve = None
        self.l = 3  # 车辆轴距，单位：m  什么意思？？
        self.dt = 0.1 #时间步长？？
        print("输入场景参数: dif_v7_v0, dif_v1_v7, dif_x7_x0")

    def init(self, scenario):
        self.location_curve = np.zeros([scenario.shape[0]])
        self.y7_sum = np.zeros([scenario.shape[0]])
        [dif_v7_v0, dif_v1_v7, dif_x7_x0] = scenario[:,
                                                     0], scenario[:, 1], scenario[:, 2]

        # 初始化前车，侧向车与本车的速度
        v1 = np.ones([scenario.shape[0]])*15
        v7 = v1 - dif_v1_v7
        v0 = v7 - dif_v7_v0
        if ((v0 <= 0) | (v1 <= 0) | (v7 <= 0)).sum() > 0:
            warnings.warn('Initial speed that smaller than 0!', UserWarning)
            v1[v1 <= 0] = 0
            v7 = v1 - dif_v1_v7
            v7[v7 <= 0] = 0
            v0 = v7 - dif_v7_v0
            v0[v0 <= 0] = 0

        # 前车与侧向车纵向距离
        dif_x1_x7 = np.ones([scenario.shape[0]])*35

        # 本车与侧向车横向距离
        dif_y7_y0 = np.ones([scenario.shape[0]])*3.5

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
        
        bezier_7 = pd.DataFrame(dif_y7_y0) #-dif_y7_y0目前为负，改成正的曲线形态会变成超车前期
        print("bezier_7")
        print(bezier_7[0])
        curve = np.array(list(map(self.BezierCurve1, bezier_7[0])))
        self.curve = curve.reshape(scenario.shape[0], -1, 2)
        # self.curve[:, :, 0] += x7.reshape(-1, 1) #reshape(-1, n) 函数， 表示将此矩阵或者数组重组，以 m行n列的形式表示
        # self.curve[:, :, 1] += y7.reshape(-1, 1)
        # Encode to array, shape (0,0,6)
        # self.vehicle_list = ['ego', 'f', 'l']
        # self.vehicle_array = np.zeros(
        #     (scenario.shape[0], len(self.vehicle_list), 6))
        # for i, x, y, v in zip(range(len(self.vehicle_list)), [x0, x1, x7], [y0, y1, y7], [v0, v1, v7]):
        #     self.vehicle_array[:26, i, 0] = x
        #     self.vehicle_array[:26, i, 1] = y
        #     self.vehicle_array[:26, i, 2] = v
        #     self.vehicle_array[:26, i, 3] = np.zeros((scenario.shape[0]))
        #     self.vehicle_array[:26, i, 4] = np.ones(
        #         (scenario.shape[0])) * self.car_length
        #     self.vehicle_array[:26, i, 5] = np.ones(
        #         (scenario.shape[0])) * self.car_width
        
        
        bezier_8 = pd.DataFrame(dif_y7_y0) #-dif_y7_y0目前为负，改成正的曲线形态会变成超车前期
        print("bezier_8")
        print(bezier_8[0])
        curve = np.array(list(map(self.BezierCurve2, bezier_8[0])))
        curve = curve.reshape(scenario.shape[0], -1, 2)

        self.curve = np.concatenate((self.curve,curve),axis=1)
        

        self.curve[:, :, 0] += x7.reshape(-1, 1) #reshape(-1, n) 函数， 表示将此矩阵或者数组重组，以 m行n列的形式表示
        self.curve[:, :, 1] += y7.reshape(-1, 1)
        # Encode to array, shape (0,0,6)
        self.vehicle_list = ['ego', 'f', 'l']
        self.vehicle_array = np.zeros(
            (scenario.shape[0], len(self.vehicle_list), 6))
        for i, x, y, v in zip(range(len(self.vehicle_list)), [x0, x1, x7], [y0, y1, y7], [v0, v1, v7]):
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
        straight_curve = np.concatenate(
            (np.linspace(0, 50, 100).reshape(-1, 1), np.zeros(100).reshape(-1, 1)), axis=1)
        straight_curve = np.expand_dims(
            straight_curve, 0).repeat(self.curve.shape[0], axis=0)
        straight_curve += self.curve[:, -1,
                                     :].reshape(self.curve.shape[0], 1, -1)
        curve = np.concatenate((self.curve, straight_curve), axis=1)
        a7, rot7 = self.background_crontrol.deside_all(state_7, curve)
        # 更新x,y
        for i in ['ego', 'l', 'f']:
            array_sub = self.vehicle_array[:, self.vehicle_list.index(i), :]
            array_sub[:, 0] += array_sub[:, 2]*self.dt*np.cos(array_sub[:, 3])
            array_sub[:, 1] += array_sub[:, 2]*self.dt*np.sin(array_sub[:, 3])
        ##############
        # 更新v与dir
        for i, a, rot in zip(['ego', 'l'], [a0, a7], [rot0, rot7]):
            array_sub = self.vehicle_array[:, self.vehicle_list.index(i), :]
            array_sub[:, 3] += array_sub[:, 2] / \
                array_sub[:, 4]*np.tan(rot)*self.dt
            array_sub[:, 2] += a * self.dt
            array_sub[:, 2] = np.clip(array_sub[:, 2], 0, 1e5)
        danger_index = self.judge()
        return danger_index


    def judge(self):
        result = np.zeros(self.vehicle_array.shape[0])
        poly_ego = self.get_poly('ego')
        poly_l = self.get_poly('l')
        poly_f = self.get_poly('f')
        intersection = []
        for ego, f, l in zip( poly_ego, poly_f, poly_l):
            polys = [
                ego,
                f,
                l
            ]
            intersect = cascaded_union(
                [a.intersection(b) for a, b in combinations(polys, 2)]
            )
            intersection += [intersect.area]
        result[np.array(intersection) > 0] = 1
        return result

    @staticmethod
    def BezierCurve1(end_py, start_px=0, start_py=0, end_px=30, start_heading=0, end_heading=0):
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
        # print(end_py)
        t = np.linspace(0, 1, num=int(25))
        x1 = start_px * 2.0 / 3 + end_px * 1.0 / 3  # vector (sample.shape,1)
        x2 = start_px * 1.0 / 3 + end_px * 2.0 / 3  # vector (sample.shape,1)
        y1 = start_py * 2.0 / 3 + end_py * 1.0 / 3  # vector (sample.shape,1)
        y2 = start_py * 1.0 / 3 + end_py * 2.0 / 3  # 三等分点 # vector (sample.shape,1)
        p1_x = (y1 - start_py - np.tan(start_heading + np.pi / 2) * x1 + np.tan(start_heading) * start_px) / \
               (np.tan(start_heading) - np.tan(start_heading +
                                               np.pi / 2))  # vector (sample.shape,1)
        p1_y = np.tan(start_heading) * (p1_x - start_px) + \
            start_py  # vector (sample.shape,1)
        p2_x = (y2 - end_py - np.tan(end_heading + np.pi / 2) * x2 + np.tan(end_heading) * end_px) / \
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

    @staticmethod
    def BezierCurve2(start_py, end_py=0, start_px=30, end_px=60, start_heading=0, end_heading=0):
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
        print(start_py)
        t = np.linspace(0, 1, num=int(25))
        x1 = start_px * 2.0 / 3 + end_px * 1.0 / 3  # vector (sample.shape,1)
        x2 = start_px * 1.0 / 3 + end_px * 2.0 / 3  # vector (sample.shape,1)
        y1 = start_py * 2.0 / 3 + end_py * 1.0 / 3  # vector (sample.shape,1)
        y2 = start_py * 1.0 / 3 + end_py * 2.0 / 3  # 三等分点 # vector (sample.shape,1)
        p1_x = (y1 - start_py - np.tan(start_heading + np.pi / 2) * x1 + np.tan(start_heading) * start_px) / \
               (np.tan(start_heading) - np.tan(start_heading +
                                               np.pi / 2))  # vector (sample.shape,1)
        p1_y = np.tan(start_heading) * (p1_x - start_px) + \
            start_py  # vector (sample.shape,1)
        p2_x = (y2 - end_py - np.tan(end_heading + np.pi / 2) * x2 + np.tan(end_heading) * end_px) / \
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

    def test(self, scenario, sut,  plot_key=False):
        scenario = scenario.reshape(-1, self._scenario_shape)
        assert(scenario.shape[1] == self._scenario_shape)
        if plot_key:
            plt.ion()
        result = np.zeros(scenario.shape[0])
        # 初始化场景，场景参数→state 9*5 x,y,v,dir,length, width
        state = self.init(scenario)
        for i in range(30):
            state = self.get_state('ego')
            a, rot = sut.deside_all(state)
            # 更新state, 返回reward
            danger_index = self.update([a, rot])
            result[danger_index == 1] = 1
            if plot_key:
                plt.cla()
                plt.plot(self.curve[0, :, 0], self.curve[0, :, 1])
                self.plot_all()
                plt.pause(1e-2)
                plt.show()
        return result


if __name__ == "__main__":
    print("start")
    import time
    import multiprocessing
    from sut.rot_test import ROT
    sut = IDM()
    # sut = ROT(rot_speed=10*np.pi/180)
    env = cutIn()
    test_sample = np.array([
        [-0.935513833,	-13.52682938,	13.62226994],
        [-3.757009286,	0.879751554,	8.203278612],
        [-1.646032093,	-17.04708008,	15.05895378],
        [-5.144133455,	4.477844891,	10.51108026],
    ]
    )
    # env.test(test_sample,sut)
    for i in test_sample:
        print(env.test(i.reshape(1,-1), sut, plot_key=True))
