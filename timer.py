# timer.py
# Includes Timer class for timing animations on sprites

import pygame as pg


class Timer:
    def __init__(self, image_list, start_index=0, delay=100, is_loop=True):
        # Timer class initialization function
        self.image_list = image_list
        self.delay = delay
        self.is_loop = is_loop
        self.last_time_switched = pg.time.get_ticks()
        self.frames = len(image_list)
        self.start_index = start_index
        self.index = start_index if start_index <= len(image_list) - 1 else 0

    def next_frame(self):
        """
        Increase index for animation frame by 1 or loop back around to index 0 if at end of indexes.
        :return:
        """
        if self.is_expired():
            return
        now = pg.time.get_ticks()
        if now - self.last_time_switched > self.delay:
            self.index += 1
            if self.is_loop:
                self.index %= self.frames
            self.last_time_switched = now

    def reset(self):
        """
        Reset index to 0 upon reaching last index
        :return: Boolean Value
        """
        self.index = self.start_index if self.start_index < len(self.image_list) - 1 else 0

    def is_expired(self) -> bool:
        """
        Checks if the animation sequence is expired; not a loop and end of the sequence.
        :return: Boolean Value
        """
        return not self.is_loop and self.index >= len(self.image_list) - 1

    def image(self):
        """
        Call next_frame, then return the next image in the list
        :return:
        """
        self.next_frame()
        return self.image_list[self.index]
