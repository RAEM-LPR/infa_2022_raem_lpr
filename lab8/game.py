from curses.textpad import rectangle
from pickle import FALSE
import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 1
screen = pygame.display.set_mode((1200, 900))
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class gamescore(object):
    """docstring"""
 
    def __init__(self, maxtarget=1):
        """Constructor"""
        self.score = 0
        self.total = 0
        self.maxtarget = maxtarget
        self.targets=[]
        
    def increm(self):
        self.score += 1
    
    def next(self):
        if(len(self.targets)>=self.maxtarget):
            for i in range(0, self.maxtarget-1):
                self.targets[i]=self.targets[i+1]            
            self.targets[self.maxtarget-1] = target()  
        else:
            self.targets.append(target())
        self.total += 1
        
    def scorestr(self):
        return ('Score: ' + str(score) + '/' + str(total))
    
    


class target(object):
    """docstring"""
 
    def __init__(self):
        """Constructor"""
        self.color = COLORS[randint(0, 5)]
        self.x = randint(100,700)
        self.y = randint(100,500)
        self.r = randint(30,50)
        if randint(0,10) == 0: 
            self.isSimple = False
        else:
            self.isSimple = True
    
    def draw(self):
        if(self.isSimple):
            circle(screen, self.color, (self.x, self.y), self.r)
        else:          
            polygon(screen, self.color, [(self.x,self.y), (self.x+self.r,self.y),
                                         (self.x+self.r,self.y+self.r), (self.x,self.y+self.r)])
    def clickchek(self, event):
        if(self.isSimple):
            
            return True
        
        return False
    

gscore = gamescore(2)

def new_ball():
    '''рисует новый шарик '''
    global x, y, r, total
    x = randint(100,700)
    y = randint(100,500)
    r = randint(30,50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    total = total + 1
    
def click(event):
    global score,x,y,r
    if( ((x-event.pos[0])**2+(y-event.pos[1])**2) <= r**2):
        score = score + 1

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    screen.blit(my_font.render(('Score: ' + str(score) + '/' + str(total)), False, GREEN) , (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)  

pygame.quit()