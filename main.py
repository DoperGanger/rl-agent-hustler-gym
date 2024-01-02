import pygame
import numpy as np
import time

from environment import Env
from agent import Agent

# Colors
ORANGE = (255, 165, 0)
GREEN = (0, 150, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)

display_width, display_height = 800, 900

def show_info(goals, busts, game_display):
    pygame.draw.rect(gameDisplay, BLACK, [0, 800, 800, 5])
    font = pygame.font.SysFont(None, 40)
    text1 = font.render("Total Hustlers Escaped: "+str(goals), True, GREEN)
    text2 = font.render("Total Hustlers Busted: "+str(busts), True, RED)
    
    game_display.blit(text1,(50,810))
    game_display.blit(text2,(50,855))	

def draw_rect(game_display, color, x, y, width, height):
    pygame.draw.rect(game_display, color, [x*width, y*height, width, height], 10)
    pygame.display.update()
    time.sleep(0.5)

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Police and Hustler Agents')
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()


# Initialize Environment
env = Env(gameDisplay, 20, 20) #display, rows, columns
# set obstacles config if any
env.set_obstacles([
    8, 9, 10, 17, 18, 19, 37, 38, 39, 42, 57, 58, 59, 67, 68, 69, 70, 71, 77,
    78, 79, 80, 81, 82, 87, 88, 89, 90, 91, 97, 98, 99, 100, 101, 102, 
    107,108,109,110,111,117,
    118, 119, 120, 121, 122, 127, 128, 129, 130, 131, 137, 138, 139, 147, 148,
    149, 150, 151, 152, 157, 158, 159, 161, 167, 176, 180, 181, 182, 200, 201,
    202, 220, 221, 222, 246, 252, 261, 280, 281, 282, 287, 288, 289, 290, 291,
    300, 301, 302, 307, 308, 309, 310, 311, 316, 320, 321, 322, 327, 328, 329,
    330, 331, 338, 339, 347, 348, 349, 350, 351, 358, 359, 367, 368, 369, 370,
    371, 378, 379, 391, 398, 399,
    ])

# Initialize Agents
catcher = Agent(env, possibleActions = 4)
hustler = Agent(env, possibleActions = 4)

# Load the policies
dir = 'policies/'
# hustler.load_policy(dir+'mouse.pickle')
# catcher.load_policy(dir+'cat.pickle')
hustler.loadQtableFromJson(dir+'1goal1000hustlerQtable.json')
catcher.loadQtableFromJson(dir+'1goal1000catcherQtable.json')


# Init Stats
total_goals_reached = 0
total_hustlers_busted = 0

# Init Learning Params
num_episodes = 10000
epsilon, eps_decay, eps_min = 1.0, 0.99, 0.05

for i_episode in range(1, num_episodes+1):

    epsilon = max(epsilon*eps_decay, eps_min)
    state = env.reset()

    # Init Action for Agents
    action_hustler = hustler.greedy_action(state['hustler'], epsilon)
    action_catcher = catcher.greedy_action(state['catcher'], epsilon)
    
    #render the environment  
    env.render(i_episode)

    # loop until game is done
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # env step forward with chosen actions
        next_state, reward, done, info = env.step(action_hustler, action_catcher)

        #provide feedback to agents
        hustler.Q_learn(state['hustler'], action_hustler, reward['hustler'], next_state['hustler'])
        catcher.Q_learn(state['catcher'], action_catcher, reward['catcher'], next_state['catcher'])

        gameDisplay.fill(WHITE) #background color
        env.render(i_episode)
        show_info(total_goals_reached, total_hustlers_busted, gameDisplay) #goals, busts, game_display

        pygame.display.update()
        clock.tick(60)

        if done:
            if info['goal_reached']:
                total_goals_reached += 1
                draw_rect(gameDisplay, GREEN, info['x'], info['y'], info['width'], info['height'])       
            
            if info['hustler_caught']:
                total_hustlers_busted += 1
                draw_rect(gameDisplay, RED, info['x'], info['y'], info['width'], info['height'])  
            break

        # Update state
        state = next_state

        # What action to take next?

        # greedy action?

        # policy action?
        action_hustler = hustler.greedy_action(state['hustler'], epsilon)
        action_catcher = catcher.greedy_action(state['catcher'], epsilon)

hustler.set_policy(saveQtable=False, dir='')
catcher.set_policy(saveQtable=False, dir='')

#hustler.saveQtableToCsv('policies/'+str(num_episodes)+'hustler')
#catcher.saveQtableToCsv('policies/'+str(num_episodes)+'catcher')

hustler.saveQtableToJson('policies/'+"1goal"+str(num_episodes)+'hustler')
catcher.saveQtableToJson('policies/'+"1goal"+str(num_episodes)+'catcher')
