#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import lib
from abc import abstractmethod, ABCMeta
import numpy as np


class sutBase(metaclass=ABCMeta):
    state_shape = (9, 6)
    trainable = False
    @abstractmethod
    def deside_acc(self, state): pass
    @abstractmethod
    def deside_rotation(self, state): pass

    def deside_all(self, state, curve = None):
        state = state.reshape(-1, self.state_shape[0], self.state_shape[1])
        acc = self.deside_acc(state)
        if curve is None:
            rot = self.deside_rotation(state)
        else:
            rot = self.deside_rotation(state,curve)
        return acc, rot

    def test_sut(self,curve=None):
        state = np.arange(108).reshape(-1,9,6)
        if curve is None:
            print(self.deside_all(state))
        else:
            print(self.deside_all(state,curve))   