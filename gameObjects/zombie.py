
from . import mobile
from .mobile import Mobile
from FSMs import animation, movement

# from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, rectAdd, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Zombie(Mobile):
   Zombiecount=4
   powerup = 1
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
         "standing" : 6,
          "powered"   : 8
      }
      
      self.rowList = {
         "moving"   : 1,
         "damage1"   : 2,
         "damage2"   : 3,
         "damage3"   : 4,
         "damage4"   : 5,
         "standing" : 0,
         "powered"   : 6
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "damage1"   : 8,
         "damage2"   : 8,
         "damage3"   : 8,
         "damage4"   : 8,
         "powered"   : 8,
         "standing" : 8
      }
            
      
      self.hp = 10
      self.attack=5
      self.pow = False
      # self.hitBox = rectAdd(self.position, self.getRect())
      self.FSManimated = animation.WalkingFSM(self)
      self.LR = movement.AccelerationFSM(self, axis=0)
      self.spawn = True
      self.dead =  True
      
      
   def getRect(self):
        return self.image.get_rect()
      
   def handleEvent(self, event):
      if event.type == KEYDOWN:
         if event.key == K_UP and Zombie.powerup > 0:
            Zombie.powerup -=1
            self.pow=True
            self.hp=10
            self.attack=10
   
   def update(self, seconds): 
      # print(self.frame)
      if self.frame == 5 and self.spawn==True:
         self.FSManimated.move()
         self.LR.decrease()
         self.spawn=False
      self.LR.update(seconds)
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

   
  