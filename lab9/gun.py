import math
from random import choice
from random import randint as rnd

import pygame

TARGET_COUNT = 2
SPEED_MULT = 30
GRAVITY = 0.15
DISSIPATION = 0.3

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


def hypot(x1, x2, y1, y2):  # расстояние между двумя точками
    return ((x1-x2)**2+(y1-y2)**2)**0.5


class Ball:
    """
    Класс снаряда
    """
    def __init__(self, screen: pygame.Surface, xy=(40, 450), sballtype=0):
        """
        Конструктор класса ball

        Args:
        xy - начальное положение мяча
        sballtype - тип мяча (влияет его размер)
        """
        self.screen = screen
        self.pos = list(xy)
        self.r = 5
        self.vel = [0, 0]
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.ignited = False
        self.balltype = sballtype
        if sballtype == 1:
            self.r = 10
        elif sballtype == 2:
            self.r = 20

    def setVel(self, angl, power):
        """
        Сообщает мячу скорость power под углом angl
        """
        self.vel = [power * math.cos(angl), power * math.sin(angl)]

    def move(self, dtime=100):
        """
        Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки.
        То есть обновляет значения self.pos с учетом скоростей
        self.vel, силы гравитации, действующей на мяч
        и стен по краям окна (размер окна 800х600).
        """
        self.pos[0] += self.vel[0] * dtime
        self.pos[1] += self.vel[1] * dtime
        self.vel[1] += GRAVITY * dtime

        if self.pos[0] + self.r >= WIDTH:
            self.vel[0] = -abs(self.vel[0]) * (1 - DISSIPATION)
            self.vel[1] *= (1 - DISSIPATION) ** 2
        elif self.pos[0] <= self.r:
            self.ignite()
        if self.pos[1] + self.r >= HEIGHT:
            self.vel[1] = -abs(self.vel[1]) * (1 - DISSIPATION)
            self.vel[0] *= (1 - DISSIPATION) ** 2
            # если мяч лежит на полу и почти остановился:
            if self.vel[0]**2 + self.vel[1]**2 <= 2:
                self.ignite()  # то удалить его
        # крыши нет

    def draw(self):
        """
        Рисуем этот снаряд
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.pos[0], self.pos[1]),
            self.r)

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
        return hypot(obj.x, self.pos[0], obj.y, self.pos[1]) <= self.r + obj.r

    def ignite(self):
        """
        Снаряд взорвался и теперь неактивный
        """
        self.ignited = True


class Gun:
    """
    Класс танка
    """
    def __init__(self, screen, color1=RED, color2=YELLOW):
        """
        color1 - цвет шкалы
        color2 - цвет шкалы FIXME
        """
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
        """
        Начинаем копить силу выстрела
        при нажатии кнопки мыши.
        """
        self.f2_on = 1

    def fire2_end(self, event):
        """
        Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости
        мяча vx и vy зависят от положения мыши.
        """
        myGame.bullet += 1
        new_ball = Ball(self.screen, self.getGunEndFixed(), self.balltype)
        self.an = math.atan2((event.pos[1]-new_ball.pos[1]),
                             (event.pos[0]-new_ball.pos[0]))
        new_ball.setVel(self.an, self.f2_power)
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
        """
        Рисует танк
        """
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

    def getGunEndFixed(self):
        """
        Возвращает координаты конца пушки
        """
        return (self.pos[0] + 20 * math.cos(self.an),
                self.pos[1] + 20 * math.sin(self.an))

    def power_up(self):
        """
        Увеличение силы выстрела
        при удерживании клавиши сыши
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = self.color2
        else:
            self.color = self.color1

    def turn(self, dx, dy):
        """
        Включить движение
        """
        self.vel[0] = dx * 10
        self.vel[1] = -dy * 10

    def move(self, dtime=100):
        """
        Перемещение танка за время dtime
        """
        self.pos[0] += self.vel[0] * dtime
        self.pos[1] += self.vel[1] * dtime

        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.vel[0] = 0
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.vel[1] = 0

    def changebullet(self, bultype):
        """
        Поменять тип снарядов
        """
        self.balltype = bultype


class Target:
    """
    Класс мишени
    """
    def __init__(self, screen):
        """ Инициализация новой цели """
        self.screen = screen

        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.color1 = choice(GAME_COLORS)
        self.color2 = self.color1
        while self.color2 == self.color1:
            self.color2 = choice(GAME_COLORS)

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
        pygame.draw.circle(
            self.screen,
            self.color1,
            (self.x, self.y),
            self.r
            )
        pygame.draw.circle(
            self.screen,
            self.color2,
            (self.x, self.y),
            self.r/2
            )

    def move(self, dtime=100):
        """Перемещение мишени за время dtime"""
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
    """
    Главный класс
    """
    def __init__(self, screen, tmax=1):
        self.screen = screen

        self.bullet = 0
        self.balls = []
        self.targets = [Target(screen) for _ in range(tmax)]
        self.targetsMax = tmax
        self.dtm = 100

        self.gun = Gun(screen)

    def drawBallsAndTargets(self):
        """
        Рисует игровые объекты (мячи и мишени) на экране
        """
        for b in self.balls:
            b.draw()
        for t in self.targets:
            t.draw()

    def drawGun(self):
        """
        Рисует танк
        """
        self.gun.draw()

    def checking(self):
        """
        Ищет попадания мяча в мишень
        При попадании удаляет старую и создаёт новую мишень, удаляет снаряд
        """
        for t in self.targets:
            t.move(self.getInterval())
        for b in range(len(self.balls)):
            b.move(self.getInterval())
            for i in range(len(self.targets)):
                if self.balls[b].hittest(self.targets[i]):
                    if self.targets[i].hit():
                        self.targets[i] = Target(screen)
                        self.balls[b].ignite()
        try:
            for b in range(len(self.balls))[::-1]:
                if self.balls[b].ignited:
                    del self.balls[b]
        except IndexError:
            pass

    def delay(self):
        """
        Ждёт некторое время перед следующей отрисовкой
        """
        self.dtm = clock.tick(FPS)

    def getInterval(self):
        """
        Возвращает время, прошедшее с последней отрисовки
        """
        return self.dtm/SPEED_MULT

    def keyAction(self, event):
        """Обработка нажатия на клавишу"""
        if event.key == pygame.K_RIGHT:
            self.gun.turn(1, 0)
        elif event.key == pygame.K_LEFT:
            self.gun.turn(-1, 0)
        elif event.key == pygame.K_UP:
            self.gun.turn(0, 1)
        elif event.key == pygame.K_DOWN:
            self.gun.turn(0, -1)
        elif event.key == pygame.K_1:
            self.gun.changebullet(0)
        elif event.key == pygame.K_2:
            self.gun.changebullet(1)
        elif event.key == pygame.K_3:
            self.gun.changebullet(2)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False

myGame = Game(screen, TARGET_COUNT)

while not finished:
    screen.fill(WHITE)
    myGame.drawGun()
    myGame.drawBallsAndTargets()
    pygame.display.update()
    myGame.delay()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            myGame.gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            myGame.gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            myGame.gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            myGame.keyAction(event)
        elif event.type == pygame.KEYUP:
            myGame.gun.turn(0, 0)

    myGame.checking()
    myGame.gun.move(myGame.getInterval())
    myGame.gun.power_up()

pygame.quit()
