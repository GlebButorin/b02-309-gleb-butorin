import math
from random import choice

import pygame


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
g = 1


def rnd(x,y):
    return(choice(range(x,y)))

class Ball:
    global balls
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 90

    def move(self):
        global g
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME +
        self.x += self.vx
        self.y -= self.vy
        self.vy -= g + self.vy * 0.02
        self.vx -= self.vx * 0.02

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME +

        if ((self.x-obj.x)**2+(self.y-obj.y)**2) < (self.r+obj.r)**2:
            return True
        else:
            return False


    def wall_collide(self):
        if self.x + self.r >= 800 or self.x - self.r <= 0:
            self.vx = -self.vx
        if self.y + self.r >= 600 or self.y - self.r <= 0:
            self.vy = -self.vy
    def checklive(self):
        self.live -= 1
        if self.live == 0:
            balls.pop(0)


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-450), (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT + don't know how to do it
        # pass
        self.width = 10
        self.length = 20 + self.f2_power
        pygame.draw.polygon(self.screen, self.color, [(20, 450),
                                                      (20+self.length*math.cos(self.an), 450+self.length*math.sin(self.an)),
                                                      (20+self.length*math.cos(self.an)-self.width*math.sin(self.an), 450+self.length*math.sin(self.an)+self.width*math.cos(self.an)),
                                                      (20-self.width*math.sin(self.an), 450+self.width*math.cos(self.an))])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME + : don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = RED

    def hit(self, points=1):

        global balls
        global bullet

        """Попадание шарика в цель."""
        self.points += points
        self.new_target()
        screen.fill(WHITE)
        gun.draw()
        score.draw()
        for b in balls:
            b.draw()
        text1 = pygame.font.SysFont('score', 30)
        img1 = text1.render('Вы уничтожили цель за ' + str(bullet) + ' выстрелов', True, 'BLUE')
        screen.blit(img1, (200, 200))
        pygame.display.update()
        pygame.time.delay(1000)
        self.live = 1
        bullet = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.r)


class Score:
    global target
    def __init__(self, sreen):
        self.text = pygame.font.SysFont('score', 72)
    def draw(self):
        img = self.text.render(str(target.points), True, BLUE)
        screen.blit(img, (20, 20))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
score = Score(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    score.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.checklive()
        b.move()
        b.wall_collide()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
