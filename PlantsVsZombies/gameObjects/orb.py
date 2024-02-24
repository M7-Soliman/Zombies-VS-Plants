
from . import mobile
from .mobile import Mobile
from FSMs import animation, movement

# from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, rectAdd, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class orb(Mobile):
    
    
    def __init__(self, position):
        # print()
        super().__init__( position, "orb.png")
        self.velocity = vec(0,0)
        self.accel =  vec(20000,0)
        # self.acc = vec(300,300)
        self.hitBox = pygame.Rect(0, 0, 50, 50)
            
    def update(self, seconds):
        if 0 > self.position[0] or RESOLUTION[0] < self.position[0]:
           self.position[0] = 0
        
      #   if 0 > self.position[1] or RESOLUTION[1] < self.position[1]:
      #       self.position[0] = 0
        
        self.velocity =  self.accel * seconds
        super().update(seconds)
        self.hitBox = rectAdd(self.position, self.getRect())
        