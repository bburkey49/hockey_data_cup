import pandas as pd
import csv


headers = ["game_date",
           "Home Team",
           "Away Team",
           "Period",
           "Clock",
           "Home Team Skaters",
           "Away Team Skaters",
           "Home Team Goals",
           "Away Team Goals",
           "Team",
           "Player",
           "Event",
           "X Coordinate",
           "Y Coordinate",
           "Detail 1",
           "Detail 2",
           "Detail 3",
           "Detail 4",
           "Player 2",
           "X Coordinate 2",
           "Y Coordinate 2"
           ]

shots = []
goals = []


with open('/Users/bburkey49/Documents/playground/hockey_comp/big_data_cup_2021/hackathon_womens.csv', 'r') as csvfile:
    df = pd.read_csv(csvfile, delimiter=',', )

    for event, x, y in zip(df["Event"], df["X Coordinate"], df["Y Coordinate"]):
        if event == "Shot":
            shots.append((x, y))

        elif event == "Goal":
            goals.append((x,y))



import sys
import pygame
from pygame.locals import KEYDOWN, K_q

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 600, 255
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (160, 160, 160)
PADDING = PADTOPBOTTOM, PADLEFTRIGHT = 0, 0
# VARS:
_VARS = {'surf': False}


def main():
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        drawGrid(3)
        pygame.display.update()


def drawGrid(divisions):
    # DRAW Rectangle

    # TOP lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM), 2)


    # BOTTOM lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (0 + PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM),
      (WIDTH - PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)


    # LEFT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (0 + PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)


    # RIGHT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (WIDTH - PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)

    # Get cell size
    horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
    vertical_cellsize = (HEIGHT - (PADTOPBOTTOM*2))/divisions

    # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
    for x in range(divisions):
        pygame.draw.line(
           _VARS['surf'], BLACK,
           (0 + PADLEFTRIGHT+(horizontal_cellsize*x), 0 + PADTOPBOTTOM),
           (0 + PADLEFTRIGHT+horizontal_cellsize*x, HEIGHT - PADTOPBOTTOM), 2)
    # HORITZONTAL DIVISION
        pygame.draw.line(
          _VARS['surf'], BLACK,
          (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize*x)),
          (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize*x)), 2)


    plotted_shots = []
    for shot in shots:
        adj = (shot[0] * 3, shot[1] * 3)
        alpha = 1.5
        if shot in plotted_shots:
            alpha += 1.5
        # print(f'Adj: {adj}')
        pygame.draw.circle(
            _VARS['surf'], BLACK, 
            adj, alpha)
        plotted_shots.append(shot)

    plotted_goals = []
    for goal in goals:
        adj = (goal[0] * 3, goal[1] * 3)
        alpha = 1.5
        if goal in plotted_goals:
            alpha += 1.5
        # print(f'Adj: {adj}')
        pygame.draw.circle(
            _VARS['surf'], RED, 
            adj, alpha)
        plotted_goals.append(goal)

    # print(f"Goals: {len(goals)}")

    # pygame.draw.circle(_VARS['surf'], GREEN, (150,30), 100)


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()



