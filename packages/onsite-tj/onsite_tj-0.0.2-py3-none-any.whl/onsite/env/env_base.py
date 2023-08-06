#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings
from abc import abstractmethod, ABCMeta

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon


class EnvBase(metaclass=ABCMeta):
    """测试环境基类，放置一些通用的方法.

    每个测试环境必须包含两个内容

    vehicle_array : 用以存储所有车辆的信息
    vehicle_list : 用以存储所有车辆的名字
    """
    vehicle_array = np.zeros((0, 0, 6))
    vehicle_list = None
    state = None
    detection_dis = 30
    color_list = ['r','blue','blue','k','blue','k','k','blue','k']

    @abstractmethod
    def init(self):
        """每个测试场景必须包含初始化方法
    
        """
        pass

    @abstractmethod
    def update(self):
        """每个测试场景必须包含场景更新方法
        
        """
        pass

    @abstractmethod
    def judge(self):
        """每个测试场景必须包含判断场景当前时刻状态的方法

        """
        pass

    @abstractmethod
    def test(self, scenario, sut, plot_key):
        """每个测试场景必须包含完成全过程的测试方法

        """
        pass

    @staticmethod
    def _plot_car(x, y, direction=0,txt=None,c='blue', detection_dis=15, l=3, w=1.8):
        """利用 matplotlib 和 patches 绘制小汽车，以 x 轴为行驶方向

        :param x: 本车x坐标
        :param y: 本车y坐标
        :param direction: 本车车头角
        :param c: 本车颜色
        :param detection_dis: 本车检测范围
        :param l: 本车长度
        :param w: 本车宽度
        """
        angle = np.arctan(w / l) + direction
        diagonal = np.sqrt(l ** 2 + w ** 2)
        plt.gca().add_patch(
            patches.Rectangle(
                xy=(x - diagonal / 2 * np.cos(angle),
                    y - diagonal / 2 * np.sin(angle)),
                width=l,
                height=w,
                angle=direction / np.pi * 180,
                color=c
            ))
        if detection_dis > 0 :
            plt.gca().add_patch(
                patches.Circle(
                    xy=(x, y),
                    radius=detection_dis,
                    color=c,
                    fill=False,
                    alpha=0.3,
                    ls='--'
                ))

    def plot_all(self,ego=False):
        """利用 plot_car 方法，绘制存储在vehicle_array中的所有小汽车

        """
        plt.ylim(-50, 50)
        plt.xlim(-20, 80)
        plt.gca().set_aspect('equal')
        if len(self.vehicle_array.shape) == 3:
            plot_array = self.vehicle_array[0, :, :].copy()
        else:
            plot_array = self.vehicle_array.copy()

        for i in range(len(self.vehicle_list)):
            if self.vehicle_list[i] == 'ego':
                self._plot_car(plot_array[i, 0], plot_array[i, 1],
                               plot_array[i, 3], c='red', l=plot_array[i, 4],
                               w=plot_array[i, 5],detection_dis=self.detection_dis)
            else:
                self._plot_car(plot_array[i, 0], plot_array[i, 1],
                               plot_array[i, 3], c='k', l=plot_array[i, 4],
                               w=plot_array[i, 5],detection_dis=self.detection_dis)

        if ego:
            state = self.get_state("ego")[0,:,:].copy()
            for i in range(state.shape[0]):
                if np.isnan(state[i,0]) != True:
                    self._plot_car(state[i, 0], state[i, 1],
                            state[i, 3], c=self.color_list[i], l=state[i, 4],
                            w=state[i, 5],detection_dis=0)
                    plt.text(state[i, 0], state[i, 1], str(i),fontsize=10)
    
    def get_state(self, name):
        """按照车辆名字获取车辆周围车信息的方法。

        输入一个车辆的名字，get_state方法会自动计算并返回一个包含本车的周围9辆车信息的矩阵

        :param name:车辆的名字
        :return: 一个9×6的包含本车的周围9辆车信息的np.array
        """
        scenario_num = self.vehicle_array.shape[0]
        vehicle_num = self.vehicle_array.shape[1]
        self.state = np.full([scenario_num, 9, 6], np.nan)
        # step.1 标定车道
        ego = self.vehicle_array[:, self.vehicle_list.index(name),
              :].copy()  # ego.shape = (场景数,6)
        self.state[:, 0, :] = ego.copy()

        # 计算基本信息
        x_array = self.vehicle_array[:, :, 0].copy()
        dis_x_array = self.vehicle_array[:, :, 0] - ego[:, 0].reshape(-1,
                                                                      1)  # shape (场景数, 车数)
        dis_y_array = self.vehicle_array[:, :, 1] - ego[:, 1].reshape(-1,
                                                                      1)  # shape (场景数, 车数)
        euclidean_array = (dis_y_array ** 2 + dis_x_array ** 2) ** 0.5

        # 标定车道
        # vehicle_array ; shape[scenario_num,vehicle_num,6]
        length_array = self.vehicle_array[:,:,4].copy() # shape (场景数,车数)
        width_array = self.vehicle_array[:,:,5].copy() # shape (场景数,车数)
        alpha = np.arctan(width_array / length_array) # shape (场景数,车数)
        diagonal = np.sqrt(width_array ** 2 + length_array ** 2) # shape (场景数,车数)
        
        diagonal_array = np.concatenate((np.sin(ego[:, 3].reshape(-1,1) + alpha).reshape(scenario_num, vehicle_num, 1), np.sin(
            ego[:, 3].reshape(-1,1) - alpha).reshape(scenario_num, vehicle_num, 1)), axis=2)

        y_bias = diagonal / 2 * np.max(np.abs(diagonal_array),axis=2) # shape (场景数,车数)
        
        lane_array = np.zeros((scenario_num,
                               vehicle_num))  # shape (场景数,车数)
        lane_array[dis_y_array > (y_bias[:,0].reshape(-1,1) + y_bias + 2)] = 1  # 左
        lane_array[-dis_y_array > (y_bias[:,0].reshape(-1,1) + y_bias + 2)] = 2  # 右
        # if name == "ego":
        #     print(lane_array)
        # 删除距离过远车辆
        lane_array[euclidean_array > self.detection_dis] = np.nan
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            # step.2 标定本车道信息
            ind = (lane_array == 0) & (dis_x_array > 0)
            self._fill_state(dis_x_array, ind, 1, 'min')
            ind = (lane_array == 0) & (dis_x_array < 0)
            self._fill_state(dis_x_array, ind, 2, 'max')

            # step.3 标定侧向车道信息
            # 左
            ind = (lane_array == 1)
            self._fill_state(euclidean_array, ind, 7, 'min')
            ind = (lane_array == 1) & (
                    x_array > self.state[:, 7, 0].reshape(-1, 1))
            self._fill_state(x_array, ind, 6, 'min')
            ind = (lane_array == 1) & (
                    x_array < self.state[:, 7, 0].reshape(-1, 1))
            self._fill_state(x_array, ind, 8, 'max')
            # 右
            ind = (lane_array == 2)
            self._fill_state(euclidean_array, ind, 4, 'min')
            ind = (lane_array == 2) & (
                    x_array > self.state[:, 4, 0].reshape(-1, 1))
            self._fill_state(x_array, ind, 3, 'min')
            ind = (lane_array == 2) & (
                    x_array < self.state[:, 4, 0].reshape(-1, 1))
            self._fill_state(x_array, ind, 5, 'max')
        return self.state.reshape(-1,9,6)

    def _fill_state(self, judge_array, ind, car_pos, minormax='min'):
        """填充state所用的方法, 仅在get_state中使用

        :param judge_array:
        :param ind:
        :param car_pos:
        :param minormax:
        """
        assert (minormax in ['min', 'max'])
        array_sub = judge_array.copy()
        exist = (ind.sum(axis=1) != 0)
        array_sub[ind == False] = np.nan
        if minormax == 'min':
            key = np.nanargmin(array_sub[exist], axis=1)
        else:
            key = np.nanargmax(array_sub[exist], axis=1)
        self.state[exist, car_pos, :] = self.vehicle_array[exist, key, :].copy()

    def get_poly(self, name):
        """根据车辆名字获取对应的，符合shapely库要求的矩形。

        这是为了方便地使用shapely库判断场景中的车辆是否发生碰撞

        :param name:车辆的名字
        :return: 一列对应的shapely图形
        """
        # ego = self.vehicle_frame.loc[name]
        ego = self.vehicle_array[:, self.vehicle_list.index(name), :].copy()
        alpha = np.arctan(ego[:, 5] / ego[:, 4])
        diagonal = np.sqrt(ego[:, 5] ** 2 + ego[:, 4] ** 2)
        poly_list = []
        x0 = ego[:, 0] + diagonal / 2 * np.cos(ego[:, 3] + alpha)
        y0 = ego[:, 1] + diagonal / 2 * np.sin(ego[:, 3] + alpha)
        x2 = ego[:, 0] - diagonal / 2 * np.cos(ego[:, 3] + alpha)
        y2 = ego[:, 1] - diagonal / 2 * np.sin(ego[:, 3] + alpha)
        x1 = ego[:, 0] + diagonal / 2 * np.cos(ego[:, 3] - alpha)
        y1 = ego[:, 1] + diagonal / 2 * np.sin(ego[:, 3] - alpha)
        x3 = ego[:, 0] - diagonal / 2 * np.cos(ego[:, 3] - alpha)
        y3 = ego[:, 1] - diagonal / 2 * np.sin(ego[:, 3] - alpha)
        for i in range(x0.shape[0]):
            poly_list += [Polygon(((x0[i], y0[i]), (x1[i], y1[i]),
                                   (x2[i], y2[i]), (x3[i], y3[i]),
                                   (x0[i], y0[i]))).convex_hull]
        return poly_list


if __name__ == "__main__":
    EnvBase._plot_car(15, 10, 45, c='red')
    plt.show()
