from . import AbstractGameFSM
from utils import magnitude, EPSILON, SpriteManager

from statemachine import State

class AnimateFSM(AbstractGameFSM):
    """For anything that animates. Adds behavior on
       transitioning into a state to change animation."""
    def on_enter_state(self):
        state = self.current_state.id
        if self.obj.row != self.obj.rowList[state]:
            self.obj.nFrames = self.obj.nFramesList[state]
            self.obj.frame = 0
            self.obj.row = self.obj.rowList[state]
            self.obj.framesPerSecond = self.obj.framesPerSecondList[state]
            self.obj.animationTimer = 0
            self.obj.image = SpriteManager.getInstance().getSprite(self.obj.imageName,
                                                                   (self.obj.frame, self.obj.row))
         
        
class WalkingFSM(AnimateFSM):
    """Two-state FSM for walking / stopping in
       a top-down environment."""
       
    standing = State(initial=True)
    moving   = State()
    damage1= State()
    damage2= State()
    damage3= State()
    damage4= State()
    # dead= State()

    move = standing.to(moving)  | damage1.to(moving)  | damage1.to(moving)  | damage1.to(moving)  | damage1.to(moving)  
    stop = moving.to(standing)
    hurt1 = moving.to(damage1)
    hurt2 = damage1.to(damage2)
    hurt3 = damage2.to(damage3)
    hurt4 = damage3.to(damage4)
    # die = damage4.to(dead)
        
    
    def updateState(self):
        if self.obj.hp == 8 and self == "moving":
            self.hurt1()
        if self.obj.hp == 6 and self == "damage1":
                self.hurt2()
        if self.obj.hp == 4 and self == "damage2":
                self.hurt3()
        if self.obj.hp == 2 and self == "damage3":
                self.hurt4()
        if self.hasVelocity() and self == "standing":
            self.move()
        # elif not self.hasVelocity() and self != "standing":
        #     self.stop()
    
    def hasVelocity(self):
        return magnitude(self.obj.velocity) > EPSILON
    
    def noVelocity(self):
        return not self.hasVelocity()