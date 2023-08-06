#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import lib
import sys
sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from sut.sut_base import sutBase
import numpy as np


class IDM(sutBase):
    def __init__(self, a_bound=5.0, exv=21.72, t=1.2, a=2.22, b=2.4, gama=4, s0=1.0, s1=2.0):
        """跟idm模型有关的模型参数，一定要记得调整

        :param a_bound: 本车加速度的下界
        :param exv: 期望速度
        :param t: 反应时间
        :param a: 起步加速度
        :param b: 舒适减速度
        :param gama: 加速度指数
        :param s0: 静止安全距离
        :param s1: 与速度有关的安全距离选择参数
        """
        self._state_shape = 8
        self.a_bound = a_bound
        self.exv = exv
        self.t = t
        self.a = a
        self.b = b
        self.gama = gama
        self.s0 = s0
        self.s1 = s1

    def deside_acc(self, state):
        state = state.reshape(-1, self._state_shape)
        assert(state.shape[1] == self._state_shape)
        # [para.reshape(-1, 1) for para in [,Vd,T,a,b,max_b]
        v, fv, dis,self.exv,self.t,self.a,self.b,self.a_bound = [state[:,i] for i in range(self._state_shape)]
        # 求解本车与前车的期望距离
        s_ = self.s0 + self.s1 * (v / self.exv) ** 0.5 + self.t * v + v * (
            v - fv) / 2 / (self.a * self.b) ** 0.5
        # 求解本车加速度
        a_idm = self.a * (1 - (v / self.exv) ** self.gama - ((s_ / (dis+1e-6)) ** 2))
        # 对加速度进行约束
        a_idm = np.clip(a_idm, -self.a_bound, 1e5)
        return a_idm

    def deside_rotation(self, state):
        state = state.reshape(-1, self._state_shape)
        assert(state.shape[1] == self._state_shape)
        return np.zeros(state.shape[0])

if __name__ == "__main__":
    sut = IDM()
    state = np.array([[1, 2, 3 ,4,5,6,7,1], [2,3,4,5,6,7,8,2]])
    print(sut.deside_acc(state))
    print(sut.deside_rotation(state))
