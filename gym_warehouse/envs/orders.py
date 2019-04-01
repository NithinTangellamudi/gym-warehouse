# File for determining how orders appear in the warehouse

import numpy as np
from collections import deque


class Orders:
    def __init__(self,warehouse_size = (16,600),classA=(3,1),
    classB = (1,0.5), classC = (0,0.5), dist="exp",warehouse_order_map_file_path=None,version=1):

        self.__classAmean = classA[0]
        self.__classAstdev = classA[1]
        self.__classBmean = classB[0]
        self.__classBstdev = classB[1]
        self.__classCmean = classC[0]
        self.__classCstdev = classC[1]

        self.__warehouse_size = warehouse_size

        if warehouse_order_map_file_path is None:
            self.__warehouse_order_class_map = self.make_warehouse_order_class_map(warehouse_size)
        else:
            if not os.path.exists(warehouse_order_map_file_path):
                dir_path = os.path.dirname(os.path.abspath(__file__))
                rel_path = os.path.join(dir_path, "order_map_samples", warehouse_order_map_file_path)
                if os.path.exists(rel_path):
                    warehouse_order_map_file_path = rel_path
                else:
                    raise FileExistsError("Cannot find %s." % warehouse_order_map_file_path)
            self.__warehouse_order_class_map = self.load_warehouse_order_class_map(warehouse_order_map_file_path)

        # efficient to store orders in an array accroding to location
        self.__orders = np.zeros(warehouse_size)


    def make_warehouse_order_class_map(self, warehouse_size):
        # randomly assign each spot in the warehouse to a class A.B, or C
        class_map = np.zeros(warehouse_size,dtype=int)

        print("SHAPE OF CLASS MAP: ",class_map.shape)

        for i in range(warehouse_size[0]):
            for j in range(warehouse_size[1]):
                if np.random.random_sample()< 0.05:
                    class_map[i][j]=1
                elif np.random.random_sample()<0.20:
                    class_map[i][j]=2
                else:
                    class_map[i][j]=3
        file_name="default"
        np.save(file_name,class_map)
        return class_map


    def load_warehouse_order_class_map(self,warehouse_order_map_file_path):
        self.__warehouse_order_class_map = np.load(warehouse_order_map_file_path)



    def new_order(self,dist="normal"):
        # Orders come in at specific rates
        # at each time step one new order copmes in

        x = int(self.__warehouse_size[0]*np.random.random_sample())
        y = int(self.__warehouse_size[1]*np.random.random_sample())
        qty = 0

        order_class = self.__warehouse_order_class_map[x][y]

        if dist=="exp":
            if order_class ==3:
                qty = np.random.exponential(self.__classCmean)
            elif order_class ==2:
                qty = np.random.exponential(self.__classBmean)
            if order_class ==1:
                qty = np.random.exponential(self.__classAmean)
        elif dist == "normal":
            if order_class ==3:
                qty = np.random.normal(self.__classCmean,self.__classCstdev)
            elif order_class ==2:
                qty = np.random.normal(self.__classBmean,self.__classBstdev)
            if order_class ==1:
                qty = np.random.normal(self.__classAmean,self.__classAstdev)

        self.__orders[x,y]=self.__orders[x,y]+qty
        return x,y


    def clear_order(self,x,y):
        self.__orders[x][y]=0

    def reset(self):
        self.__orders=np.zeros(self.__warehouse_size)

    def get_order_qty(self,x,y):
        return self.__orders[x][y]

    def on_order(self,x,y):
        if self.__orders[x][y] > 0:
            return True
        return False
