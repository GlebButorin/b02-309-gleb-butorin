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
time = 30 #время игры в секундах


def rnd(x,y):
    return(choice(range(x,y)))


class Ball:
    global balls, bullet

    def __init__(self,ball_type, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = ball_type.r
        self.vx = 0
        self.vy = 0
        self.color = ball_type.color
        self.live = ball_type.live_time
        self.g = ball_type.g
        self.f = ball_type.f
        self.k_v = ball_type.k_v
        self.type = ball_type.type

    def move(self):
        #global g
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME +
        self.x += self.vx
        self.y += self.vy
        self.vy -= -self.g + self.vy * self.f
        self.vx -= self.vx * self.f

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
        if self.x + self.r >= 800 and self.vx > 0 or self.x - self.r <= 0 and self.vx < 0:
            self.vx = -self.vx
        if self.y + self.r >= 600 and self.vy > 0 or self.y - self.r <= 0 and self.vy < 0:
            self.vy = -self.vy

    def checklive(self):
        self.live -= 1
        if self.live <= 0:
            self.check_dividing()
            for i in range(len(balls)-1, -1, -1):
                if self == balls[i]:
                    balls.pop(i)

    def check_dividing(self):
        global d2_v, d3_v
        #if self.type == d1:
        if self.type == 'd1':
            for i in range(3):
                new_ball = Ball(dividing2, self.screen, self.x, self.y)
                an = i * math.pi * 2/3
                new_ball.vx = self.vx + math.cos(an)*d2_v
                new_ball.vy = self.vy + math.sin(an)*d2_v
                balls.append(new_ball)
        if self.type == 'd2':
            for i in range(3):
                new_ball = Ball(dividing3, self.screen, self.x, self.y)
                an = i * math.pi * 2/3
                new_ball.vx = self.vx + math.cos(an) * d3_v
                new_ball.vy = self.vy + math.sin(an) * d3_v
                balls.append(new_ball)




class Gun:
    global next_ball
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
        global balls, num_bullets
        num_bullets += 1
        new_ball = Ball(next_ball, self.screen)
        #new_ball.r += 5 зачем это надо???
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an) * new_ball.k_v
        new_ball.vy = self.f2_power * math.sin(self.an) * new_ball.k_v
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        def_next_ball()

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
        vy = self.vy = rnd(-20, 20)
        r = self.r = rnd(10, 40)
        color = self.color = RED

    def hit(self):

        global balls
        global num_bullets
        global points

        """Попадание шарика в цель."""
        points += 1
        self.new_target()
        screen.fill(WHITE)
        gun.draw()
        for t in targets:
            if t != self:
                t.draw()
        score.draw()
        for b in balls:
            b.draw()
        #text1 = pygame.font.SysFont('score', 30)
        #img1 = text1.render('Вы уничтожили цель за ' + str(num_bullets) + ' выстрелов', True, 'BLUE')
        #screen.blit(img1, (200, 200))
        #pygame.display.update()
        #pygame.time.delay(1000)
        self.live = 1
        num_bullets = 0

    def move(self):
        self.y += self.vy

    def wall_collide(self):
        if self.y + self.r >= 600 or self.y - self.r <= 0:
            self.vy = -self.vy

    def draw(self):
        pygame.draw.circle(screen, BLACK, [self.x, self.y], self.r+1)
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.r)


class Score:
    global points

    def __init__(self, screen):
        self.text = pygame.font.SysFont('score', 72)

    def draw(self):
        img = self.text.render(str(points), True, BLUE)
        screen.blit(img, (20, 20))

class Ball_text:
    global next_ball
    def __init__(self, screen):
        self.text = pygame.font.SysFont('next', 36)

    def draw_next(self):
        img = self.text.render('Next:', True, BLACK)
        screen.blit(img, (580, 20))
        pygame.draw.circle(screen, next_ball.color, (670, 35), 15)


class Ball_type:
    def __init__(self, color, type, live_time, r, g, f, k_v):
        self.type = type
        self.color = color
        self.live_time = live_time
        self.r = r
        self.g = g #гравитация
        self.f = f #трение
        self.k_v = k_v #начальная скорость


def def_next_ball():
    global next_ball
    next_ball = choice(ball_types)

def timer():
    global time
    global time_is_up
    text = pygame.font.SysFont(None, 36)
    t0 = pygame.time.get_ticks()
    t = time - int(t0/1000)
    sec = t % 60
    min = (t - sec) // 60
    img = text.render('time left:     ' + str(min) + ':' + str(sec//10) + str(sec%10), True, BLACK)
    screen.blit(img, (300, 20))

    if t <= 0:
        time_is_up = True

def game_over():
    text = pygame.font.SysFont('times new roman', 48)
    img = text.render('GAME OVER', True, 'RED')
    screen.blit(img, (290, 200))
    pygame.display.update()

bouncy = Ball_type(GREEN, 'b', 150, 10, 0.5, 0, 1.5)
heavy = Ball_type(BLACK, 'h', 90, 50, 2.5, 0.04, 0.8)
normal = Ball_type(YELLOW,'n',  90, 20, 1.5, 0.03, 1.0)
dividing1 = Ball_type(BLUE,'d1',  40, 24, 1.5, 0.01, 1.0)
dividing2 = Ball_type(BLUE,'d2',  40, 16, 1.5, 0.02, 1.0)
dividing3 = Ball_type(BLUE, 'd3', 40, 8, 1.5, 0.02, 1.0)
ball_types = [bouncy, heavy, normal, dividing1]
d2_v = 15
d3_v = 10





pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
num_bullets = 0
points = 0
balls = []
targets = []
def_next_ball()

clock = pygame.time.Clock()
gun = Gun(screen)
ball_text = Ball_text(screen)
for i in range(2):
    targets.append(Target(screen))
score = Score(screen)
finished = False
time_is_up = False

while not finished and not time_is_up:
    screen.fill(WHITE)
    gun.draw()
    for target in targets:
        target.draw()
    score.draw()
    ball_text.draw_next()
    for b in balls:
        b.draw()
    timer()
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
    for target in targets:
        target.move()
        target.wall_collide()

    for b in balls:
        b.checklive()
        b.move()
        b.wall_collide()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
    gun.power_up()
if time_is_up:
    game_over()
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True


pygame.quit()
