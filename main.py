import pygame
import numpy as np
import time

from environment import Env

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
#env.set_obstacles([])

# Initialize Agents
# cat = Agent(env, possibleActions = 4)
# mouse = Agent(env, possibleActions = 4)

# Number of Episodes
num_episodes = 1000

for i_episode in range(1, num_episodes+1):

    state = env.reset()

    env.render(i_episode)


    # Init Action for Agents

    # loop until game is done
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # env step forward with chosen actions
        #next_state, reward, done, info = env.step()

        gameDisplay.fill(WHITE) #background color
        env.render(i_episode)
        show_info(0, 0, gameDisplay) #goals, busts, game_display

        pygame.display.update()
        clock.tick(60)

        # if done:
            # update scores and info
        #   break

        # update state and next action
        # if loop:
        #     action_mouse = np.random.randint(0, 5)
        #     action_cat = np.random.randint(0, 5)
        #     loop = False