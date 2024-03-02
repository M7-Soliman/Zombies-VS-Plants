
from . import mobile
from .mobile import Mobile
from FSMs import animation, movement

# from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, rectAdd, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Zombie(Mobile):
   def __init__(self, position):
      super().__init__(position, "zom.png")
        
      # # Animation variables specific to Kirby
      self.framesPerSecond = 6
      self.nFrames = 6
      
      self.nFramesList = {
         "moving"   : 8,
         "damage1"   : 8,
         "damage2"   : 8,
         "damage3"   : 8,
         "damage4"   : 8,
         "standing" : 6
      }
      
      self.rowList = {
         "moving"   : 1,
         "damage1"   : 2,
         "damage2"   : 3,
         "damage3"   : 4,
         "damage4"   : 5,
         "standing" : 0
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "damage1"   : 8,
         "damage2"   : 8,
         "damage3"   : 8,
         "damage4"   : 8,
         "standing" : 8
      }
            
            
      self.hp = 10
      # self.hitBox = rectAdd(self.position, self.getRect())
      self.FSManimated = animation.WalkingFSM(self)
      self.LR = movement.AccelerationFSM(self, axis=0)
      self.UD = movement.AccelerationFSM(self, axis=1)
      self.spawn = True
      self.dead =  True
      
   def getRect(self):
        return self.image.get_rect()
      
   # def handleEvent(self, event):
   #    if event.type == KEYDOWN:
   #       if event.key == K_UP:
   #          self.UD.decrease()
             
   #       elif event.key == K_DOWN:
   #          self.UD.increase()
            
   #       elif event.key == K_LEFT:
   #          self.LR.decrease()
            
   #       elif event.key == K_RIGHT:
   #          self.LR.increase()
            
   #    elif event.type == KEYUP:
   #       if event.key == K_UP:
   #          self.UD.stop_decrease()
             
   #       elif event.key == K_DOWN:
   #          self.UD.stop_increase()
             
            
   #       elif event.key == K_LEFT:
   #          self.LR.stop_decrease()
            
   #       elif event.key == K_RIGHT:
   #          self.LR.stop_increase()
   
   def update(self, seconds): 
      # print(self.frame)
      if self.frame == 5 and self.spawn==True:
         self.FSManimated.move()
         self.LR.decrease()
         self.spawn=False
      self.LR.update(seconds)
      self.UD.update(seconds)
      self.hitBox = rectAdd(self.position, self.getRect())
      super().update(seconds)

   # def updateMovement(self):
   #    pressed = pygame.key.get_pressed()

   #    if not pressed[pygame.K_UP] and self.UD == "decrease":
   #       self.UD.stop_decrease()
   #    if not pressed[pygame.K_DOWN] and self.UD == "increase":
   #       self.UD.stop_increase()
         
   #    if not pressed[pygame.K_LEFT] and self.LR == "decrease":
   #       self.LR.stop_decrease()
   #    if not pressed[pygame.K_RIGHT] and self.LR == "increase":
   #       self.LR.stop_increase()

   
  