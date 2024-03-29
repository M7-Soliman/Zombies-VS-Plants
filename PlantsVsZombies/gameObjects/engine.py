import pygame

from . import Drawable, kirby
from .kirby import Kirby
from .zombie import Zombie
from .orb import orb
import math
import copy
from utils import vec, RESOLUTION, SCALE



def closest_position(mouse_click, position_list):
    distances = [math.sqrt((mouse_click[0] - pos[0]) ** 2 + (mouse_click[1] - pos[1]) ** 2) for pos in position_list]
    min_distance_index = distances.index(min(distances))
    return position_list[min_distance_index]
    
class TimerStatic(object):
    def __init__(self, setTo):
        self.time = 0
        self.setTo = setTo
        self.reset()
    
    def reset(self):
        self.time = self.setTo
    
    def done(self):
        return self.time <= 0

    def update(self, seconds):
        self.time -= seconds


class GameEngine(object):
    import pygame

    def __init__(self):       
        # self.zombie = Zombie((100,0))
        # self.orbs= [orb((0,5)),orb((0,45)),orb((0,85)),orb((0,125)),orb((0,165)),orb((0,205)),orb((0,245)),orb((0,285)),orb((0,325)),orb((0,365))]
        # self.zombies = [Zombie((700,25)),Zombie((700,100)),Zombie((700,175)),Zombie((700,250))]
        # self.orbs_copy= [orb((0,5)),orb((0,45)),orb((0,85)),orb((0,125)),orb((0,165)),orb((0,205)),orb((0,245)),orb((0,285)),orb((0,325)),orb((0,365))]
        self.orbs=[]
        self.zombies=[]
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.png")
        # self.timer = TimerStatic(2)
        self.lanes=[(700,55),(700,130),(700,215),(700,300)]
        self.zom = False
    
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        
                
        [o.draw(drawSurface) for o in self.orbs]
        [o.draw(drawSurface) for o in self.zombies]
        # self.zombie.draw(drawSurface)
        
            
    def handleEvent(self, event):
      
        # self.zombie.handleEvent(event)
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_1:
                self.zom = True
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_1:
                self.zom = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.zom:
                mousePosition = vec(*event.pos) // SCALE - vec(25, 25)
                self.orbs.append(orb(position=(0,mousePosition[1])))
       
            if self.zom:
                mousePosition = vec(*event.pos) // SCALE - vec(32,34)
                mousePosition=closest_position(mousePosition,self.lanes)
                self.zombies.append(Zombie((700,mousePosition[1])))
            
    def update(self, seconds):
        # self.zombie.update(seconds)
        # self.timer.update(seconds)
        # print(self.timer.time)
        # if self.timer.done():
        #     self.timer.reset()
        #     if len(self.orbs) < 10:
        #         self.orbs = [orb((0,5)),orb((0,45)),orb((0,85)),orb((0,125)),orb((0,165)),orb((0,205)),orb((0,245)),orb((0,285)),orb((0,325)),orb((0,365))]

            
        [o.update(seconds) for o in self.orbs]
        [o.update(seconds) for o in self.zombies]
        
        for orb in self.orbs:
            orb.update(seconds)
            
        
        for j in range(len(self.zombies)):
            for r in range(len(self.orbs)):
                if self.orbs[r].hitBox.colliderect(self.zombies[j].hitBox):
                    self.zombies[j].hp-=1
                    self.orbs.pop(r) 
                    break
  
        for j in range(len(self.zombies)):
            if self.zombies[j].hp <=0:
                self.zombies.pop(j) 
                break
      
        # Drawable.updateOffset(self.zombie, self.size)
  
    

