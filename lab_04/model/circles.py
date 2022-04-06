from math import sqrt, cos, sin, pi


def save_points(x, y, x_c, y_c, xxx, yyy):
    xxx.append(x_c + x)
    yyy.append(y_c + y)
    xxx.append(x_c + x)
    yyy.append(y_c - y)
    xxx.append(x_c - x)
    yyy.append(y_c + y)
    xxx.append(x_c - x)
    yyy.append(y_c - y)

    xxx.append(x_c + y)
    yyy.append(y_c + x)
    xxx.append(x_c + y)
    yyy.append(y_c - x)
    xxx.append(x_c - y)
    yyy.append(y_c + x)
    xxx.append(x_c - y)
    yyy.append(y_c - x)


def bresenham_circle(x_c, y_c, radius):
    x = 0
    y = radius

    delta_i = 2 * (1 - radius)

    eps = 0

    xxx = []
    yyy = []

    while (x <= y):
        save_points(x, y, x_c, y_c, xxx, yyy)

        if (delta_i <= 0):
            eps = 2 * delta_i + 2 * y - 1

            if (eps < 0):
                param = 1
            else:
                param = 2
        elif (delta_i > 0):
            eps = 2 * delta_i - 2 * x - 1

            if (eps < 0):
                param = 2
            else:
                param = 3

        if (param == 1):
            x = x + 1
            delta_i = delta_i + 2 * x + 1
        elif (param == 2):
            x = x + 1
            y = y - 1
            delta_i = delta_i + 2 * x - 2 * y + 2
        else:
            y = y - 1
            delta_i = delta_i - 2 * y + 1

    return xxx, yyy


def canon_circle(x_c, y_c, radius):
    xxx = []
    yyy = []

    edge = round(radius / sqrt(2))

    double_radius = radius * radius

    x = 0

    while x <= edge:
        y = round(sqrt(double_radius - x * x))

        save_points(x, y, x_c, y_c, xxx, yyy)
        x += 1

    return xxx, yyy


def mid_dot_circle(x_c, y_c, radius):
    xxx = []
    yyy = []

    x = 0
    y = radius

    delta = 1 - radius

    while (x <= y):
        save_points(x, y, x_c, y_c, xxx, yyy)

        x += 1

        if (delta < 0):
            delta = delta + 2 * x + 1
        else:
            y -= 1
            delta = delta + 2 * (x - y) + 1

    return xxx, yyy


def parametric_circle(x_c, y_c, radius):
    xxx = []
    yyy = []

    print(radius)
    if radius == 0:
        return [], []

    step = 1 / radius

    alpha = 0

    while (alpha < pi / 4 + step):
        x = round(radius * cos(alpha))
        y = round(radius * sin(alpha))

        save_points(x, y, x_c, y_c, xxx, yyy)

        alpha += step

    return xxx, yyy


FUNC_METHODS = [canon_circle, parametric_circle, bresenham_circle, mid_dot_circle]