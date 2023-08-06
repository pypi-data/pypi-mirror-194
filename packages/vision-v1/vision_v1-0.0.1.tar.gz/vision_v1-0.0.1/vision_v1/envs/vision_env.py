import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pybullet as p
import pybullet_data
import cv2
import numpy as np
import random
from os.path import normpath, basename
import time

class VisionEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-10)
        p.setRealTimeSimulation(1)

        self.car_location = [0,0,0.3]
        self.balls_location = dict({
            'red'    : [6,0,1.5],
            'blue'   : [0,6,1.5],
            'yellow' : [-6,0,1.5],
            'green'  : [0,-6,1.5]
        })
        self.humanoids_location = dict({
            'red'    : [6,0,1.5],
            'blue'   : [0,6,1.5],
            'yellow' : [-6,0,1.5],
            'green'  : [0,-6,1.5]
        })

        self.load_env()

    def load_env(self):
        orientation = p.getQuaternionFromEuler([0,0,0])  
        p.loadURDF('gym_env/urdf/arena/arena.urdf')
        p.loadURDF('gym_env/urdf/car/car.urdf', self.car_location, orientation)  
        p.loadURDF('gym_env/urdf/ball/ball_red.urdf', self.balls_location["red"], orientation)
        p.loadURDF('gym_env/urdf/ball/ball_blue.urdf', self.balls_location["bule"], orientation)
        p.loadURDF('gym_env/urdf/ball/ball_yellow.urdf', self.balls_location["yellow"], orientation)
        p.loadURDF('gym_env/urdf/ball/ball_green.urdf', self.balls_location["green"], orientation)
        p.loadURDF('gym_env/urdf/humanoid/humanoid_red.urdf', self.humanoids_location["red"], orientation)
        p.loadURDF('gym_env/urdf/humanoid/humanoid_blue.urdf', self.humanoids_location["blue"], orientation)
        p.loadURDF('gym_env/urdf/humanoid/humanoid_yellow.urdf', self.humanoids_location["yellow"], orientation)
        p.loadURDF('gym_env/urdf/humanoid/humanoid_green.urdf', self.humanoids_location["green"], orientation)     