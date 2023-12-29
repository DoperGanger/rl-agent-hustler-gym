import pygame
import numpy as np 
import random

class Env():
    def __init__(self, display, matrix, cat_mode, map_mode):
        self.HEIGHT = matrix.ROWS # y
        self.WIDTH = matrix.COLUMNS # x
        # self.CAT_MODE = cat_mode
        # self.MAP_MODE = map_mode
        self.OBSTACLES = []

        # Pygame setting
        self.DISPLAY = display
        displayWidth, displayHeight = display.get_size()
        displayHeight -= 100  # For info panel
        self.BLOCK_WIDTH = int(displayWidth/self.WIDTH)
        self.BLOCK_HEIGHT = int(displayHeight/self.HEIGHT)

        # Agents
        self.CATCHER = Catcher(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.HUSTLER = Hustler(self.DISPLAY, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.MOVES = {'hustler':100,'catcher':100}

        # GOAL
        self.GOAL = pygame.transform.scale(pygame.image.load('sprites/door.png'),(self.BLOCK_WIDTH, self.BLOCK_HEIGHT))


        # Set Obstacles Postion Array
        def set_obstacles(self, obstacles:np.array): # Used to change the obstacles in the map
            self.OBSTACLES = obstacles

        def render(self, i_episode = -1):

            # Draw Agents
            self.HUSTLER.draw(self.HUSTLER_X, self.HUSTLER_Y)
            self.CATCHER.draw(self.CATCHER_X, self.CATCHER_Y)
            self.DISPLAY.blit(self.GOAL, (self.GOAL_X*self.BLOCK_WIDTH, self.GOAL_Y*self.BLOCK_HEIGHT))

            # Draw Obstacles
            for pos in self.OBSTACLES:
                pygame.draw.rect(self.DISPLAY, (0,0,255), [pos[0]*self.BLOCK_WIDTH, pos[1]*self.BLOCK_HEIGHT, self.BLOCK_WIDTH, self.BLOCK_HEIGHT])

            # Draw Info Panel
            if i_episode>=0:
                self.display_episode(i_episode)
        
        def reset(self):
            '''
            Used to reset all elements position in the environment
            '''

            # get set of map indices in a flat array
            indices = np.arange(self.WIDTH * self.HEIGHT)

            # remove indices of obstacles
            for v in indices:
                if v in self.OBSTACLES:
                    # pop value out of indices
                    indices = np.delete(indices, np.where(indices == v))

            # Random set all agent positions
            self.HUSTLER_X, self.HUSTLER_Y = self.indexToXY(self.getRandom(indices))
            self.CATCHER_X, self.CATCHER_Y = self.indexToXY(self.getRandom(indices))
            self.GOAL_X, self.GOAL_Y = self.indexToXY(self.getRandom(indices))

            self.MOVES['hustler'] = 100
            self.MOVES['catcher'] = 100

            return self.get_state()

        def get_state(self):
            return

        def step(self, huslter_action, catcher_action):
            return
        
        def getRandom(self, indices):
            return indices[np.random.randint(0, len(indices))]

        def indexToXY(self, index):
            return (index % self.WIDTH, index // self.WIDTH)


        # === Info Panels ===
                
        def display_episode(self,epsiode):
            font = pygame.font.SysFont(None, 25)
            text = font.render("Episode: "+str(epsiode), True, (0,0,220))
            self.DISPLAY.blit(text,(1,1))





class Catcher():
    def __init__(self, display, width, height):
        self.DISPLAY = display
        self.WIDTH = width 
        self.HEIGHT = height
        
        self.IMG = pygame.image.load('sprites/smith.png')
        self.IMG = pygame.transform.scale(self.IMG, (self.WIDTH, self.HEIGHT))


    def draw(self, x, y):
        self.DISPLAY.blit(self.IMG, (x*self.WIDTH, y*self.HEIGHT))

class Hustler():
    def __init__(self, gameDisplay, width, height):
        self.DISPLAY = gameDisplay
        self.WIDTH = width 
        self.HEIGHT = height
    
        self.IMG = pygame.image.load('sprites/hustler.png')
        self.IMG = pygame.transform.scale(self.IMG, (self.WIDTH, self.HEIGHT))


    def draw(self, x, y):
        self.DISPLAY.blit(self.IMG, (x*self.WIDTH, y*self.HEIGHT))