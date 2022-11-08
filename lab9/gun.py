import math
from random import choice
from random import randint as rnd

import pygame

TARGET_COUNT = 2
SPEED_MULT = 30
GRAVITY = 0.15

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


def hypot(x1, x2, y1, y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450, sballtype=0):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.ignited = False
        self.balltype = sballtype
        if sballtype == 1:
            self.r = 10
        elif sballtype == 2:
            self.r = 20

    def move(self, dtime=100):
        """
        Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки.
        То есть обновляет значения self.x и self.y с учетом скоростей
        self.vx и self.vy, силы гравитации, действующей на мяч
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx * dtime
        self.y += self.vy * dtime
        self.vy += GRAVITY * dtime

        if self.x > WIDTH or self.x < 0:
            self.vx = -self.vx
        if self.y > HEIGHT or self.y < 0:
            self.vy = -self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """
        Функция проверяет, сталкивалкивается ли
        данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели.
            В противном случае возвращает False.
        """
        return hypot(obj.x, self.x, obj.y, self.y) <= self.r + obj.r

    def ignite(self):
        self.ignited = True


class Gun:
    def __init__(self, screen, color1=RED, color2=YELLOW):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color1 = color1
        self.color2 = color2
        self.color = color1
        self.pos = [40, 450]
        self.vel = [0, 0]
        self.balltype = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """
        Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости
        мяча vx и vy зависят от положения мыши.
        """
        myGame.bullet += 1
        gunend = self.getGunEnd()
        new_ball = Ball(self.screen, gunend[0], gunend[1], self.balltype)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y),
                             (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        myGame.balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-self.pos[1]),
                                 (event.pos[0]-self.pos[0]))
        if self.f2_on:
            self.color = self.color2
        else:
            self.color = self.color1

    def draw(self):
        pygame.draw.line(self.screen, GREY,
                         self.pos, self.getGunEndFixed(), 5)
        pygame.draw.rect(self.screen, GREY,
                         [self.pos[0]-5, self.pos[1] - 5, 10, 10])
        pygame.draw.rect(self.screen, GREY,
                         [self.pos[0]-10, self.pos[1] + 5, 20, 10])
        pygame.draw.line(self.screen, self.color,
                         [self.pos[0]-10, self.pos[1] - 10],
                         [self.pos[0] - 10 + 0.2 * self.f2_power,
                          self.pos[1] - 10], 5)

    def getGunEnd(self):
        return (self.pos[0] + self.f2_power * math.cos(self.an),
                self.pos[1] + self.f2_power * math.sin(self.an))

    def getGunEndFixed(self):
        return (self.pos[0] + 20 * math.cos(self.an),
                self.pos[1] + 20 * math.sin(self.an))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = self.color2
        else:
            self.color = self.color1

    def turn(self, dx, dy):
        self.vel[0] = dx * 10
        self.vel[1] = -dy * 10

    def move(self, dtime=100):
        self.pos[0] += self.vel[0] * dtime
        self.pos[1] += self.vel[1] * dtime

        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.vel[0] = 0     # -self.vel[0]
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.vel[1] = 0     # -self.vel[1]

    def changebullet(self, bultype):
        self.balltype = bultype


class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.color1 = choice(GAME_COLORS)  # RED
        self.color2 = choice(GAME_COLORS)  # YELLOW

        self.vx = rnd(0, 2)
        self.vy = rnd(0, 2)

        self.points = 0
        self.live = 1

        self.isSimple = True
        if rnd(0, 10) == 0:
            self.isSimple = False  # motion: random

    def hit(self, points=1, lives=1):
        """Попадание шарика в цель."""
        self.live -= lives
        self.points += points
        return self.live <= 0

    def draw(self):
        global screen
        pygame.draw.circle(
            screen,
            self.color1,
            (self.x, self.y),
            self.r
            )
        pygame.draw.circle(
            screen,
            self.color2,
            (self.x, self.y),
            self.r/2
            )

    def move(self, dtime=100):
        if not self.isSimple:
            if abs(self.vx) > 6:
                self.vx = 0
            if abs(self.vy) > 6:
                self.vy = 0
            self.vx += rnd(-1, 1)
            self.vy += rnd(-1, 1)

        self.x += self.vx * dtime
        self.y += self.vy * dtime
        self.vy += GRAVITY * dtime

        if self.x >= WIDTH - self.r or self.x <= self.r:
            self.vx = -self.vx
        if self.y >= HEIGHT - self.r or self.y <= self.r:
            self.vy = -self.vy


class Game:
    def __init__(self, tmax=1):
        self.bullet = 0
        self.balls = []
        self.targets = [Target() for _ in range(tmax)]
        self.targetsMax = tmax
        self.dtm = 100

    def drawBallsAndTargets(self):
        for b in self.balls:
            b.draw()
        for t in self.targets:
            t.draw()

    def checking(self):
        for b in self.balls:
            b.move(self.getInterval())
        for t in self.targets:
            t.move(self.getInterval())
        try:
            for b in range(len(self.balls)):
                for i in range(len(self.targets)):
                    if self.balls[b].hittest(self.targets[i]):
                        if(self.targets[i].hit()):
                            self.targets[i] = Target()
                            self.balls[b].ignite()
                            del self.balls[b]
        except IndexError:
            pass

    def delay(self):
        self.dtm = clock.tick(FPS)

    def getInterval(self):
        return self.dtm/SPEED_MULT


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False

myGame = Game(TARGET_COUNT)
gun = Gun(screen)


while not finished:
    screen.fill(WHITE)
    gun.draw()
    myGame.drawBallsAndTargets()
    pygame.display.update()
    myGame.delay()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                gun.turn(1, 0)
            elif event.key == pygame.K_LEFT:
                gun.turn(-1, 0)
            elif event.key == pygame.K_UP:
                gun.turn(0, 1)
            elif event.key == pygame.K_DOWN:
                gun.turn(0, -1)
            elif event.key == pygame.K_1:
                gun.changebullet(0)
            elif event.key == pygame.K_2:
                gun.changebullet(1)
            elif event.key == pygame.K_3:
                gun.changebullet(2)
        elif event.type == pygame.KEYUP:
            gun.turn(0, 0)
    myGame.checking()
    gun.move(myGame.getInterval())
    gun.power_up()

pygame.quit()
