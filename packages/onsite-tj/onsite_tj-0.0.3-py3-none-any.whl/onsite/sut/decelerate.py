#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import sys
sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from sut.sut_base import sutBase


class DC(sutBase):
    def __init__(self, a_bound=5.0):
        """模型参数

        :param a_bound: 本车加速度绝对值的上下界
        """
        self.a_bound = a_bound

    def deside_acc(self, state):
        a = -np.ones(state.shape[0])*self.a_bound
        return a

    def deside_rotation(self, state,curve=None):
        return np.zeros(state.shape[0])


if __name__ == "__main__":
    sut = DC()
    sut.test_sut()
