import gym
from gym import spaces
from env import loaddata
from sklearn import preprocessing
import numpy as np
import random
import pandas as import pd
from env.graph import ENVGraph

class FXEnv(gym.Env):

    def __init__(self, pair, spread=0.0,
            initial_balance=100000, look_back=60):

        super(FXEnv, self).__init__()

        pd.options.mode.chained_assignment = None
        
        self.group_by = fdata.DAY
        self.look_back = look_back
        self.initial_balance = initial_balance
        self.spread = spread

        self.year = 2011
        self.maxyear = 2018

        self.action_space = spaces.Discrete(7)
        self.maxaction = 6
        self.observation_space = spaces.Box(low=0, high=1, shape=[self.look_back, 12])
        self.pair = pair
        self.data = loaddata.load_data(self.pair, self.year)
        self.current_day = 0
        self.position_amount = initial_balance * 0.2
        
        self.pos_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
        self.pos_scaler.fit(np.array([[-3], [3]]))
        self.totalDays = len(self.data) // loaddata.DAY
    
    def reset(self):
        