#######################################################################
#  This file contains a class acting as a wrapper for the Unity ML    #
#  environment. It allows the modular code developped by Shangtong    #
#  Zhang(zhangshangtong.cpp@gmail.com) to interface with Unity instead#
#  of an open ai gym environment.                                     #
#                                                                     #
#  File implemented for the RL Udacity nanodegree in the context      #
#  of the continuous control project (p2)                             #
#######################################################################

import gym
from gym import spaces
from unityagents import UnityEnvironment
import numpy as np

class Unity():
	# init function building the wrapper and creating the environment
    def __init__(self):
		# environment created using Unity function. Only on environment can be executed
		# on the machine.
        self.env = UnityEnvironment(file_name='./Reacher_Windows_x86_64/Reacher.exe')
        brain_name = self.env.brain_names[0]
		# by default the environment is set in training. For evaluation it will
        # need to be set to false before launching the episode
        env_info = self.env.reset(train_mode=True)[brain_name] 
        # get the state to define state dims
        state = env_info.vector_observations[0]
        brain = self.env.brains[brain_name]	
		# attribute statedim created to interface with Config class eval_env
        self.state_dim = len(state)
        self.observation_space = env_info.vector_observations[0]
		# attribute actiondim created to interface with Config class eval_env
        self.action_dim = brain.vector_action_space_size
		# define action space
        self.action_space = spaces.Box(low=-float("inf"), high=float("inf"), shape=(4,))
        # open ai attribute recreated here
        self.name ='ContinuousControl'

	#seed function existing in the Openai Gym environment
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

	#wrapper for step function compatible with OpenAI gym format
    def step(self,action):
		# input is an action
		# returns next state, reward, done , info
		# get default brain nam
        brain_name = self.env.brain_names[0]
        env_info = self.env.step(action)[brain_name]
		# get next state, reward and done from env_info
        next_state = env_info.vector_observations[0]
        reward = env_info.rewards[0]
        done = env_info.local_done[0]
		# set info to empty text
        info = ''
        return next_state, reward, done, info

	# reset function used by agent via a call to task reset
    def reset(self):
		# no param for input
		# returns states after a reset
        brain_name = self.env.brain_names[0]
        env_info = self.env.reset(train_mode=True)[brain_name] 
        return env_info.vector_observations[0]
	
	# close unity environment
    def close(self):
        self.env.close()

class Unity20(Unity):
	#Constructor for 20 agent slightly different:
	# new environment
	# returned observation is a vector of 20 observation spaces
    def __init__(self):
		# environment created using Unity function. Only on environment can be executed
        # on the machine. Use Multi agent environment
        self.env = UnityEnvironment(file_name='./Reacher_Windows_x86_64_20/Reacher.exe')
		#only one brain to interact with 20 agents
        brain_name = self.env.brain_names[0]
		# by default the environment is set in training. For evaluation it will
        # need to be set to false before launching the episode
        env_info = self.env.reset(train_mode=True)[brain_name] 
		# get the 20 states of the 20 agents
        states = env_info.vector_observations
        brain = self.env.brains[brain_name]	
		# all observation space are similar. Define dimension base on one agent		
        self.state_dim = states.shape[1]
		# same applies for action space. 
        self.action_dim = brain.vector_action_space_size
        self.action_space = spaces.Box(low=-float("inf"), high=float("inf"), shape=(4,))
        self.observation_space = env_info.vector_observations[0]
        self.name ='ContinuousControl'
        #self.seed()

	#wrapper for step function compatible with OpenAI gym format
    def step(self,actions):
		# input param is a vector containing 20 actions of dimension action_dim (4)
        brain_name = self.env.brain_names[0]
		# step the unity environment for 20 agents
        env_info = self.env.step(actions)[brain_name] 
		# get vector of all 20 observations
        next_states = env_info.vector_observations         
		# get reward (for each agent)
        rewards = env_info.rewards                         
		# see if episode finished
        dones = env_info.local_done   
		# dummy values
        infos = np.zeros(20)							
        return next_states, rewards, dones, infos

    def reset(self):
		# no param for input
		# returns states after a reset
        brain_name = self.env.brain_names[0]
        env_info = self.env.reset(train_mode=True)[brain_name] 
		# return all states for 20 agents 
        return env_info.vector_observations



