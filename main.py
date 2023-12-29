import pygame
import numpy as np
import time

# Colors
ORANGE = (255, 165, 0)
GREEN = (0, 150, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)

display_width, display_height = 800, 900

def show_info(door, hustler, game_display):
    pygame.draw.rect(gameDisplay, BLACK, [0, 800, 800, 5])
    font = pygame.font.SysFont(None, 40)
    text1 = font.render("Total Hustlers Escaped: "+str(door), True, GREEN)
    text2 = font.render("Total Hustlers Busted: "+str(hustler), True, RED)
    
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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    gameDisplay.fill(WHITE)

    pygame.display.update()
    clock.tick(60)