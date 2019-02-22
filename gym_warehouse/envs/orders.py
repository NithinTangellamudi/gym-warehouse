# File for determining how orders appear in the warehouse

imort numpy as np


class Orders:
    def __init__(self,warehouse_size = (16,600),dist = "Normal",classA=(3,1),
    classB = (1,0.5), classC = (0,0.5), dist="exp",warehouse_order_map_file_path=None,version=1):

        self.__classAmean = classA[0]
        self.__classAstdev = classA[1]
        self.__classBmean = classB[0]
        self.__classBstdev = classB[1]
        self.__classCmean = classC[0]
        self.__classCstdev = classC[1]

        self.__warehouse_size = warehouse_size

        if warehouse_order_map_file_path is None:
            self.__warehouse_order_class_map = make_warehouse_order_class_map(warehouse_size
            ,version)
        else:
            if not os.path.exists(warehouse_order_map_file_path):
                dir_path = os.path.dirname(os.path.abspath(__file__))
                rel_path = os.path.join(dir_path, "order_map_samples", warehouse_order_map_file_path)
                if os.path.exists(rel_path):
                    warehouse_order_map_file_path = rel_path
                else:
                    raise FileExistsError("Cannot find %s." % warehouse_order_map_file_path)
            self.__warehouse_order_class_map = load_warehouse_order_class_map(warehouse_order_map_file_path)




    def make_warehouse_order_class_map(self, warehouse_size,version):
        # randomly assign each spot in the warehouse to a class A.B, or C
        class_map = np.array(warehouse_size,dtype=int)

        for i in range(warehouse_size[0]):
            for j in range(warehouse_size[1]):
                if np.random()< 0.05:
                    class_map(i,j)="A"
                elif np.random()<0.20:
                    class_map(i,j)="B"
                else:
                    class_map(i,j)="C"
        file_name="default"+version
        np.save(file_name,class_map)


    def load_warehouse_order_class_map(self,warehouse_order_map_file_path):
        self.__warehouse_order_class_map = np.load(warehouse_order_map_file_path)



    def new_order(self,dist):
        # Orders come in at specific rates
        # at each time step one new order copmes in

        x = np.random(0,warehouse_size[0])
        y = np.random(0,warehouse_size[1])
        qty = 0

        order_class = self.__warehouse_order_class_map[x][y]

        if dist=="exp":
            if order_class =="C":
                qty = np.random.exponential(self.__classCmean)
            elif order_class =="B":
                qty = np.random.exponential(self.__classBmean)
            if order_class =="A":
                qty = np.random.exponential(self.__classAmean)
        elif fist == "normal":
            if order_class =="C":
                qty = np.random.normal(self.__classCmean,self.__classCstdev)
            elif order_class =="B":
                qty = np.random.normal(self.__classBmean,self.__classBstdev)
            if order_class =="A":
                qty = np.random.normal(self.__classAmean,self.__classAstdev)

        return x,y,qty


    def clear_order(self,x,y):
        self.__orders[x][y] = 0
