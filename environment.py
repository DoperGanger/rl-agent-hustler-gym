import pygame
import numpy as np 
import random

class Env():

    def __init__(self, display, rows, columns):
        self.HEIGHT = rows # y
        self.WIDTH = columns # x
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
        self.GOAL = pygame.transform.scale(pygame.image.load('sprites/drugs.png'),(self.BLOCK_WIDTH, self.BLOCK_HEIGHT))

    # Set Obstacles Postion Array ( array of indices)
    def set_obstacles(self, obstacles:np.array): # Used to change the obstacles in the map
            self.OBSTACLES = obstacles

    def render(self, i_episode = -1):
        # Draw Agents
        self.HUSTLER.draw(self.HUSTLER_X, self.HUSTLER_Y)
        self.CATCHER.draw(self.CATCHER_X, self.CATCHER_Y)
        self.DISPLAY.blit(self.GOAL, (self.GOAL_X*self.BLOCK_WIDTH, self.GOAL_Y*self.BLOCK_HEIGHT))

        # Draw Obstacles
        for pos in self.OBSTACLES:
            #pygame.draw.rect(self.DISPLAY, (0,0,255), [pos[0]*self.BLOCK_WIDTH, pos[1]*self.BLOCK_HEIGHT, self.BLOCK_WIDTH, self.BLOCK_HEIGHT])
            
            obs_x, obs_y = self.indexToXY(pos)
            pygame.draw.rect(self.DISPLAY, (34,49,29), [obs_x*self.BLOCK_WIDTH, obs_y*self.BLOCK_HEIGHT, self.BLOCK_WIDTH, self.BLOCK_HEIGHT])

        # Draw Info Panel
        if i_episode>=0:
            self.display_episode(i_episode)
        
    def reset(self):
        '''
        Used to reset all elements position in the environment
        '''
        
        # get set of map indices in a flat array
        indices = np.arange(self.WIDTH * self.HEIGHT)
        goal_positions = [199,219,239]

        # remove indices of obstacles
        for v in indices:
            if v in self.OBSTACLES:
                # pop value out of indices
                indices = np.delete(indices, np.where(indices == v))
        
        # remove indices of goal
        # for v in indices:
        #     if v in goal_positions:
        #         # pop value out of indices
        #         indices = np.delete(indices, np.where(indices == v))

        # Random set all agent positions
        hustler_pos = self.getRandomIndexPos(indices)
        #self.HUSTLER_X, self.HUSTLER_Y = self.indexToXY(hustler_pos)
        self.HUSTLER_X, self.HUSTLER_Y = self.indexToXY(0)
        # pop out hustler position from indices
        indices = np.delete(indices, np.where(indices == hustler_pos))
        catcher_pos = self.getRandomIndexPos(indices)
        #self.CATCHER_X, self.CATCHER_Y = self.indexToXY(catcher_pos)
        self.CATCHER_X, self.CATCHER_Y = (11,1)
        #self.GOAL_X, self.GOAL_Y = self.indexToXY(self.getRandomIndexPos(indices))

        # pop out hustler position and catcher position from goal positions
        goal_positions = np.delete(goal_positions, np.where(goal_positions == hustler_pos))
        goal_positions = np.delete(goal_positions, np.where(goal_positions == catcher_pos))
        self.GOAL_X, self.GOAL_Y = self.indexToXY(219)

        self.MOVES['hustler'] = 100
        self.MOVES['catcher'] = 100

        return self.get_state()

    def get_state(self):
        '''
        Return the state for the agent:
            Hustler:
                - Manhattan distance between hustler and catcher
                - Manhattan distance between hustler and goal
                - Info about walls and obstacles in their neighborood?
            Catcher:
                - Manhattan distance between hustler and catcher
                - Info about walls and obstacles in their neighborood?
        '''
        self.STATE = {'hustler':(
                                #self.HUSTLER_X - self.CATCHER_X, self.HUSTLER_Y - self.CATCHER_Y,
                                #self.HUSTLER_X - self.GOAL_X, self.HUSTLER_Y -  self.GOAL_Y,
            
                                # add map index for obstacle aware
                                self.HUSTLER_Y*self.WIDTH + self.HUSTLER_X,
                                self.CATCHER_Y*self.WIDTH + self.CATCHER_X,
                                self.GOAL_Y*self.WIDTH + self.GOAL_X,
                                ), 
                    'catcher':(
                                #self.CATCHER_X - self.HUSTLER_X, self.CATCHER_Y - self.HUSTLER_Y, 
                                # add map index for obstacle aware
                                self.HUSTLER_Y*self.WIDTH + self.HUSTLER_X,
                                self.CATCHER_Y*self.WIDTH + self.CATCHER_X,
                                self.GOAL_Y*self.WIDTH + self.GOAL_X,
                            )}

        return self.STATE
        
    def step(self, hustler_action, catcher_action):
        '''
        Reward update, change angents' position and do some controls about position changes.
        '''
        reward = {'hustler':-1, 'catcher':-1}
        done = False
        info = {
            'goal_reached': False,
            'hustler_caught': False, 
            'x': -1, 'y': -1, 
            'width':self.BLOCK_WIDTH, 
            'height':self.BLOCK_HEIGHT
        }

        #decreasing the no. of moves
        self.MOVES['catcher'] -= 1
        self.MOVES['hustler'] -= 1
        #done if moves = 0
        if self.MOVES['catcher'] == 0 or self.MOVES['hustler'] == 0:
            done = True

        # track previous positions
        prev_hustler_x, prev_hustler_y = self.HUSTLER_X, self.HUSTLER_Y
        prev_catcher_x, prev_catcher_y = self.CATCHER_X, self.CATCHER_Y

        self.update_positions(hustler_action, catcher_action)
        
        #hustler reached the goal
        if self.HUSTLER_X == self.GOAL_X and self.HUSTLER_Y == self.GOAL_Y:
            done = True
            reward['hustler'] = 50
            info['goal_reached'], info['x'], info['y'] = True,  self.HUSTLER_X, self.HUSTLER_Y
        
        #catcher caught the hustler
        if self.CATCHER_X == self.HUSTLER_X and self.CATCHER_Y == self.HUSTLER_Y:
            done = True
            reward['catcher'] = 50
            reward['hustler'] = -20
            info['hustler_caught'], info['x'], info['y'] = True,  self.HUSTLER_X, self.HUSTLER_Y
        
        # if hit obstacles we port them back to the start and penalize?
        for obs in self.OBSTACLES:
            obs_x, obs_y = self.indexToXY(obs)
            #if self.HUSTLER_X == obs[0] and self.HUSTLER_Y == obs[1]:
            if self.HUSTLER_X == obs_x and self.HUSTLER_Y == obs_y:
                reward['hustler'] = -20
                self.HUSTLER_X, self.HUSTLER_Y = (0,0)

            if self.CATCHER_X == obs_x and self.CATCHER_Y == obs_y:    
                reward['catcher'] = -20
                self.CATCHER_X, self.CATCHER_Y = (0, self.HEIGHT -1)
        
        # if position no change (meaning they went out of bounds of env), penalize?
        if prev_hustler_x == self.HUSTLER_X and prev_hustler_y == self.HUSTLER_Y:
            reward['hustler'] = -20
        if prev_catcher_x == self.CATCHER_X and prev_catcher_y == self.CATCHER_Y:
            reward['catcher'] = -20

        return self.get_state(), reward, done, info
    

    def update_positions(self, hustler_action, catcher_action): # Update agents' position
        x_change_hustler, y_change_hustler = self.get_changes(hustler_action)
        x_change_catcher, y_change_catcher = self.get_changes(catcher_action)
        #x_change_catcher, y_change_catcher = (0,0)

        self.HUSTLER_X += x_change_hustler 
        self.HUSTLER_Y += y_change_hustler

        self.CATCHER_X += x_change_catcher
        self.CATCHER_Y += y_change_catcher

        # a fix for going out of bounds
        self.HUSTLER_X, self.HUSTLER_Y = self.fix(self.HUSTLER_X, self.HUSTLER_Y)
        self.CATCHER_X, self.CATCHER_Y = self.fix(self.CATCHER_X, self.CATCHER_Y)


    def get_changes(self, action): # Get changes by action choosed
        x_change, y_change = 0, 0
        if action == 0:
            x_change = -1   #moving LEFT
        elif action == 1:
            x_change = 1    #moving RIGHT
        elif action == 2:
            y_change = -1   #moving UP
        elif action ==3:
            y_change = 1    #moving DOWN
        
        return x_change, y_change


    def getRandomIndexPos(self, indices):
        return indices[np.random.randint(0, len(indices))]


    def indexToXY(self, index):
        return (index % self.WIDTH, index // self.WIDTH)


    def fix(self, x, y):
        # If agents out of bounds, fix!
        if x < 0:
            x = 0
        elif x > self.WIDTH-1:
            x = self.WIDTH-1
        if y < 0:
            y = 0
        elif y > self.HEIGHT -1:
            y = self.HEIGHT -1

        return x, y


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
    
        self.IMG = pygame.image.load('sprites/pinkman.png')
        self.IMG = pygame.transform.scale(self.IMG, (self.WIDTH, self.HEIGHT))


    def draw(self, x, y):
        self.DISPLAY.blit(self.IMG, (x*self.WIDTH, y*self.HEIGHT))