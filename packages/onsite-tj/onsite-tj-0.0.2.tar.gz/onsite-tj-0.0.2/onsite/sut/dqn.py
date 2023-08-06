# -*- coding: utf-8 -*-
import random
import numpy as np
import sys
import os
from collections import deque
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model,load_model
from tensorflow.keras.optimizers import Adam
from tensorflow import reduce_mean

sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from sut.sut_base import sutBase


class DQN(sutBase):
    def __init__(self,trainable=True,dueling=False,rot_sut=None,a_bound=5,loadpath=None,savepath=None,batch=64):
        self.trainable = trainable
        self.dueling = dueling
        self.input_shape = 14
        # action_space
        self.action_num = 5
        self.action_space = np.linspace(-a_bound,a_bound,self.action_num)
        print("action_space:",self.action_space)
        # build net
        if loadpath is not None:
            self.model = load_model(loadpath)
            self.target_model = load_model(loadpath)
        else:
            self.model = self.build_model()
            self.target_model = self.build_model()
            self.update_target_model()
        self.l_r = 1e-4
        self.model.compile(loss='mse', optimizer=Adam(self.l_r))

        self.savepath = savepath
        self.batch = batch
        # 经验池
        self.memory_buffer = deque(maxlen=10000)
        # Q_value的discount rate，以便计算未来reward的折扣回报
        self.gamma = 0.9
        # 贪婪选择法的随机选择行为的程度
        if trainable:
            self.epsilon = 1.0
        else:
            self.epsilon = 0
        # 上述参数的衰减率
        self.epsilon_decay = 0.995
        # 最小随机探索的概率
        self.epsilon_min = 0.1
        self.rot_sut = rot_sut
        self.count = 0
        self.q_avg = np.zeros([self.action_num])
        self.q_count = 0
        self.loss_rec = 0
        self.loss_count = 0
        self.reward_rec = 0

    def build_model(self):
        """基本网络结构.
        """
        inputs = Input(shape=(self.input_shape,))
        x = Dense(128, activation='relu')(inputs)
        # x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(32, activation='relu')(x)
        if self.dueling:
            value_s = Dense(1, activation='linear')(x)
            value_a = Dense(self.action_num, activation='linear')(x)
            x = value_s + value_a-reduce_mean(value_a,axis=1,keepdims=True)
        else:
            x = Dense(self.action_num, activation='linear')(x)

        model = Model(inputs=inputs, outputs=x)

        return model

    def update_target_model(self):
        """更新target_model
        """
        self.target_model.set_weights(self.model.get_weights())

    def egreedy_action(self, state):
        """ε-greedy选择action

        Arguments:
            state: 状态

        Returns:
            action: 动作
        """
        if np.random.rand() <= self.epsilon:
             return np.random.choice(self.action_num,state.shape[0])
        else:
            q_values = self.model.predict(state)
            # print(q_values)
            self.q_avg += q_values.sum(axis=0)
            self.q_count += 1
            return np.argmax(q_values,axis=1)

    def remember(self, state, action, reward, next_state, done):
        """向经验池添加数据

        Arguments:
            state: 状态
            action: 动作
            reward: 回报
            next_state: 下一个状态
            done: 游戏结束标志
        """
        for item in zip(state, action, reward, next_state, done):
            self.memory_buffer.append(item)

    def update_epsilon(self):
        """更新epsilon
        """
        if self.epsilon >= self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def process_batch(self, batch):
        """batch数据处理

        Arguments:
            batch: batch size

        Returns:
            X: states
            y: [Q_value1, Q_value2]
        """
         # 从经验池中随机采样一个batch
        data = random.sample(self.memory_buffer, batch)
        # 生成Q_target。
        states = np.array([d[0] for d in data]).reshape(batch,-1)
        next_states = np.array([d[3] for d in data]).reshape(batch,-1)
        y = self.model.predict(states)
        q_next = self.target_model.predict(next_states)
        q_eval = self.model.predict(next_states)
        for i, (_, action, reward, _, done) in enumerate(data):
            target = reward
            if not done:
                target += self.gamma * q_next[i,np.argmax(q_eval[i])]
            y[i][action] = target

        return states, y
    
    def deside_acc(self,state):
        state = self.preprocess_state(state)
        action = self.egreedy_action(state)
        return self.action_space[action]
    
    def deside_rotation(self,state, curve = None):
        if self.rot_sut is None:
            rot = np.zeros(state.shape[0])
        elif curve is None:
            rot = self.rot_sut.deside_rotation(state)
        else:
            rot = self.rot_sut.deside_rotation(state,curve)
        return rot

    def preprocess_state(self,state):
        state  = state.copy().reshape(-1,9,6)
        state_ego = state[:,0,:].copy() # 存储本车信息
        state = state[:,:,:-3] # 舍弃车长车宽转向角信息
        # state[:,:,:-1] -= state_ego[:,:-3].repeat(state.shape[1],axis=0).reshape(state.shape[0],state.shape[1],-1)
        # state[:,0,:] = state_ego[:,:-2].copy()
        state -= state_ego[:,:-3].repeat(state.shape[1],axis=0).reshape(state.shape[0],state.shape[1],-1)
        state[:,0,:] = state_ego[:,:-3].copy()
        nan = np.isnan(state).sum(axis=2)>0
        state[:,:,2][nan] = 0
        # 转向角信息
        # state[:,:,3][nan] = 0

        # i = [2,5,8]
        for i in [2,5,8]:
            state[nan[:,i],i,0] = -20
        for i in [1,3,4,6,7]:
            state[:,i,0][nan[:,i]] = 20
        for i in [1,2]:
            state[:,i,1][nan[:,i]] = 0
        for i in [6,7,8]:
            state[:,i,1][nan[:,i]] = 5
        for i in [3,4,5]:
            state[:,i,1][nan[:,i]] = -5
        # 标准化
        state[:,:,0] /= 20
        state[:,:,1] /= 5
        state[:,:,2] /= 20
        # reshape阶段
        vehicle_list = [0,1,2,4,7]
        state = state[:,vehicle_list,:].reshape(-1,15)
        # state = state.reshape(-1,27)

        # 最终处理
        # state = state[:,2:]
        state = state[:,1:]
        state[:,0] = state_ego[:,3]
        assert(state.shape[1] == self.input_shape)
        return state
        
    def train(self,state,new_state,action,reward,done):
        action,rot = action
        action_ind = np.argmin(np.abs(self.action_space.repeat(action.shape[0]).reshape(-1,action.shape[0]).T - action.reshape(-1,1)),axis=1)
        # print("state",state)
        # print("new_state",new_state)
        state = self.preprocess_state(state)
        new_state = self.preprocess_state(new_state)

        # print("ego_state",state[:,:2])
        # print("state",state)
        # print("new_state",new_state)
        # print("reward",reward)
        # print("done",done)
        # print("action",action)
        # os.system("pause")
        self.remember(state, action_ind, reward, new_state, done)
        if len(self.memory_buffer) > self.batch:
            # 训练
            X, y = self.process_batch(self.batch)
            loss = self.model.train_on_batch(X, y)
            self.loss_rec += loss
            self.reward_rec += reward[0]
            self.loss_count += 1
            self.count += 1
            # 减小egreedy的epsilon参数。
            self.update_epsilon()

            # 固定次数更新target_model
            if self.count != 0 and self.count % 100 == 0:
                self.update_target_model()
            # 固定次数保存模型
            if self.savepath != None and self.count != 0 and self.count % 200 == 0:
                self.model.save(self.savepath)
            # print(loss)

if __name__ == "__main__":
    sut = DQN(dueling=True)
    sut.model.summary()
    state = np.arange(108).reshape(2,9,6)
    state = sut.preprocess_state(state)
    sut.epsilon = 0
    # print(state)
    # print()
    # print(sut.deside_all(state))
    print(sut.egreedy_action(state))
    print(sut.memory_buffer)