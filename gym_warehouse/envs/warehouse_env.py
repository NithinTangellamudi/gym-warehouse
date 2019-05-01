import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
from gym_warehouse.envs.warehouse_view import WarehouseView2D
import copy
import math

class WarehouseEnv(gym.Env):
    metadata = {'render.modes':['human','rgb_array']}

    ACTION=["STAY","IN","OUT","LEFT","RIGHT"]

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
        self.action_space = spaces.Discrete(25)
        # self.action_space = spaces.MultiDiscrete([5,5])

        # observation is the x,y coordinate of the grid
        # low = np.zeros(len(self.warehouse_size),dtype=int)
        # high = np.array(self.warehouse_size,dtype=int) - np.ones(len(self.warehouse_size),dtype=int)

        # self.observation_space = spaces.Box(low,high,dtype=np.float32)
        self.observation_space = spaces.Box(low=-2.0,high=2.0,shape=(5,10),dtype=np.float32)

        # initial condition
        self.state = None
        self.steps_beyond_done = None
        self.done = False
        self.orders_fulfilled = [0,0]
        self.steps = 0
        self.all_rewards = 0
        self.distance = [0,0]
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

        # action will be 0 through 24 ... need to make that translate to [0,0]-type action

        input_action = copy.deepcopy(action)


        action = [0,0]
        action[0] = int(input_action/5)
        action[1] = input_action%5

        self.steps+=1

        old_position_x_0 = self.warehouse_view.robot[0][0]
        old_position_y_0 = self.warehouse_view.robot[0][1]
        old_position_x_1 = self.warehouse_view.robot[1][0]
        old_position_y_1 = self.warehouse_view.robot[1][1]



        robot_0_value = -1.0
        robot_1_value = -1.0

        # if isinstance(action,int):
        # print("ACTION IS: ", action)
        # if isinstance(action,(list,tuple,np.ndarray)):
        #     # print("ACTION IS: ", action)

        self.warehouse_view.get_order()

        # self.warehouse_view.move_robot(self.ACTION[action])
        if action[0] is not 0:
            self.distance[0]+=1
        if action[1] is not 0:
            self.distance[1]+=1


        old_load = self.warehouse_view.move_robot(action,self.ACTION)
        # print("Old Load: ",old_load)
        # print("Order Array: ",self.warehouse_view.Orders.get_order_arr())


        old_value_0 = 0.0
        if self.warehouse_view.Orders.get_order_arr()[old_position_x_0][old_position_y_0] == 1.0 and old_load[0]:
            old_value_0 = 1.0
        old_value_1 = 0.0
        if self.warehouse_view.Orders.get_order_arr()[old_position_x_1][old_position_y_1] == 1.0 and old_load[1]:
            old_value_1 = 1.0
        # else:
        #     self.warehouse_view.move_robot(action)



        reward = [0,0]

        # check if robot is picking up an order

# Robot 1
        # If newly is_loaded

        if self.warehouse_view.is_loaded()[0]:
            # reward[0] += math.sqrt(3 - math.sqrt((abs(self.warehouse_view.robot[0][0]-self.warehouse_view.entrance[0][0]))+(abs(self.warehouse_view.robot[0][1]-self.warehouse_view.entrance[0][1]))))
            robot_0_value = 2.0
            if not old_load[0]:
                reward[0]+=1

        if np.array_equal(self.warehouse_view.robot[0], self.warehouse_view.entrance[0]) or np.array_equal(self.warehouse_view.robot[0], self.warehouse_view.entrance[1]):
            if not self.warehouse_view.is_loaded()[0]:
                # sitting at base/visiting base without order
                # reward[0] += 0.25
                pass
            else:
                # correct dropoff
                reward[0] += 1
                # reward[0] -= math.sqrt(0.01*abs(self.orders_fulfilled[0]-self.orders_fulfilled[1]))
                self.warehouse_view.dropoff(0)
                robot_0_value = -1.0
                self.orders_fulfilled[0] +=1
                # reward[0] -= math.sqrt(0.01*abs(self.orders_fulfilled[0]-self.orders_fulfilled[1]))

        if self.warehouse_view.Orders.on_order(self.warehouse_view.robot[0][0],self.warehouse_view.robot[0][1]) and old_load[0]:
            robot_0_value = -2.0

        reward[0] -= 0.01

