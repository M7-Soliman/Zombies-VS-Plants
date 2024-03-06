
from . import mobile
from .mobile import Mobile
from .drawable import Drawable
from FSMs import animation, movement
from pygame import transform

# from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, rectAdd, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Plant(Drawable):
   def __init__(self, position):
      super().__init__(position, "plany.png")
        
      #Descaling
      scale_factor = 0.3
      original_image = self.image.copy()  # Create a copy of the original image
      scaled_width = int(original_image.get_width() * scale_factor)
      scaled_height = int(original_image.get_height() * scale_factor)
      self.image = transform.smoothscale(original_image, (scaled_width, scaled_height))

      self.hp = 5
      self.hitBox = rectAdd(self.position, self.getRect())
      # self.FSManimated = animation.WalkingFSM(self)
      # self.LR = movement.AccelerationFSM(self, axis=0)
      # self.UD = movement.AccelerationFSM(self, axis=1)
      self.dead =  False
      
   def getRect(self):
        return self.image.get_rect()
     
   def update(self, seconds): 
      # print(self.frame)
      # if self.frame == 5 and self.spawn==True:
      #    self.FSManimated.move()
      #    self.LR.decrease()
      # self.LR.update(seconds)
      # self.UD.update(seconds)
      
      self.hitBox = rectAdd(self.position, self.getRect())
      super().update(seconds)