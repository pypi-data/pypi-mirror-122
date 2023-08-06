#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import lib
import sys
sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from sut.sut_base import sutBase
import numpy as np
from sut.idm import IDM
import math
import pandas as pd

class CP(sutBase):
    def __init__(self, L=4,a_bound=5.0, exv=21.72, t=1.2, a=2.22, b=2.4, gama=4, s0=1.0, s1=2.0):
        self.idm = IDM(a_bound,exv,t,a,b,gama,s0,s1)
        self.pind = 0
        self.k = 0.1  # 前视距离系数
        self.Lfc = 4  # 前视距离
        # dt = 0.1  # 时间间隔，单位：s
        self.L = L  # 车辆轴距，单位：m

    def deside_acc(self, state):
        a_idm = self.idm.deside_acc(state)
        return a_idm

    def deside_rotation(self, state, curve=None):
        if curve is None:
            delta = np.zeros(state.shape[0])
        else:    
            x0 = state[:,0,0]
            y0 = state[:,0,1]
            v0 = state[:,0,2]
            dir0 = state[:,0,3]
            cx = curve[:,:,0]
            cy = curve[:,:,1]
            ind = self.calc_target_index(x0, y0, v0,curve)

            tx = cx[range(curve.shape[0]),ind]
            ty = cy[range(curve.shape[0]),ind]
            alpha = np.arctan2(ty - y0, tx - x0) - dir0
            
            alpha[v0<0] = np.pi - alpha[v0<0]

            Lf = self.k * v0 + self.Lfc

            delta = np.arctan2(2.0 * self.L * np.sin(alpha) / Lf, 1.0)

        return delta

    def calc_target_index(self,x0, y0, v0,curve):
        # 搜索最临近的路点
        cx = curve[:,:,0]
        cy = curve[:,:,1]
        dx = cx-x0.reshape(-1,1)
        dy = cy-y0.reshape(-1,1)
        ind = np.argmin(np.sqrt(dx**2+dy**2),axis=1)
        L = np.zeros(cx.shape[0])
        Lf = self.k * v0 +self.Lfc
        ind_final = ind.copy()
        while (L < Lf).sum() > 0:
            ind = np.clip(ind,0,cx.shape[1]-2)
            dx = cx[range(cx.shape[0]),ind+1] - cx[range(cx.shape[0]),ind]
            dy = cy[range(cx.shape[0]),ind+1] - cy[range(cx.shape[0]),ind]
            L += np.sqrt(dx**2 + dy**2)
            ind += 1
            ind_final[L>Lf] = ind[L>Lf].copy()
            
        return ind_final
    
    def test_sut(self,curve):
        state = np.full([2, self.state_shape[0], self.state_shape[1]], np.nan)
        state[0, 0, :] = [0, 0, 10, 0, 4.975, 1.875]
        state[0, 1, :] = [10, 0, 5, 0, 4.975, 1.875]
        state[1, 0, :] = [0, 0, 10, 0, 4.975, 1.875]
        state[1, 1, :] = [5, 0, 20, 0, 4.975, 1.875]
        print(self.deside_all(state,curve))

if __name__ == "__main__":
    sut = CP()
    
    def BezierCurve(end_py, start_px=0, start_py=0, end_px=15, start_heading=0, end_heading=0):
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

        t = np.linspace(0, 1, num=int(20))
        x1 = start_px * 2.0 / 3 + end_px * 1.0 / 3  # vector (sample.shape,1)
        x2 = start_px * 1.0 / 3 + end_px * 2.0 / 3  # vector (sample.shape,1)
        y1 = start_py * 2.0 / 3 + end_py * 1.0 / 3  # vector (sample.shape,1)
        y2 = start_py * 1.0 / 3 + end_py * 2.0 / \
            3  # 三等分点 # vector (sample.shape,1)
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
    
    def get_curve(car1_DistoStart,r):
        horizontal_x = np.linspace(0, car1_DistoStart, 100).T  # n*100
        horizontal_y = np.zeros(horizontal_x.shape)  # n *100
        circle_x = np.linspace(0, r, 100).T
        circle_y = -np.sqrt(r.reshape(-1, 1)**2-circle_x**2)  # 下半圆
        circle_x += car1_DistoStart.reshape(-1, 1)
        circle_y += r.reshape(-1, 1)  # 调整圆心坐标
        vertical_y = np.linspace(0, np.full(r.shape, 50), 100).T
        vertical_x = np.zeros(vertical_y.shape)
        vertical_y += r.reshape(-1, 1)
        vertical_x += car1_DistoStart.reshape(-1, 1)+r.reshape(-1, 1)
        curve_x = np.concatenate((horizontal_x, circle_x, vertical_x), axis=1)
        curve_y = np.concatenate((horizontal_y, circle_y, vertical_y), axis=1)
        curve = np.concatenate(
            (curve_x.reshape(-1, curve_x.shape[1], 1), curve_y.reshape(-1, curve_x.shape[1], 1)), axis=2)
        return curve
    
    # 贝塞尔曲线
    dis = np.array([3.5,3])
    r = np.array([4,5])
    dis1_y_frame = pd.DataFrame(-dis)
    curve = np.array(list(map(BezierCurve, dis1_y_frame[0])))
    curve = curve.reshape(dis.shape[0], -1, 2)
    print(curve.shape)
    
    # 交叉口曲线 
    dis = np.array([3.5,3])
    r = np.array([4,5])
    curve = get_curve(dis,r)
    print(curve.shape)

    sut.test_sut(curve)