import pygame
from pygame.draw import *
from random import randint
pygame.init()


MAX_TARGETS_NUMBER = 3 # max number of targets on screen
FPS = 30
BALLS_DELAY = 30  #create new target each 30 frame 
BALLS_DELAY_COUNTER = 0
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
SCORE_TEXT_POSITION = (0,0)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Target:
    """Target class"""
    
    def __init__(self):
        """Constructor"""
        self.color = COLORS[randint(0, 5)]
        self.x = randint(100,SCREEN_WIDTH-100)
        self.y = randint(100,SCREEN_HEIGHT-100)
        self.r = randint(30,50)
        self.moveVector = [randint(-5,5), randint(-5,5)]
        if randint(0,10) == 0: 
            self.isSimple = False # shape: square, motion: random
            self.score = 3
        else:
            self.isSimple = True # shape: circle, motion: linear 
            self.score = 1
    
    def draw(self):
        """draw this target on screen"""
        if self.isSimple:
            circle(screen, self.color, (self.x, self.y), self.r)
        else:          
            polygon(screen, self.color, [(self.x,self.y), (self.x+self.r,self.y),
                                         (self.x+self.r,self.y+self.r), (self.x,self.y+self.r)])
    def clickcheck(self, event):
        """
        checking that the target is hit
        event - your mouse click
        """
        if self.isSimple:
            if( ((self.x-event.pos[0])**2 + (self.y-event.pos[1])**2) <= self.r**2):
                return True
            else:
                return False
        else:
            if( (self.x <= event.pos[0]) and (self.x + self.r >= event.pos[0]) and (self.y <= event.pos[1]) and (self.y+self.r >= event.pos[1]) ):
                return True
            else:
                return False
                
    def move(self):
        """this target move to one step"""
        if not self.isSimple: # new motion direction for square target
            if abs(self.moveVector[0]) > 10:
              self.moveVector[0] = 0
            if abs(self.moveVector[1]) > 10:
              self.moveVector[1] = 0
            self.moveVector[0] +=randint(-2,2) 
            self.moveVector[1] +=randint(-2,2)            
        self.x += self.moveVector[0]
        self.y += self.moveVector[1]
        if self.x <= self.r or self.x >= gscore.screen_width - self.r:
            self.moveVector[0] = -self.moveVector[0]
        if self.y <= self.r or self.y >= gscore.screen_height - self.r:
            self.moveVector[1] = -self.moveVector[1]

class Game:
    """main game class"""
 
    def __init__(self, SCREEN_SIZE, maxtarget=1):
        """
        Constructor
        maxtarget - max number of targets on screen
        SCREEN_SIZE - game screen size
        """
        self.score = 0 # your game score
        self.total = 0 # total targets generated
        self.maxtarget = maxtarget
        self.targets = []
        self.screen_height = SCREEN_SIZE[1]
        self.screen_width = SCREEN_SIZE[0]
    
    def next(self):
        """generate new target"""
        if(len(self.targets)>=self.maxtarget):
            for i in range(0, self.maxtarget-1):
                self.targets[i]=self.targets[i+1]            
            self.targets[self.maxtarget-1] = Target()  
        else:
            self.targets.append(Target())
        self.total += 1
        
    def scorestr(self):
        """return your score string to display on screen"""
        return ('Score: ' + str(self.score) + '/Targets: ' + str(self.total))
        
    def checkclick(self, event):
        """
        checking that any target is hit
        event - your mouse click
        """
        for i in range(len(self.targets)):
            if self.targets[i]:
                if self.targets[i].clickcheck(event):
                    self.score += self.targets[i].score
                    self.targets[i] = None
    def draw(self):
        """draw all active targets on screen"""
        screen.fill(BLACK)
        screen.blit(my_font.render( gscore.scorestr(), False, GREEN) , SCORE_TEXT_POSITION)        
        for t in self.targets:
            if t:
                t.draw()
                
    def move(self):
        """all active targets move to one step"""
        for t in self.targets:
            if t:
                t.move()
    
gscore = Game(SCREEN_SIZE, MAX_TARGETS_NUMBER)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    BALLS_DELAY_COUNTER += 1    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gscore.checkclick(event)
    gscore.move()
    if BALLS_DELAY_COUNTER == BALLS_DELAY:
        BALLS_DELAY_COUNTER = 0
        gscore.next()       
    gscore.draw()
    pygame.display.update()
    

pygame.quit()