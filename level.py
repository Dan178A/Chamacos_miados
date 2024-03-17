# level.py
# Includes Level class for all scenes/menus/levels inside the game

import sys
from settings import *
from player import Player
from fish import Hand, Fish
import pygame as pg
from pygame.sprite import Group


class Level:
    dt = 0
    score = 0

    def __init__(self, game, state):
        # Level class init function, initialize attributes
        self.game = game
        self.state = state
        self.display_surface = pg.display.get_surface()
        self.sprite_group = Group()
        self.game_scroll = [0, 0]
        self.player = Player(game, (tile * 4 + tile // 2, tile * 4 + tile // 2), self.sprite_group, self.dt)
        self.hand = Hand(self.sprite_group)
        self.fish = Fish(self.sprite_group)
        self.level_background = level1_image
        self.level_board_file = "boards/board-level-1.txt"
        self.menu_scroll = 0
        self.current_level = 0
        self.clouds_scroll = 0
        self.game_scroll = [0, 0]
        self.wiggle = [0, 0]
        self.text_bounce = 0
        self.drop_color = [0, 0, 0]  # black
        self.time = pg.time.get_ticks()
        self.fishing_tiles = None
        self.collision_tiles = None
        self.current_board = None
        self.score = 0

    def next_level(self):
        """
        Add 1 to the current level counter and load the current level
        :return:
        """
        self.current_level += 1
        self.load_level()

    def load_level(self):
        """
        Opens and saves the current level_board to a 2d list.
        :return:
        List of lists
        """
        # creates or resets a list, adding each row as a list, stripping the last element (newline element)
        self.fishing_tiles = []
        self.current_board = []
        self.collision_tiles = []
        # spawn different things based on the current level
        if self.current_level == 1:
            with open(self.level_board_file, "r") as open_board:
                for row in open_board:
                    self.current_board.append(list(row[:-1]))
            for i in range(len(self.current_board)):
                for j in range(len(self.current_board[0])):
                    if self.current_board[i][j] == "F":
                        self.fishing_tiles.append(
                            wall_image.get_rect(center=(j * tile + tile // 2, i * tile + tile // 2)))
                    if self.current_board[i][j] == '.':  # . = wall
                        self.collision_tiles.append(
                            wall_image.get_rect(center=(j * tile + tile // 2, i * tile + tile // 2)))

    def check_collisions(self) -> bool:
        """
        Checks for collision; if the player's center point collides with a tile
        :return Boolean Value:
        """
        for coll_tile in self.collision_tiles:
            if coll_tile.collidepoint(self.player.collision_rect.center):
                return True
        return False

    def can_fish(self) -> bool:
        """
        Check for collision with a "fishing spot" tile.
        :return Boolean Value:
        """
        for fish_tile in self.fishing_tiles:
            if fish_tile.colliderect(self.player.collision_rect):
                return True
        return False

    def fishing(self,dt):
        """
        Fishing events; handles key events while fishing.
        :return:
        """
        # print("fishing")
        self.state = "fishing"

        # self.s
        # Crear un contador
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()  # quit on esc key
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.hand.grab(self.fish):
                    self.score += 1
                    print(f"Score: {self.score}")
                    self.fish.catch_and_go()
                    self.fish = Fish(self.sprite_group)
                else:
                    print("No fish")
                    pass
                if self.score == 5:
                    self.state = "level1"
                self.fish.draw(dt)
            elif event.type == pg.MOUSEBUTTONUP:
                self.hand.reset_hand()

    def level1(self, dt):
        """
        Level 1 events; handles key events while roaming free on level 1.
        wiggle[] is the difference between the background and the screen size, which is factored into the scroll.
        game_scroll[] is applied to the position of objects on the screen, resulting in a visual scroll effect.
        :return:
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()  # quit on esc key
                    sys.exit()
        # wiggle room: the size of the background level image - the size of the screen
        # This is the different between the size of the screen and the size of the current level
        self.wiggle[0] = self.level_background.get_size()[0] - width
        self.wiggle[1] = self.level_background.get_size()[1] - height

        # game screen scroll: screen move effect centered around player but stops at screen edges
        # dividing this value causes the scroll to smoothly follow the player in a delayed manner, not a locked scroll
        self.game_scroll[0] += (self.player.rect.x - self.game_scroll[0] - center_width) / 50
        self.game_scroll[1] += (self.player.rect.y - self.game_scroll[1] - center_height) / 50

        # game will always stop scrolling at the borders of the game map
        if self.game_scroll[0] < 0:
            self.game_scroll[0] = 0
        if self.game_scroll[1] < 0:
            self.game_scroll[1] = 0
        if self.game_scroll[0] > self.wiggle[0]:
            self.game_scroll[0] = self.wiggle[0]
        if self.game_scroll[1] > self.wiggle[1]:
            self.game_scroll[1] = self.wiggle[1]

        self.sprite_group.update(dt)

    def menu(self):
        """
        Menu state
        handles scroll calculation per tick and key getter
        :return:
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.state = "level1"
                    self.next_level()
                if event.key == pg.K_ESCAPE:
                    pg.quit()  # quit on esc key
                if event.key == pg.K_ESCAPE:
                    pg.quit()  # quit on esc key
                    sys.exit()

        # scroll background at this rate per frame
        self.menu_scroll -= .25
        self.clouds_scroll += .1

        # reset scroll upon reaching edge of first tile
        if abs(self.menu_scroll) > menu_bg_width:
            self.menu_scroll = 0

        if abs(self.clouds_scroll) > clouds_bg_width:
            self.clouds_scroll = 0

    def menu_titles(self, x1, y1, x2, y2):
        """
        Main Menu Titles
        Encapsulated drop shadow functions for tiles, title bounce effect
        """
        title_drop_shadow = title_font.render("Isla del Capy", False, self.drop_color)
        title_drop_shadow.set_alpha(100)
        window.blit(title_drop_shadow, (x1 - 10 - self.text_bounce, y1 - 10 - self.text_bounce))
        title = title_font.render("Isla del Capy", False, white)
        window.blit(title, (x1 + self.text_bounce, y1 + self.text_bounce))
        play_drop_shadow = play_font.render("- press p to play -", False, self.drop_color)
        play_drop_shadow.set_alpha(100)
        play_title = play_font.render("- press p to play -", False, white)

        # Text bounce effect + flashing play title
        cur = pg.time.get_ticks() - self.time
        if cur < 1000:
            window.blit(play_drop_shadow, (x2 - 10, y2 - 10))
            window.blit(play_title, (x2, y2))
            self.text_bounce += .05
        elif cur < 2000:
            self.text_bounce -= .05
        elif cur < 2500:
            self.time = pg.time.get_ticks()

    def update(self, dt):
        """
        State handling update function. Directs game to different states/levels.
        :param dt:
        :return:
        """
        self.dt = dt
        if self.state == "menu":
            self.menu()
        if self.state == "level1":
            self.level1(dt)
        if self.state == "fishing":
            self.fishing(dt)
        self.draw(dt)

    def draw(self, dt):
        """
        Blit sprites on screen by level state.
        :param dt:
        :return:
        """
        if self.state == "menu":
            # blit tiles so that they seamlessly align, from left to right
            for tiles in range(0, menu_tiles):
                window.blit(menu_bg, (tiles * menu_bg_width + self.menu_scroll, 0))
            for tiles in range(0, clouds_tiles):
                window.blit(clouds_bg, (tiles * -clouds_bg_width + self.clouds_scroll, 0))
            # blit menu titles/text with function
            self.menu_titles(155, 155, 290, 550)
        if self.state == "level1":
            # blit BG image for current level, adjusting for scroll
            window.blit(self.level_background, (0 - self.game_scroll[0], 0 - self.game_scroll[1]))
            # blit the collision tiles
            for e in self.collision_tiles:
                window.blit(wall_image, (e.x - self.game_scroll[0], e.y - self.game_scroll[1]))
            # self.sprite_group.draw(self.display_surface)
            self.player.draw()

        if self.state == "fishing":
            # fishes = [Fish(self.sprite_group) for _ in range(20)]
            window.blit(river_image, (0, 0))
            # for fish in fishes:
            #     fish.draw(dt)
            # self.hand.draw(dt)
            self.fish.draw(dt)
            self.hand.draw(dt)
