#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import lib
import sys
from .sut_base import sutBase
import numpy as np


class IDM(sutBase):
    def __init__(self, a_bound=5.0, exv=21.72, t=1.2, a=2.22, b=2.4, gama=4, s0=1.0, s1=2.0):
        """跟idm模型有关的模型参数，一定要记得调整

        :param a_bound: 本车加速度绝对值的上下界
        :param exv: 期望速度
        :param t: 反应时间
        :param a: 起步加速度
        :param b: 舒适减速度
        :param gama: 加速度指数
        :param s0: 静止安全距离
        :param s1: 与速度有关的安全距离选择参数
        """
        self.a_bound = a_bound
        self.exv = exv
        self.t = t
        self.a = a
        self.b = b
        self.gama = gama
        self.s0 = s0
        self.s1 = s1
        self.s_ = 0

    def deside_acc(self, state):
        v, fv, dis_gap = state[:,0, 2], state[:,1, 2], state[:,1,0] - state[:,0,0] - 0.5*(state[:,1,4]+state[:,0,4])
        ind = np.isnan(fv)
        fv[ind] = self.exv
        ind = np.isnan(dis_gap)
        dis_gap[ind] = state[0,0,4]*10
        # 求解本车与前车的期望距离
        self.s_ = self.s0 + self.s1 * (v / self.exv) ** 0.5 + self.t * v + v * (
            v - fv) / 2 / (self.a * self.b) ** 0.5
        # 求解本车加速度
        a_idm = self.a * (1 - (v / self.exv) ** self.gama - ((self.s_ / (dis_gap+1e-6)) ** 2))
        # 对加速度进行约束
        a_idm = np.clip(a_idm, -self.a_bound, 1e7)
        return a_idm

    def deside_rotation(self, state):
        return np.zeros(state.shape[0])

if __name__ == "__main__":
    sut = IDM()
    sut.test_sut()