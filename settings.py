import pygame as pg
from math import ceil
from pygame.locals import *  # import for flags

width, height = (1280, 800)
tile = 64
center_width = (width / 2) - tile
center_height = (height / 2) - tile

pg.init()
pg.mixer.pre_init()  # preset the mixer
pg.mixer.music.load('audio/blossom_of_the_water_lilies.wav')  # play forest foley sound
pg.mixer.music.set_volume(0)
pg.mixer.music.play(-1)  # play song on infinite loop, or until stopped
pg.display.set_caption('Capybara Fisher')
pg.mouse.set_visible(False)  # invisible mouse cursor
pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONUP, MOUSEBUTTONDOWN])  # types of events allowed

flags = DOUBLEBUF | SCALED | FULLSCREEN # fullscreen, double buffering, scaled resolution
window = pg.display.set_mode((width, height), flags)

white = [255, 255, 255]
title_font = pg.font.Font("fonts/dpcomic.ttf", 150)
play_font = pg.font.Font("fonts/dpcomic.ttf", 100)

menu_bg = pg.image.load("images/menu_bg.png").convert()
menu_bg = pg.transform.scale(menu_bg, (width, height))
menu_bg_width = menu_bg.get_width()
menu_tiles = ceil(width / menu_bg_width) + 1  # creates the amount of tiles for the menu screen scroll

clouds_bg = pg.image.load("images/clouds.png").convert_alpha()
clouds_bg = pg.transform.scale(clouds_bg, (width * 2, height))
clouds_bg.set_alpha(100)
clouds_bg_width = clouds_bg.get_width()
clouds_tiles = ceil(width / clouds_bg_width) + 1

capy_image = pg.image.load("images/capy1.png").convert_alpha()
capy_width = 64
capy_height = 96
capy_image = pg.transform.scale(capy_image, (capy_width, capy_height))

wall_image = pg.image.load("images/wall.png").convert_alpha()
wall_image = pg.transform.scale(wall_image, (tile, tile))
wall_image.set_alpha(0)

level1_image = pg.image.load("images/capy_level1.png").convert()
level1_image = pg.transform.scale(level1_image, (tile * 50, tile * 35))

river_image = pg.image.load("images/river.png").convert()
river_image = pg.transform.scale(river_image, (tile * 20, tile * 13))

capy_hand = pg.image.load("images/capy_hand.png").convert_alpha()
capy_hand = pg.transform.scale(capy_hand, (tile * 6, tile * 10))

fish_image = pg.image.load("images/fish.png").convert_alpha()
fish_image = pg.transform.scale(fish_image, (tile * 4, tile * 2))
