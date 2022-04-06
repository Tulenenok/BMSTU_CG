import matplotlib.pyplot as plt

from time import *
from model.circles import *
from model.ellipses import *


def measure_time():
    radiuses = [r for r in range(100, 10002, 1000)]

    canon_circle_times = []
    parametric_circle_times = []
    bresenham_circle_times = []
    mid_dot_circle_times = []

    canon_ellips_times = []
    parametric_ellips_times = []
    bresenham_ellipse_times = []
    mid_dot_ellipse_times = []

    tasks1 = '''canon_circle
    parametric_circle
    bresenham_circle
    mid_dot_circle'''

    tasks2 = '''canon_ellips
    parametric_ellips
    bresenham_ellipse
    mid_dot_ellipse'''


    for radius in radiuses:
        for task in tasks1.split('\n'):
            start = time()
            eval(f'{task}(0, 0, {radius})')
            stop = time()
            eval(f'{task}_times.append(stop-start)')


        for task in tasks2.split('\n'):
            start = time()
            eval(f'{task}(0, 0, {radius}, {0.5*radius})')
            stop = time()
            eval(f'{task}_times.append(stop-start)')

    plt.figure(figsize=(15, 6))

    plt.subplot(1, 2, 1)
    plt.title("Замеры для окружностей: ")
    plt.plot(radiuses, canon_circle_times, label="Каноническое\nуравнение")
    plt.plot(radiuses, parametric_circle_times, label="Параметрическое\nуравнение")
    plt.plot(radiuses, bresenham_circle_times, label="Брезенхем")
    plt.plot(radiuses, mid_dot_circle_times, label="Алгоритм\nсредней точки")
    plt.legend()
    plt.ylabel("Время")
    plt.xlabel("Величина радиуса")

    plt.subplot(1, 2, 2)
    plt.title("Замеры для эллипсов: ")
    plt.plot(radiuses, canon_ellips_times, label="Каноническое\nуравнение")
    plt.plot(radiuses, parametric_ellips_times, label="Параметрическое\nуравнение")
    plt.plot(radiuses, bresenham_ellipse_times, label="Брезенхем")
    plt.plot(radiuses, mid_dot_ellipse_times, label="Алгоритм\nсредней точки")
    plt.legend()
    plt.ylabel("Время")
    plt.xlabel("Величина радиуса")

    plt.show()