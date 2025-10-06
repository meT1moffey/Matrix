import math
import time
import pygame as pg

from configurator import *
from vector import Vector

title = "M2. Бильярд"

settings = {
    "Нач. скорость шара v (м/с)": (0.001, 1000),
    "Масса первого шара m1 (кг)": (0.1, 10),
    "Масса второго шара m2 (кг)": (0.1, 10),
    "Коеффициент для закона Гука (кг/с^2)": (0, 1000),
    "Коеффициент для закона Ньютона (кг/м^0.5/с^2)": (0, 100),
    "Скорость симуляции": (0.001, 1000)
}

simulate_collision = True
subticks = 1_000

screen_size = (1200, 600)
balls_y = 300
border_x = 1100
balls_rad = 25

screen_color = (64, 128, 64)
border_color = (32, 64, 32)
ball1_color = (255, 255, 240)
ball2_color = (240, 32, 32)

pg.font.init()
font = pg.font.SysFont('Comic Sans MS', 30)

if __name__ == "__main__":
    data = list(configurate(title, settings, quick_mode=False).values())
    if data == []:
        exit()

    border = pg.Rect(border_x, 0, screen_size[0] - border_x, screen_size[1])
    ball1_pos = 50
    ball2_pos = 500
    ball1_vel = data[0]
    ball2_vel = 0

    collision_cnt = 0
    
    eps = 1e-4
    trace = []
    times = []
    track = []
    runtime = 0
    while ball1_vel > ball2_vel or ball2_vel > 0 or ball2_pos + balls_rad > 0:
        trace.append((ball1_pos, ball2_pos))
        track.append((ball1_vel, ball2_vel))
        times.append(runtime)

        mutal_deform = balls_rad - (ball2_pos - ball1_pos) / 2
        mutal_force = data[3] * mutal_deform + data[4] * mutal_deform ** 1.5 if mutal_deform > 0 else 0
        border_deform = ball2_pos + balls_rad - border_x
        border_force = data[3] * border_deform + data[4] * border_deform ** 1.5 if border_deform > 0 else 0

        ball1_acc = -mutal_force / data[1]
        ball2_acc = (mutal_force - border_force) / data[2]

        if ball1_acc != 0 or ball2_acc != 0:
            delta_time = eps * (abs(ball1_vel) + abs(ball2_vel) + eps) / (abs(ball1_acc) + abs(ball2_acc) + eps)
        else:
            delta_time = eps
        
        delta_time = min(eps, delta_time)
        runtime += delta_time

        ball1_vel += ball1_acc * delta_time        
        ball2_vel += ball2_acc * delta_time
        ball1_pos += ball1_vel * delta_time
        ball2_pos += ball2_vel * delta_time

    speed = runtime / 10

    pg.init()
    win = pg.display.set_mode(screen_size)
    pg.display.set_caption(title)

    moment = 0
    running = True
    start_time = prev_time = time.time()
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
        
        while moment < len(times) - 1 and times[moment] < (time.time() - start_time) * speed:
            moment += 1
        ball1_pos, ball2_pos = trace[moment]
        
        win.fill(screen_color)

        pg.draw.rect(win, border_color, border)
        pg.draw.circle(win, ball1_color, (ball1_pos, balls_y), balls_rad)
        pg.draw.circle(win, ball2_color, (ball2_pos, balls_y), balls_rad)
        win.blit(font.render(f"Скорость левого шара: {track[moment][0]:.2f} м/с", False, ball1_color), (10, 10))
        win.blit(font.render(f"Скорость правого шара: {track[moment][1]:.2f} м/с", False, ball2_color), (10, 60))
        win.blit(font.render(f"Общая кинетическая энегрия: {(data[1] * track[moment][0] ** 2 + data[2] * track[moment][1] ** 2) / 2e3:.2f} КДж", False, (0, 0, 0)), (10, 110))

        pg.display.flip()
