import math
import time
import pygame as pg

from configurator import *
from vector import Vector

title = "М1 Полет камня"

settings = {
    "Начальная скорость v0 (м/с)": (0, 1_000_000),
    "Угол запуска fi (гр.)": (0, 90),
    "Ускорение свободного падения g (м/с^2)" : (1, 100),
    "Коеффициент линейного сопротивнения воздуха k1 (кг/с)" : (0, 10),
    "Коеффициент квадратичного сопротивнения воздуха k2 (кг/м)" : (0, 1),
    "Масса m (кг)": (0.001, 10000),
}

to_rads = lambda deg: deg * math.pi / 180

screen_size = (1200, 600)
ground_y = 500
start = Vector(50, ground_y)
stone_rad = 5

screen_color = (127, 192, 255)
ground_color = (127, 255, 127)
stone_color = (127, 127, 127)
trace_color = (192, 63, 63)

if __name__ == "__main__":
    data = list(configurate(title, settings, quick_mode=False).values())
    if data == []:
        exit()

    ground = pg.rect.Rect(0, ground_y, screen_size[0], screen_size[1] - ground_y)
    stone_pos = 1 * start
    stone_vel = data[0] * Vector(math.cos(to_rads(data[1])), -math.sin(to_rads(data[1])))
    stone_acc = gravity_acc = Vector(0, data[2])

    peak = 0

    eps = 1e-3
    trace = []
    times = []
    runtime = 0
    while stone_pos.y <= ground_y:
        trace.append(1 * stone_pos)
        times.append(runtime)

        stone_acc = gravity_acc - stone_vel * (data[3] + abs(stone_vel) * data[4]) / data[5]
        delta_time = eps * min(1, abs(stone_vel) / abs(stone_acc))
        runtime += delta_time

        old_vel = 1 * stone_vel
        stone_vel += stone_acc * delta_time

        if old_vel.y * stone_vel.y < 0:
            print("Время пика (с):", round(runtime, 2))
            print("Макс высота (м):", round(-(stone_pos.y - start.y), 3))
            peak = stone_pos.y
        
        stone_pos += stone_vel * delta_time

        if stone_pos.y > ground_y:
            print("Пройденное расстояние (м):", round(stone_pos.x - start.x, 3))
            print("Время полета (с):", round(runtime, 2))

    zoom = min((screen_size[0] - 2 * start.x) / (stone_pos.x - start.x), ground_y / (ground_y - peak))
    speed = runtime / 5

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
        stone_pos = (trace[moment] - start) * zoom + start

        win.fill(screen_color)

        pg.draw.rect(win, ground_color, ground)
        for t_pos in trace[::max(1, len(trace) // 1000)]:
            zoomed = (t_pos - start) * zoom + start
            pg.draw.circle(win, trace_color, (zoomed.x, zoomed.y), 1)
        pg.draw.circle(win, stone_color, (stone_pos.x, stone_pos.y), stone_rad)

        pg.display.flip()
