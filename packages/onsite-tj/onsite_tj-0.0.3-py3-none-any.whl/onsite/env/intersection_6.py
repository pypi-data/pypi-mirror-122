# coding=utf-8
import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon

sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from sut.idm import IDM
from sut.curve_pursuit import CP


class Intersection:

    def __init__(self, a_bound=5,sut=None):
        self.scenario_shape = 6  # 6
        self.background_control = IDM(a_bound=a_bound)
        self.car_length = 4.924
        self.car_width = 1.872
        self.dt = 0.1
        self.l = 3  # 车辆轴距，单位：m
        self.metric = 'danger'
        print("输入参数:car1_DistoStart, r, car2_DistoCross, v1, v2, y2")
        if sut == None:
            self.sut = CP(5)
        else:
            self.sut = sut

    @staticmethod
    def plot_car(x, y, direction=0, c='blue', l=3, w=1.8):
        plt.ylim(-50, 50)
        plt.xlim(-20, 80)
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

    def init(self, scenario):
        self.result = np.zeros([scenario.shape[0]])
        [car1_DistoStart, r, car2_DistoCross, v1, v2, y2] = [scenario[:, i]
                                                             for i in range(
                self.scenario_shape)]
        self.car1_DistoStart = car1_DistoStart
        self.car2_DistoCross = car2_DistoCross
        self.x1 = np.zeros([scenario.shape[0]])
        self.y1 = np.zeros([scenario.shape[0]])
        self.v1 = v1
        self.dir1 = np.zeros([scenario.shape[0]])
        self.x2 = np.full(
            scenario.shape[0],
            car2_DistoCross + (r ** 2 - (r - y2) ** 2) ** 0.5 + car1_DistoStart)
        self.y2 = y2
        self.v2 = v2
        self.dir2 = np.full(scenario.shape[0], -np.pi)
        self.r = r
        self.curve = self.get_curve()
        self.x2_init = self.x2.copy()  # 记录2号车的初始位置
        self.cross_x = self.x2 - car2_DistoCross  # 计算冲突点位置
        self.cross_y = y2.copy()  # 计算冲突点位置
        self.car1_arc_full = np.arccos((r - y2) / r) * r  # 计算car1到交点的完整的弧长

    def get_curve(self):
        car1_DistoStart = self.car1_DistoStart.copy()
        r = self.r.copy()
        horizontal_x = np.linspace(0, car1_DistoStart, 100).T  # n*100
        horizontal_y = np.zeros(horizontal_x.shape)  # n *100
        circle_x = np.linspace(0, r, 100).T
        circle_y = -np.sqrt(r.reshape(-1, 1) ** 2 - circle_x ** 2)  # 下半圆
        circle_x += car1_DistoStart.reshape(-1, 1)
        circle_y += r.reshape(-1, 1)  # 调整圆心坐标
        vertical_y = np.linspace(0, np.full(r.shape, 50), 100).T
        vertical_x = np.zeros(vertical_y.shape)
        vertical_y += r.reshape(-1, 1)
        vertical_x += car1_DistoStart.reshape(-1, 1) + r.reshape(-1, 1)
        curve_x = np.concatenate((horizontal_x, circle_x, vertical_x), axis=1)
        curve_y = np.concatenate((horizontal_y, circle_y, vertical_y), axis=1)
        curve = np.concatenate(
            (curve_x.reshape(-1, curve_x.shape[1], 1),
             curve_y.reshape(-1, curve_x.shape[1], 1)), axis=2)
        return curve

    def get_dis_to_cross(self):
        car2_to_cross = self.car2_DistoCross - (self.x2_init - self.x2)
        car1_to_cross = np.zeros(car2_to_cross.shape)
        car1_hori = self.x1 < self.car1_DistoStart  # 记录car1位置是否在水平线上, True在,False不在
        # 对于在水平线上的本车
        car1_to_cross[car1_hori] = self.car1_DistoStart[car1_hori] - \
                                   self.x1[car1_hori] + self.car1_arc_full[
                                       car1_hori]
        # 对于不在水平线上的本车
        ind = (car1_hori == False)
        car1_angle = (self.r[ind] - self.y1[ind]) / self.r[ind]
        car1_angle = np.clip(car1_angle, -1, 1)
        car2_angle = (self.r[ind] - self.y2[ind]) / self.r[ind]
        car2_angle = np.clip(car2_angle, -1, 1)
        car1_to_cross[ind] = self.r[ind] * \
                             (np.arccos(car2_angle) - np.arccos(car1_angle))

        # print("car1_to_cross:%.2f" % car1_to_cross[0],"car2_to_cross:%.2f" % car2_to_cross[0])
        return car1_to_cross, car2_to_cross

    def get_state(self):
        self.get_dis_to_cross()
        state_car_1 = np.full((self.x1.shape[0], 9, 6), np.nan)
        state_car_1[:, 0, :] = np.concatenate(
            (
                self.x1.reshape(-1, 1),
                self.y1.reshape(-1, 1),
                self.v1.reshape(-1, 1),
                self.dir1.reshape(-1, 1),
                np.full((self.x1.shape[0], 1), self.car_length),
                np.full((self.x1.shape[0], 1), self.car_width)
            ), axis=1)
        state_car_2 = np.full((self.x1.shape[0], 9, 6), np.nan)
        state_car_2[:, 0, :] = np.concatenate(
            (
                self.x2.reshape(-1, 1),
                self.y2.reshape(-1, 1),
                self.v2.reshape(-1, 1),
                self.dir2.reshape(-1, 1),
                np.full((self.x1.shape[0], 1), self.car_length),
                np.full((self.x1.shape[0], 1), self.car_width)
            ), axis=1)
        car1_to_cross, car2_to_cross = self.get_dis_to_cross()
        car1_cross_t, car2_cross_t = [
            car1_to_cross / self.v1, car2_to_cross / self.v2]
        # 其中一者为负数，两车均自由行驶
        # 均为正数，则计算本车时距-冲突车时距：
        # 1、绝对值大于1.5s,均自由行驶
        # 2、绝对值小于1.5s,时距大的按冲突点有静止车行驶
        state1 = (car1_cross_t < 0) | (car2_cross_t < 0)
        state2 = (state1 == False) & (np.abs(car1_cross_t - car2_cross_t) > 1.5)
        state3 = (state1 == False) & (state2 == False) & (
                car1_cross_t - car2_cross_t < 0)
        state4 = (state1 == False) & (state2 == False) & (
                car1_cross_t - car2_cross_t > 0)
        # state1,state2 不需要改变state
        # state3,state4 为时距大的车的前车赋值
        num = state3.sum()
        state_car_2[state3, 1, :] = np.concatenate(
            (
                self.cross_x[state3].reshape(-1, 1),
                self.cross_y[state3].reshape(-1, 1),
                np.full((num, 1), 0),
                self.dir2[state3].reshape(-1, 1),
                np.full((num, 1), self.car_length),
                np.full((num, 1), self.car_width)
            ), axis=1)
        num = state4.sum()
        state_car_1[state4, 1, :] = np.concatenate(
            (
                self.cross_x[state4].reshape(-1, 1),
                self.cross_y[state4].reshape(-1, 1),
                np.full((num, 1), 0),
                self.dir1[state4].reshape(-1, 1),
                np.full((num, 1), self.car_length),
                np.full((num, 1), self.car_width)
            ), axis=1)
        self.state1 = state_car_1
        self.state2 = state_car_2

    def update(self, action):
        # 根据前向欧拉更新，根据旧速度更新位置，然后更新速度
        # x0,y0,v0,dir0,length0
        a1, rot1 = action
        a2, rot2 = self.background_control.deside_all(self.state2)
        # 更新x,y
        self.x1 += self.v1 * self.dt * np.cos(self.dir1)
        self.y1 += self.v1 * self.dt * np.sin(self.dir1)
        self.x2 += self.v2 * self.dt * np.cos(self.dir2)
        self.y2 += self.v2 * self.dt * np.sin(self.dir2)

        # 更新dir
        self.dir1 += self.v1 / self.l * np.tan(rot1) * self.dt
        # print(self.dir1)
        # 更新v
        self.v1 += a1 * self.dt
        self.v1 = np.clip(self.v1, 0, 1e5)
        self.v2 += a2 * self.dt
        self.v2 = np.clip(self.v2, 0, 1e5)
        danger_index = self.judge()
        return danger_index

    def judge(self):
        poly_ego = self.get_poly(self.x1, self.y1, self.dir1)
        poly_l = self.get_poly(self.x2, self.y2, self.dir2)
        intersection = []
        for ego, l in zip(poly_ego, poly_l):
            intersection += [ego.intersection(l).area]
        if self.metric == "danger":
            self.result[np.array(intersection) > 0] = 1
        elif self.metric == "danger_union":
            self.result = np.max(
                np.concatenate(
                    (self.result.reshape(-1, 1),
                     np.array(intersection).reshape(-1, 1)),
                    axis=1), axis=1)
        else:
            print("metric not define!")
        return self.result

    def get_poly(self, x, y, dir):
        # ego = self.vehicle_frame.loc[name]
        alpha = np.arctan(self.car_width / self.car_length)
        diagonal = np.sqrt(self.car_width ** 2 + self.car_length ** 2)
        poly_list = []
        x0 = x + diagonal / 2 * np.cos(dir + alpha)
        y0 = y + diagonal / 2 * np.sin(dir + alpha)
        x2 = x - diagonal / 2 * np.cos(dir + alpha)
        y2 = y - diagonal / 2 * np.sin(dir + alpha)
        x1 = x + diagonal / 2 * np.cos(dir - alpha)
        y1 = y + diagonal / 2 * np.sin(dir - alpha)
        x3 = x - diagonal / 2 * np.cos(dir - alpha)
        y3 = y - diagonal / 2 * np.sin(dir - alpha)
        for i in range(x0.shape[0]):
            poly_list += [Polygon(((x0[i], y0[i]), (x1[i], y1[i]),
                                   (x2[i], y2[i]), (x3[i], y3[i]),
                                   (x0[i], y0[i]))).convex_hull]
        return poly_list

    def test(self, scenario, sut=None, metric='danger', plot_key=False):
        scenario = scenario.reshape(-1, self.scenario_shape)
        assert (scenario.shape[1] == self.scenario_shape)
        self.metric = metric
        if sut == None:
            sut = self.sut
        if plot_key:
            plt.ion()
        # 初始化场景，场景参数→state 9*5 x,y,v,dir,length, width
        self.init(scenario)
        for i in range(40):
            self.get_state()
            a, rot = sut.deside_all(self.state1, self.curve)
            danger_index = self.update([a, rot])
            if plot_key:
                plt.cla()
                plt.plot(self.curve[0, :, 0], self.curve[0, :, 1])
                plt.plot(self.x1[0], self.y1[0], '*')
                plt.plot(self.x2[0], self.y2[0], '*')
                self.plot_car(self.x1[0], self.y1[0], self.dir1[0], c='red',
                              l=self.car_length, w=self.car_width)
                self.plot_car(self.x2[0], self.y2[0], self.dir2[0], c='k',
                              l=self.car_length, w=self.car_width)
                plt.pause(1e-2)
                plt.show()
            if sut.trainable:
                print("当前场景无法训练规控器")

        return self.result

class ENV(Intersection):
    pass

if __name__ == "__main__":
    print("start")
    # sut = IDM()
    sut = CP()
    env = Intersection()
    test_sample = np.array([
        [10, 15, 15, 15, 5, 4.],
        [10, 15, 15, 14, 18, 5.],
        [10, 20, 15, 20, 10, 6.],
        [10, 25, 20, 15, 20, 7.],
        [10, 30, 25, 20, 10, 8.],
    ])
    print(env.test(test_sample, sut, metric="danger_union", plot_key=False))
    for scenario in test_sample:
        res = env.test(scenario, sut, plot_key=True)
        # print(type(scenario))
        print(res)
