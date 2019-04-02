import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
from gym_warehouse.envs.warehouse_view import WarehouseView2D

class WarehouseEnv(gym.Env):
    metadata = {'render.modes':['human','rgb_array']}

    ACTION=["IN","OUT","LEFT","RIGHT"]

    def __init__(self,warehouse_file=None,warehouse_size=None):
        self.viewer = None

        if warehouse_file:
            self.warehouse_view = WarehouseView2D(warehouse_name="OpenAI Gym - Warehouse (%s)"%warehouse_file,
            warehouse_file_path=warehouse_file, screen_size=(640,640))

        elif warehouse_size:
            self.warehouse_view = WarehouseView2D(warehouse_name="OpenAI Gym - Warehouse (%d x %d)"%warehouse_size,
            warehouse_size=warehouse_size, screen_size=(640,640))
        else:
            # warehouse_size=(4,10)
            self.warehouse_view = WarehouseView2D(warehouse_name="OpenAI Gym - Default Warehouse (%d x %d)"%(16,600),
            screen_size=(640,640))
            # raise AttributeError("One must supply either a warehouse_file path (str) or the warehouse_size (tuple of length 2)")

        self.warehouse_size = self.warehouse_view.warehouse_size

        # forward or backward in each dimension, pickup and dropoff are automatic
        self.action_space = spaces.Discrete(2*len(self.warehouse_size))

        # observation is the x,y coordinate of the grid
        low = np.zeros(len(self.warehouse_size),dtype=int)
        high = np.array(self.warehouse_size,dtype=int) - np.ones(len(self.warehouse_size),dtype=int)
        self.observation_space = spaces.Box(low,high)

        # initial condition
        self.state = None
        self.steps_beyond_done = None

        # simulation related variables
        self._seed()
        self.reset()

        # initialize relevant attribtes
        self._configure()

    def __del__(self):
        self.warehouse_view.quit_game()

    def _configure(self,display=None):
        self.display = display

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self,action):
        if isinstance(action,int):
            print("ACTION IS: ", action)
            self.warehouse_view.move_robot(self.ACTION[action])
        else:
            self.warehouse_view.move_robot(action)

        self.warehouse_view.get_order()

        if self.warehouse_view.Orders.on_order(self.warehouse_view.robot[0],self.warehouse_view.robot[1]):
            reward = 1
            done = False

        elif np.array_equal(self.warehouse_view.robot, self.warehouse_view.entrance):
            if not self.warehouse_view.is_loaded():
                reward = -10
                done = False
            else:
                reward = 2
                done = True
        else:
            reward = -0.1/(self.warehouse_size[0]*self.warehouse_size[1])
            done = False

        self.state = self.warehouse_view.robot
        info ={}

        return self.state, reward, done, info

    def reset(self):
        self.warehouse_view.reset_robot()
        self.state = np.zeros(2)
        self.steps_beyond_done = None
        self.done = False
        self.warehouse_view.Orders.reset()
        return self.state

    def is_game_over(self):
        return self.warehouse_view.game_over

    def render(self,mode='human',close=False):
        if close:
            self.warehouse_view.quit_game()
        return self.warehouse_view.update(mode)

class WarehouseEnvRandomDefault(WarehouseEnv):

    def __init__(self):
        super(WarehouseEnvSampleRandomDefault,self).__init__()

# class WarehouseEnvSample5x5(WarehouseEnv):
#     def __init__(self):
#         super(WarehouseEnvSample5x5,self).__init__()
