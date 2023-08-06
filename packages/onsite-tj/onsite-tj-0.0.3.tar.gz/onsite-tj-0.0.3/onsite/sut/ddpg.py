# import wandb
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Lambda, concatenate
from tensorflow.keras.models import Model,load_model

# import gym
import argparse
import numpy as np
import random
from collections import deque
import sys
sys.path.append("\\".join(sys.path[0].split('\\')[:-1]))
from sut.sut_base import sutBase

tf.keras.backend.set_floatx('float64')
# wandb.init(name='DDPG', project="deep-rl-tf2")

parser = argparse.ArgumentParser()
parser.add_argument('--gamma', type=float, default=0.95)
parser.add_argument('--actor_lr', type=float, default=0.00005)
parser.add_argument('--critic_lr', type=float, default=0.0001)
parser.add_argument('--batch_size', type=int, default=1)
parser.add_argument('--tau', type=float, default=0.05)
parser.add_argument('--train_start', type=int, default=100)

args = parser.parse_known_args()[0]

class ReplayBuffer:
    def __init__(self, capacity=20000):
        self.buffer = deque(maxlen=capacity)
    
    def put(self, state, action, reward, next_state, done):
        for item in zip(state, action, reward, next_state, done):
            self.buffer.append(item)
    
    def sample(self):
        sample = random.sample(self.buffer, args.batch_size)
        states, actions, rewards, next_states, done = map(np.asarray, zip(*sample))
        states = np.array(states).reshape(args.batch_size, -1)
        next_states = np.array(next_states).reshape(args.batch_size, -1)
        return states, actions, rewards, next_states, done
    
    def size(self):
        return len(self.buffer)


class Actor:
    def __init__(self, state_dim, action_dim, action_bound):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.action_bound = action_bound
        self.model = self.create_model()
        self.opt = tf.keras.optimizers.Adam(args.actor_lr)

    def create_model(self):
        inputs = Input(shape=(self.state_dim,))
        x = Dense(64, activation='tanh')(inputs)
        x = Dense(32, activation='tanh')(x)
        # x = Dense(32, activation='relu')(x)
        # x = Dense(32, activation='relu')(x)
        x = Dense(self.action_dim, activation='tanh')(x)
        # x =  Lambda(lambda x:x * self.action_bound)(x)
    
        model = Model(inputs=inputs, outputs=x)
        
        return model

    def train(self, states, q_grads):
        with tf.GradientTape() as tape:
            grads = tape.gradient(self.model(states), self.model.trainable_variables, -q_grads)
        self.opt.apply_gradients(zip(grads, self.model.trainable_variables))
    
    def predict(self, state):
        return self.model.predict(state)

    def get_action(self, state):
        state = np.reshape(state, [-1, self.state_dim])
        return self.model.predict(state)


class Critic:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.model = self.create_model()
        self.opt = tf.keras.optimizers.Adam(args.critic_lr)

    def create_model(self):
        state_input = Input((self.state_dim,))
        s1 = Dense(64, activation='relu')(state_input)
        # s1 = Dense(64, activation='relu')(s1)
        # s1 = Dense(64, activation='relu')(s1)
        s2 = Dense(32, activation='relu')(s1)
        action_input = Input((self.action_dim,))
        a1 = Dense(32, activation='relu')(action_input)
        c1 = concatenate([s2, a1], axis=-1)
        c2 = Dense(16, activation='relu')(c1)
        output = Dense(1, activation='linear')(c2)
        return tf.keras.Model([state_input, action_input], output)
    
    def predict(self, inputs):
        return self.model.predict(inputs)
    
    def q_grads(self, states, actions):
        actions = tf.convert_to_tensor(actions)
        with tf.GradientTape() as tape:
            tape.watch(actions)
            q_values = self.model([states, actions])
            q_values = tf.squeeze(q_values)
        return tape.gradient(q_values, actions)

    def compute_loss(self, v_pred, td_targets):
        mse = tf.keras.losses.MeanSquaredError()
        return mse(td_targets, v_pred)

    def train(self, states, actions, td_targets):
        with tf.GradientTape() as tape:
            v_pred = self.model([states, actions], training=True)
            assert v_pred.shape == td_targets.shape
            loss = self.compute_loss(v_pred, tf.stop_gradient(td_targets))
        grads = tape.gradient(loss, self.model.trainable_variables)
        self.opt.apply_gradients(zip(grads, self.model.trainable_variables))
        return loss


