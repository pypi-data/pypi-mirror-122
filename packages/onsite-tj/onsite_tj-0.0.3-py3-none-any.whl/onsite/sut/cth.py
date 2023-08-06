#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import sys
sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from sut.sut_base import sutBase


class CTH(sutBase):
    def __init__(self, a_bound=5.0):
        """模型参数

        :param a_bound: 本车加速度绝对值的上下界
        """
        self.a_bound = a_bound
        self.exv = 22

    def deside_acc(self, state):
        v, fv, dis = state[:,0, 2], state[:,1, 2], state[:,1, 0]-state[:,0, 0]
        ind = np.isnan(fv)
        fv[ind] = self.exv
        ind = np.isnan(dis)
        dis[ind] = state[0,0,4]*10
        # 求解本车与前车的期望距离
        a = 1.12*(dis-1.4*v)+1.7*(fv-v)
        a = np.clip(a, -self.a_bound, self.a_bound)

        return a

    def deside_rotation(self, state):
        return np.zeros(state.shape[0])


if __name__ == "__main__":
    sut = CTH()
    sut.test_sut()
