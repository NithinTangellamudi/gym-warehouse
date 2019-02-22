import pygame
import random
import numpy as np
from orders import Orders
import os

class WarehouseView1D:

    def __init__(self,warehouse_name="Warehouse-Default",warehouse_file_path=None,
                warehouse_size=(16,600), screen_size=(600,600)):

        # PyGame configurations
        pygame.init()
        pygame.display.set_caption(maze_name)
        self.clock = pygame.time.Clock()
        self.__game_over = False

        # Load a warehouse
        if warehouse_file_path is None:
            self.__warehouse = Warehouse(warehouse_size=warehouse_size)
        else:
            if not os.path.exists(maze_file_path):
                dir_path = os.path.dirname(os.path.abspath(__file__))
                rel_path = os.path.join(dir_path, "warehouse_samples", warehouse_file_path)
                if os.path.exists(rel_path):
                    warehouse_file_path = rel_path
                else:
                    raise FileExistsError("Cannot find %s." % warehouse_file_path)
            self.__warehouse = Warehouse(warehouse_cells=Warehouse.load_warehouse(
            warehouse_file_path))

        # Make Orders object
        self.__orders = Orders()


        self.warehouse_size = self.__warehouse.warehouse_size

        # to show the right and bottom border
        self.screen = pygame.display.set_mode(screen_size)
        self.__screen_size = tuple(map(sum,zip(screen_size,(-1,-1)))

        # create starting point, and charge station
        self.__entrance = np.array(8,0).astype(dtype=int)

        # create robot
        self.__robot = self.entrance

        # create backgound
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255))

        # create a layer for the warehouse
        self.warehouse_layer = pygame.Surgace(self.screen.get_size()).convert_alpha()
        self.warehouse_layer.fill((0,0,0,0,))

        # ... draw warehouse, robot, entrance
        self.__draw_warehouse()
        self.__draw_robot()
        self.__draw_entrance()
        self.__draw_orders()



    def update(self,mode="human"):
        try:
            img_output = self.__view_update(mode)
            self.__controller_update()
        except Exception as e:
            self.__game_over = True
            self.quit_game()
            raise e
        else:
            return img_output

    def quit_game(self):
        try:
            self.__game_over = True
            pygame.display.quit()
            pygame.quit()
        except Exception:
            pass

    def move_robot(self,dir):
        if dir not in self.__warehouse.COMPASS.keys():
            raise ValueError("dir cannot be %s. The only valid dirs are %s."
                             % (str(dir), str(self.__warehouse.COMPASS.keys())))

        if self.__warehouse.is_open(self.__robot,dir):

            # update the drawing
            self.__draw_robot(transparancy=0)

            # move the robot
            self.__robot += np.array(self.__warehouse.COMPASS[dir

            # MAKE WAY TO 'PICK UP' OBJECT

            self.__draw_robot(transparancy=255)

    def get_orders(self):
        # Get orders randomly

        self.__orders = newOrders


    def reset_robot(self):
        self.__draw_robot(transparancy=0)
        self.__robot = self.__entrance
        self.__draw_robot(transparancy=255)

    def __controller_update(self):
        if not self.__game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__game_over = True
                    self.quit_game()

    def __view_update(self,mode="human"):
        if not self.__game_over:
            # update the robot's position
            self.__draw_entrance()
            self.__draw_robot()
            self.__draw_orders()

            # update the screen
            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.warehouse_layer,(0,0))

            if mode == "human":
                pygame.display.flip()

            return np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface())))

    def __draw_warehouse(self):

        line_colour = (0,0,0,225)

        # draw horizontal lines
        for y in range(self.warehouse.WAREHOUSE_H + 1):
            pygame.draw.line(self.warehouse_layer,linecolour,(0,y*self.CELL_H),
            (self.SCREEN_W,y*self.CELL_H))

        # drawing the vertical lines
        for x in range(self.warehouse.WAREHOUSE_W + 1):
            pygame.draw.line(self.warehouse_layer, line_colour, (x * self.CELL_W, 0),
                             (x * self.CELL_W, self.SCREEN_H))

     def __draw_robot(self, colout=(0,0,150),transparency=255):
         x = int(self.__robot[0]*self.CELL_W + self.CELL_W * 0.5 + 0.5)
         y = int(self.))robot[1] * self.CELL_H + self.CELL_H * 0.5 + 0.5)
         r = int(min(self.CELL_W, self.CELL_H)/5 + 0.5)

         pygame.draw.circle(self.maze_layer,colour + (transparency,), (x,y), r)

    def __draw_entrance(self,colour=(0,0,150),transparancy = 235):
        self.__colour_cell(self.entrance,colour=colour,transparency=transparency)


    def __draw_orders(self, transparency=160):
        # FILL IN


class Warehouse:

    COMPASS = {
        "IN":(0,1),
        "OUT":(0,-1),
        "LEFT":(-1,0),
        "RIGHT":(1,0)
    }