class DDPG(sutBase):
    def __init__(self,trainable=True,a_bound=5,rot_sut=None,loadpath=None,savepath=None):
        self.state_dim = 14
        self.input_shape = self.state_dim
        self.action_dim = 1
        self.action_bound = a_bound
        self.bg_noise = 0
        self.buffer = ReplayBuffer()
        self.trainable = trainable
        self.rot_sut = rot_sut
        self.train_count = 0
        self.actor = Actor(self.state_dim, self.action_dim, self.action_bound)
        self.critic = Critic(self.state_dim, self.action_dim)
        if loadpath is not None:
            print(loadpath+"/actor.h5")
            self.actor.model = load_model(loadpath+"/actor.h5")
            self.critic.model = load_model(loadpath+"/critic.h5")
        self.savepath = savepath
        self.target_actor = Actor(self.state_dim, self.action_dim, self.action_bound)
        self.target_critic = Critic(self.state_dim, self.action_dim)

        actor_weights = self.actor.model.get_weights()
        critic_weights = self.critic.model.get_weights()
        self.target_actor.model.set_weights(actor_weights)
        self.target_critic.model.set_weights(critic_weights)
        self.reward_rec = 0
        self.reward_count = 0

    def target_update(self):
        actor_weights = self.actor.model.get_weights()
        t_actor_weights = self.target_actor.model.get_weights()
        critic_weights = self.critic.model.get_weights()
        t_critic_weights = self.target_critic.model.get_weights()

        for i in range(len(actor_weights)):
            t_actor_weights[i] = args.tau * actor_weights[i] + (1 - args.tau) * t_actor_weights[i]

        for i in range(len(critic_weights)):
            t_critic_weights[i] = args.tau * critic_weights[i] + (1 - args.tau) * t_critic_weights[i]
        
        self.target_actor.model.set_weights(t_actor_weights)
        self.target_critic.model.set_weights(t_critic_weights)

    def td_target(self, rewards, q_values, dones):
        targets = np.asarray(q_values)
        for i in range(q_values.shape[0]):
            if dones[i]:
                targets[i] = rewards[i]
            else:
                targets[i] = args.gamma * q_values[i]
        return targets

    def list_to_batch(self, list):
        batch = list[0]
        for elem in list[1:]:
            batch = np.append(batch, elem, axis=0)
        return batch
    
    def ou_noise(self, x, rho=0.15, mu=0, dt=1e-1, sigma=0.2, dim=1):
        return x + rho * (mu-x) * dt + sigma * np.sqrt(dt) * np.random.normal(size=dim)
    
    def replay(self):
        for _ in range(1):
            states, actions, rewards, next_states, dones = self.buffer.sample()
            # print("states:",states)
            # print("new_states:",next_states)
            # print("rewards:",rewards)
            # print("actions",actions)
            # print("dones:",dones)
            target_q_values = self.target_critic.predict([next_states, self.target_actor.predict(next_states)])
            td_targets = self.td_target(rewards, target_q_values, dones)
            
            self.critic.train(states, actions, td_targets)
            
            s_actions = self.actor.predict(states)
            s_grads = self.critic.q_grads(states, s_actions)
            grads = np.array(s_grads).reshape((-1, self.action_dim))
            self.actor.train(states, grads)
            self.target_update()

    def train(self,state,new_state,action,reward,done):
        action,rot = action
        # print("state_p:",state)
        # print("new_state_p:",new_state)
        # print("rewards:",reward)
        # print("actions",action)
        # print("dones:",done)
        action /= self.action_bound
        action = action.reshape(-1,1)
        # print("action_new:",action)
        state = self.preprocess_state(state)
        new_state = self.preprocess_state(new_state)
        # print("states:",state)
        # print("new_states:",new_state)
        self.reward_rec += reward[0]
        self.reward_count += 1
        self.buffer.put(state, action, reward, new_state, done)
        if self.buffer.size() >= args.batch_size and self.buffer.size() >= args.train_start:
            self.replay() 
            self.train_count += 1
            if self.train_count % 200 == 0 and self.train_count != 0:
                self.actor.model.save(self.savepath+"/actor.h5")
                self.critic.model.save(self.savepath+"/critic.h5")

    def deside_acc(self,state):
        state = self.preprocess_state(state)
        action = self.actor.get_action(state)
        action = action*self.action_bound
        if self.trainable:
            noise = self.ou_noise(self.bg_noise, dim=self.action_dim)
            action = np.clip(action + noise*self.action_bound, -self.action_bound, self.action_bound)
            self.bg_noise = noise
            if np.abs(self.bg_noise) >= 1:
                self.bg_noise = 0
        return action.reshape(-1)
        
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


if __name__ == "__main__":
    sut = DDPG()
    sut.actor.model.summary()
    state = np.arange(108).reshape(2,9,6)
    print(state)
    print(sut.preprocess_state(state))
    print(sut.deside_all(state))