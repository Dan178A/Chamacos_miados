# Capybara Fisher
# Grid based rpg; play as a capybara, fishing throughout different spots on the map

# main.py
import time
import pygame as pg
from level import Level


def draw():
    """
    Update portions of the screen for display.
    Uses pg.display.update()
    :return:
    """
    pg.display.update()


class Game:
    def __init__(self):
        self.previous_time = time.time()  # create clock for calculating delta time
        self.level = Level(game=self, state="menu")

    def main(self):
        """
        Main loop and delta time calculator for game performance.
        :return:
        """
        while True:
            dt = time.time() - self.previous_time  # delta time
            self.previous_time = time.time()
            self.level.dt = dt
            self.level.update(dt)
            draw()


# Script call to run game loop
if __name__ == "__main__":  # if in main file
    game = Game()  # instantiate game
    game.main()  # run game loop