# Robot 2
        if self.warehouse_view.is_loaded()[1]:
            # reward[0] += math.sqrt(3 - math.sqrt((abs(self.warehouse_view.robot[0][0]-self.warehouse_view.entrance[0][0]))+(abs(self.warehouse_view.robot[0][1]-self.warehouse_view.entrance[0][1]))))
            robot_1_value = 2.0
            if not old_load[1]:
                reward[1]+=1

        if np.array_equal(self.warehouse_view.robot[1], self.warehouse_view.entrance[0]) or np.array_equal(self.warehouse_view.robot[1], self.warehouse_view.entrance[1]):
            if not self.warehouse_view.is_loaded()[1]:
                # sitting at base/visiting base without order
                # reward[1] += 0.25
                pass
            else:
                # correct dropoff
                reward[1] += 1
                # reward[0] -= math.sqrt(0.01*abs(self.orders_fulfilled[0]-self.orders_fulfilled[1]))
                self.warehouse_view.dropoff(1)
                robot_1_value = -1.0
                self.orders_fulfilled[1] +=1
                self.warehouse_view.dropoff(1)
                # reward[1]-= math.sqrt(0.01*abs(self.orders_fulfilled[0]-self.orders_fulfilled[1]))

        if self.warehouse_view.Orders.on_order(self.warehouse_view.robot[1][0],self.warehouse_view.robot[1][1]) and old_load[1]:
            robot_1_value = -2.0

        reward[1] -= 0.01

        # reward[0]=self.get_reward_1(0)
        # reward[1]=self.get_reward_1(1)
        # print("Reward: ",reward)




        self.all_rewards += reward[0]+reward[1]

        if self.steps>= 64800:
            self.done = True
        # if self.steps > 1000 and self.all_rewards < 0.0:
        #     self.done = True


        # print("New Load: ",self.warehouse_view.is_loaded())

        self.state = copy.deepcopy(self.warehouse_view.Orders.get_order_arr())
        self.state[old_position_x_0][old_position_y_0] = old_value_0
        self.state[old_position_x_1][old_position_y_1] = old_value_1
        self.state[self.warehouse_view.robot[0][0]][self.warehouse_view.robot[0][1]] = robot_0_value
        self.state[self.warehouse_view.robot[1][0]][self.warehouse_view.robot[1][1]] = robot_1_value
        info = {}
        # info = self.warehouse_view.update("")
        info = {"distance":self.distance,"orders":self.orders_fulfilled}

        # print("Entrance: ",self.warehouse_view.entrance)
        # print("Robot: ",self.warehouse_view.robot)
        # print("Number of Orders Fulfilled: ",self.order)
        # print("Reward: ",reward)
        # print("Self.is_loaded : ",self.warehouse_view.is_loaded())

        return self.state, reward, self.done, info

    def reset(self):
        # print("Number of Orders Fulfilled: ",self.orders_fulfilled)
        self.warehouse_view.reset_robot()
        self.warehouse_view.Orders.reset()
        self.state = copy.deepcopy(self.warehouse_view.Orders.get_order_arr())
        self.state[self.warehouse_view.entrance[0][0]][self.warehouse_view.entrance[0][1]] = -1
        self.state[self.warehouse_view.entrance[1][0]][self.warehouse_view.entrance[1][1]] = -1
        self.steps_beyond_done = None
        self.done = False
        self.all_rewards = 0
        self.steps = 0
        self.distance = [0,0]
        self.orders_fulfilled = [0,0]
        return self.state

    def is_game_over(self):
        return self.warehouse_view.game_over

    def render(self,mode='human',close=False):
        if close:
            self.warehouse_view.quit_game()
        return self.warehouse_view.update(mode)

    def get_num_orders_in_system(self):
        return self.warehouse_view.Orders.num_orders


    def get_reward_1(self,robot_number):
        if robot_number==0:
            other_robot=1
        else:
            other_robot=0
        return self.orders_fulfilled[robot_number] - abs(self.orders_fulfilled[robot_number]-self.orders_fulfilled[other_robot]) - abs(self.distance[robot_number]-self.distance[other_robot])

    def get_reward_2(self,robot_number):
        if robot_number==0:
            other_robot=1
        else:
            other_robot=0
        return self.orders_fulfilled[robot_number] - (self.orders_fulfilled[robot_number]-self.orders_fulfilled[other_robot])**2 - (self.distance[robot_number]-self.distance[other_robot])**2

    def get_reward_3(self,robot_number):
        if robot_number==0:
            other_robot=1
        else:
            other_robot=0
        return self.orders_fulfilled[robot_number] - (self.orders_fulfilled[robot_number]-self.orders_fulfilled[other_robot])**2 - (self.distance[robot_number]-self.distance[other_robot])**2



class WarehouseEnvRandomDefault(WarehouseEnv):

    def __init__(self):
        super(WarehouseEnvSampleRandomDefault,self).__init__()

# class WarehouseEnvSample5x5(WarehouseEnv):
#     def __init__(self):
#         super(WarehouseEnvSample5x5,self).__init__()
