# player.py
# includes Player class for the movable character during levels

from settings import *
import pygame as pg
from pygame.math import Vector2
from timer import Timer
from movimiento import camara
import threading
class Player(pg.sprite.Sprite):
    def __init__(self, game, position, group):
        # Player class init function, initialize sprite group attributes
        super().__init__(group)
        self.game = game
        self.image = self.standard_image = capy_image
        self.rect = self.image.get_rect(center=position)
        self.collision_rect = self.rect
        self.collision_rect.height = capy_height
        self.dir = "up"
        self.direction = Vector2()
        self.position = Vector2(self.rect.center)
        self.last_position = self.position
        self.speed = 150
        self.moving = False
        self.collision_timer = pg.time.get_ticks()
        self.set_animation()  # instantiate all animation images and the timers
        movimiento = camara(self)
        t = threading.Thread(target=movimiento.init, args=(False, 1, 1))
        t.start()

    def set_animation(self):
        """
        Animation framework function for player character. Sets animations and timing for direction handling.
        :return:
        """
        self.up_images = [pg.transform.scale(pg.image.load(f'images/capy/Back_0{x}.png'), (capy_width, capy_height)) for
                          x in range(8)]
        self.up_timer = Timer(self.up_images, 0, delay=50)
        self.down_images = [pg.transform.scale(pg.image.load(f'images/capy/Front_0{x}.png'), (capy_width, capy_height))
                            for x in range(8)]
        self.down_timer = Timer(self.down_images, 0, delay=50)
        self.right_images = [pg.transform.scale(pg.image.load(f'images/capy/Right_0{x}.png'), (capy_width, capy_height))
                             for x in range(8)]
        self.right_timer = Timer(self.right_images, 0, delay=50)
        self.left_images = [pg.transform.scale(pg.image.load(f'images/capy/Left_0{x}.png'), (capy_width, capy_height))
                            for x in range(8)]
        self.left_timer = Timer(self.left_images, 0, delay=50)
        self.timer = self.up_timer

    def input(self,pave = "En otro lado", movimiento = ""):
        """
        Key input getter, direction and animations setter
        :return:
        """
        if pave == "cerrando":
            self.game.level.fishing()

        keys = pg.key.get_pressed()
        self.moving = False
        # direction handling
        # uses wasd key inputs for player direction
        if keys[pg.K_w]:
            self.direction.y = -1
            self.timer = self.up_timer
            self.standard_image = self.up_images[0]
            self.dir = "up"
            self.moving = True
        elif keys[pg.K_s]:
            self.direction.y = 1
            self.timer = self.down_timer
            self.standard_image = self.down_images[0]
            self.dir = "down"
            self.moving = True
        else:
            self.direction.y = 0

        if keys[pg.K_a]:
            self.direction.x = -1
            self.timer = self.left_timer
            self.standard_image = self.left_images[0]
            self.dir = "left"
            self.moving = True
        elif keys[pg.K_d]:
            self.direction.x = 1
            self.timer = self.right_timer
            self.standard_image = self.right_images[0]
            self.dir = "right"
            self.moving = True
        elif keys[pg.K_SPACE]:
            self.game.level.fishing()
        else:
            self.direction.x = 0
            
    def update_direction_from_camera(self, direction):
        self.moving = False

        if direction == "Superior":
            self.direction.y = -1
            self.timer = self.up_timer
            self.standard_image = self.up_images[0]
            self.dir = "up"
            self.moving = True
        elif direction == "Inferior":
            self.direction.y = 1
            self.timer = self.down_timer
            self.standard_image = self.down_images[0]
            self.dir = "down"
            self.moving = True
        else:
            self.direction.y = 0

        if direction == "Izquierda":
            self.direction.x = -1
            self.timer = self.left_timer
            self.standard_image = self.left_images[0]
            self.dir = "left"
            self.moving = True
        elif direction == "Derecha":
            self.direction.x = 1
            self.timer = self.right_timer
            self.standard_image = self.right_images[0]
            self.dir = "right"
            self.moving = True
        else:
            self.direction.x = 0

    def update_collision_rect(self):
        """
        Sets the center of collision rect to the center of the player rect
        :return:
        """
        self.collision_rect.center = self.rect.center

    def move(self, dt):
        """
        Calculates movement from direction, speed, and delta time.
        Normalizes diagonal vector movement.
        Sets last position in case of collision
        :param dt:
        :return:
        """
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        movement = self.direction * self.speed * dt

        # if there is no collision, set the last position to a safe spot
        if not self.game.level.check_collisions():
            self.last_position = self.position - movement
            self.position += movement
        # if there is collision, player goes to last position
        else:
            self.position = self.last_position

        # set center position of player rect to the location of the position vector
        self.rect.center = round(self.position)
        self.update_collision_rect()

    def update(self, dt):
        """
        Gets input and moves player. Overrides pygame.update built in function
        :param dt:
        :return:
        """
        # self.input()
        self.move(dt)

    def draw(self):
        """
        Draws player onto window given movement status
        """
        # if moving and no collisions, set image to animation loop
        # otherwise if there are collisions, set standard image of player
        if self.moving and not self.game.level.check_collisions():
            self.image = self.timer.image()
        else:
            self.image = self.standard_image

        window.blit(self.image,
                    (self.rect.x - self.game.level.game_scroll[0], self.rect.y - self.game.level.game_scroll[1]))
