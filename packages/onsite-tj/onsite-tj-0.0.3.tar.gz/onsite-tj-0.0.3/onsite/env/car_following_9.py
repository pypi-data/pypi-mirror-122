import sys
sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import numpy as np
# from env.env_base import envBase
from sut.idm_modify import IDM

class CarFollowing():

    def __init__(self):
        self.scenario_shape = 9
        self.car_length = 4.924
        self.sut = IDM()
        print('carFollowing场景，输入参数fv,dif_v,dis,FA,Vd,T,a,b,max_b！')

    def test(self, scenario, sut=None,  plot_key=False, metric = None):
        if sut is None:
            sut = self.sut
        scenario = scenario.reshape(-1, self.scenario_shape)
        assert(scenario.shape[1] == self.scenario_shape)
        if plot_key:
            plt.ion()
        result = np.zeros([scenario.shape[0]])
        [fv, dif_v, dis,FA,Vd,T,alpha,beta,max_b] = [scenario[:,i] for i in range(self.scenario_shape)]
        v = fv - dif_v
        dis = np.clip(dis,0,1e5)
        v = np.clip(v,0,1e5)
        x1 = np.zeros((scenario.shape[0],))
        x2 = dis.copy()
        for i in range(30):
            a = sut.deside_acc(
                np.concatenate(
                    ([para.reshape(-1, 1) for para in [v, fv, np.clip(x2-x1-self.car_length, 0, 1e5),Vd,T,alpha,beta,max_b]]), axis=1
                )
            )
            v = v + a * 0.1
            v = np.clip(v, 0, 1e5)
            fv = fv + FA*0.1
            fv = np.clip(fv, 0, 1e5)
            x1 += v*0.1
            x2 += fv*0.1
            danger_index = ((x2-x1) < self.car_length)
            result[danger_index] = 1
            if plot_key:
                plt.cla()
                plt.xlim(0, 40)
                plt.ylim(-20, 20)
                self.plot_car(0, x1[0], c='k', l=self.car_length, w=1.872)
                self.plot_car(0, x2[0], c='r', l=self.car_length, w=1.872)
                plt.pause(1e-2)
                plt.show()
        return result
    
    @staticmethod
    def plot_car(x, y, direction=0, c='blue', l=3, w=1.8):
        """在matplotlib中绘制小汽车

        :param x:x坐标
        :param y:y坐标
        :param direction:方向角
        :param c:小汽车的颜色
        :param l:小汽车长度
        :param w:小汽车宽度
        """
        plt.ylim(-50, 50)
        plt.xlim(-20, 80)
        ax = plt.subplot(111)
        ax.add_patch(
            patches.Rectangle(
                xy=(y, x),
                width=l,
                height=w,
                angle=direction,
                color=c
            )
        )


if __name__ == "__main__":
    from sut.idm_modify import IDM
    print("start")
    sut = IDM()
    env = carFollowing()
    # 场景参数定义在此处
    test_sample = np.array([
        [4.88619646, -5.51864016, 27.06436162,-1,20,1.2,7,2,3],
        [4.81720291, 0.42054838, 10.26410715,-2,20,6,1.2,2,3],
        [7.92313679, -2.37679344, 15.78525394,-3,20,6,1.2,2,3],
        [5.84214011, 0.72061848, 12.35805587,-4,20,6,1.2,2,3],
        [7.25463418, -0.0982501, 14.04462361,-5,20,6,1.2,2,3],
    ])
    for scenario in test_sample:
        res = env.test(scenario)
        print(res)
    # print(env.test(test_sample, sut))
    # print(env.test(test_sample[2],sut))
