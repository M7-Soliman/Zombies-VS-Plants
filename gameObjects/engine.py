import pygame

from . import Drawable, kirby
from .kirby import Kirby
from .zombie import Zombie
from UI import TextEntry
from .orb import Orb
import math
import copy
from utils import vec, RESOLUTION, SCALE
from soundManager2 import *
from .plant import Plant

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
        r=[5,58,58*2, 58*3, 58*4, 58*5]
        c=[80, 80*2, 80*3, 80*4, 80*5]
        
        self.plants=[Plant((r[0], c[0]), 0, 0, 0,reward=True), Plant((r[0], c[1]), 0, 0, 0,reward=True), Plant((r[0], c[2]), 0, 0, 0),
                     Plant((r[1], c[0]), 0, 0, 0), Plant((r[1], c[1]), 0, 0, 0), Plant((r[1], c[2]), 0, 0, 0,reward=True), 
                     Plant((r[2], c[0]), 0, 0, 0), Plant((r[2], c[1]), 0, 0, 0), Plant((r[2], c[2]), 0, 0, 0,reward=True), 
                     Plant((r[3], c[0]), 0, 0, 0), Plant((r[3], c[1]), 0, 0, 0,reward=True)]
        
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.png")
        self.tankicon = Drawable((5,5), "ticon.png")
        # self.timer = TimerStatic(2)
        self.lanes=[(700,55),(700,130),(700,215),(700,300)]
        self.zom = False
        self.tankcount= TextEntry((62,62),str(Zombie.Zombiecount))
        self.orb_creation_timer = 0


    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        self.tankicon.draw(drawSurface)
        self.tankcount.draw(drawSurface)
        [o.draw(drawSurface) for o in self.orbs]
        [o.draw(drawSurface) for o in self.zombies]
        [o.draw(drawSurface) for o in self.plants]
        # self.zombie.draw(drawSurface)
        # [p.draw_attack_range(drawSurface) for p in self.plants]
            
    def handleEvent(self, event):
              
        # self.zombie.handleEvent(event)
        [o.handleEvent(event) for o in self.zombies]
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_1:
                self.zom = True
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_1:
                self.zom = False
        if event.type == pygame.MOUSEBUTTONDOWN:

       
            if self.zom and Zombie.Zombiecount > 0:
                mousePosition = vec(*event.pos) // SCALE - vec(32,34)
                mousePosition=closest_position(mousePosition,self.lanes)
                self.zombies.append(Zombie((700,mousePosition[1])))
                Zombie.Zombiecount -=1
                
    def update(self, seconds):
        # self.zombie.update(seconds)
        # self.timer.update(seconds)
        # print(self.timer.time)
        # if self.timer.done():
        #     self.timer.reset()
        #     if len(self.orbs) < 10:
        #         self.orbs = [orb((0,5)),orb((0,45)),orb((0,85)),orb((0,125)),orb((0,165)),orb((0,205)),orb((0,245)),orb((0,285)),orb((0,325)),orb((0,365))]

        # self.orb_creation_timer += seconds
        # if self.orb_creation_timer >= 2:
        #     self.orb_creation_timer = 0
        #     for plant in self.plants:
        #         if plant.shooting == 1:
        #             pos = plant.position.copy()
        #             pos[0] += 3
        #             self.orbs.append(Orb(position=(pos)))
        
        
        
        for plant in self.plants:
            if plant.shooting == 1:
                plant.starting += seconds
                if plant.starting >= 2:
                    plant.starting = 0
                    pos = plant.position.copy()
                    pos[0] += 3
                    self.orbs.append(Orb(position=(pos)))


        self.tankcount= TextEntry((62,62),str(Zombie.Zombiecount))
        [o.update(seconds) for o in self.orbs]
        [o.update(seconds) for o in self.zombies]
        
        
        
        for orb in self.orbs:
            orb.update(seconds)
            if orb.position[0]>800:
                self.orbs.remove(orb)

                
        for j in range(len(self.zombies)):
            for r in range(len(self.orbs)):
                if self.orbs[r].hitBox.colliderect(self.zombies[j].hitBox):
                    self.zombies[j].hp-=1
                    self.orbs.pop(r) 
                    break

        for j in range(len(self.zombies)):
            for r in range(len(self.plants)):
                if self.plants[r].attackRange.colliderect(self.zombies[j].hitBox):
                    self.plants[r].shooting = 1

                                    
        for j in range(len(self.zombies)):
            if self.zombies[j].hp <=0:
                self.zombies.pop(j)  
            break
    
    
        for j in range(len(self.plants)):
            if self.plants[j].hp <=0:
                self.plants.pop(j) 
                if self.plants[j].reward:
                    Zombie.Zombiecount +=1
                break
            
        for j in range(len(self.zombies)):
            for r in range(len(self.plants)):
                if self.plants[r].hitBox.colliderect(self.zombies[j].hitBox):
                    self.plants[r].hp -= self.zombies[j].attack
                    break


  


