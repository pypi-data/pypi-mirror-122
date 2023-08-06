#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/29 19:36
# @Author  : Zhou Huajun
# @File    : test_base_data.py
# @Contact : 17601244133@163.com
# @From    : Tongji University

import pandas as pd
import numpy as np

class testBaseData:
    def __init__(self,path="testedScenario.csv",name=['Speed_y','dif_speed','dis']):
        self.data = pd.read_csv(path)
        self.scenario_shape = self.data.shape[1]-1
        self.name = name
        print(self.data.shape)
    def test(self,sample,sut=None,metric=None):
        sample = np.array(sample).reshape(-1,3)
        sample_frame = pd.DataFrame(sample)
        sample_frame.columns = self.name
        sample_frame = sample_frame.merge(self.data,how='left')
        return np.array(sample_frame['result'])

class CarFollowing(testBaseData):
    scenario_shape = 3

if __name__ == "__main__":
    sut = testBaseData("data/res_vtd_car_following.csv")
    res = sut.test([[0,10,5],[3,-15,7]])
    print(res)