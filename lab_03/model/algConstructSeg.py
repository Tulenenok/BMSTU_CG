""" Реализация алгоритмов построения отрезков """
import math
from model.Tools import *
from model.lines import *

""" 
1. ЦДА (цифровой дифференциальный анализатор)
Main idea: 
Py = YEnd - YStart           полное приращение по оси Y
Px = XEnd - XStart           полное приращение по оси X

Рассчитываем единиченое приращение
N = max(abs(Py), abs(Px))  количество узлов
dx = Px / N
dy = Py / N

Начинаем рисовать точки
Начальная XStart, YEnd
Потом прибавляем dx и dy, пока не дойдем до XEnd, YEnd
"""


def CDA(xStart, yStart, xEnd, yEnd):
    if xStart == xEnd and yStart == yEnd:
        return [(xStart, yStart), (xEnd, yEnd)]

    x, y = dda_line(xStart, yStart, xEnd, yEnd)

    return [(x[i], y[i]) for i in range(len(x))]

    # Px = xEnd - xStart
    # Py = yEnd - yStart
    #
    # N = max(abs(Py), abs(Px))
    #
    # dx = Px / N
    # dy = Py / N
    #
    # points = []
    # i = 0
    # countsSteps = 1
    # while i < N:
    #     points.append((math.floor(xStart), math.floor(yStart)))
    #     xStart += dx
    #     yStart += dy
    #     i += 1
    #
    #     if not ((round(xStart + dx) == round(xStart) and
    #              round(yStart + dy) != round(yStart)) or
    #             (round(xStart + dx) != round(xStart) and
    #              round(yStart + dy) == round(yStart))):
    #         countsSteps += 1
    #
    # print(f'CDA result = {countsSteps}')
    #
    # return points

def dda_line(xStart, yStart, xEnd, yEnd):
    x, y = xStart, yStart

    x_arr = [math.floor(x)]
    y_arr = [math.floor(y)]

    l = max(abs(xEnd - xStart), abs(yEnd - yStart)) + 1

    for i in range(int(l)):
        x += (xEnd - xStart) / l
        y += (yEnd - yStart) / l

        x_arr.append(math.floor(x))
        y_arr.append(math.floor(y))

    return x_arr, y_arr

"""
2. Брезенхэм вещественные числа
alpha = (yEnd - yStart) / (xEnd - xStart)  угловой коэффициент
Изначально заполняем xStart, yStart, значение ошибки = 0

На каждом шаге к ошибке прибавляется угловой коэффициент и идет анализ:
    - если значение ошибки на i-том шаге < 0.5, то заполняется ячейка (x + 1, y)
    - если > 0.5, то ячейка (x + 1, y + 1) и из значения ошибки вычитается 1
    
Как распространить алгоритм на все направления:
    1. Зеркальные отражения (шаг не 1, а -1)
    2. Обмен переменных x и y
    3. Обмен Start и End
"""

def BresenhamRealSteps(xStart, yStart, xEnd, yEnd):
    x, y = BresenhamWrap(xStart, yStart, xEnd, yEnd, method=BresenhamInt)

    countSteps = 1
    prevTg = 0
    for i in range(1, len(x)):
        nowTg = findTg(round(x[i - 1]), round(x[i]), round(y[i - 1]), round(y[i]))
        countSteps += i != 1 and math.fabs(nowTg - prevTg) > 0.000001
        prevTg = nowTg

    return countSteps

"""
print('float')
alpha = (yEnd - yStart) / (xEnd - xStart)

flagRotate = False
if abs(alpha) > 1:
    flagRotate = True
    xStart, yStart = yStart, xStart
    xEnd, yEnd = yEnd, xEnd

alpha = (yEnd - yStart) / (xEnd - xStart)

error = 0
pointsX = [xStart]
pointsY = [yStart]

while xStart < xEnd:
    error += alpha
    xStart += 1
    if error >= 0.5:
        yStart += 1
        error -= 1
    pointsX.append(math.floor(xStart))
    pointsY.append(math.floor(yStart))

if flagRotate:
    return pointsY, pointsX

return pointsX, pointsY
"""


"""
3. Брезенхэм целые числа
Идея в том, чтобы по-другому высчитывать значение ошибки, чтобы избавится от вещественных чисел
"""


def findTg(x1, x2, y1, y2):
    k = 1000000000
    return ((y2 - y1) * k + 1) / ((x2 - x1) * k + 1)


def countSteps(xStart, yStart, xEnd, yEnd, method=Tools.M_CDA):
    if method == Tools.M_CDA:
        points = CDA(xStart, yStart, xEnd, yEnd)
        x = [p[0] for p in points]
        y = [p[1] for p in points]
    elif method == Tools.M_BREZENHAM_INT:
        x, y = BresenhamWrap(xStart, yStart, xEnd, yEnd, BresenhamInt)
    elif method == Tools.M_BREZENHAM_FLOAT:
        x, y = BresenhamWrap(xStart, yStart, xEnd, yEnd, BresenhamReal)
    elif method == Tools.M_BREZENHAM_ELIMINATION:
        x, y, i = BresenhamWithout_Wrap(xStart, yStart, xEnd, yEnd)
    elif method == Tools.M_VY:
        x, y = wu_steps([xStart, yStart], [xEnd, yEnd])
    else:
        print('Error with method in steps')
        return -1

    countSteps = 2
    prevTg = 0
    for i in range(1, len(x)):
        if x[i - 1] == x[i] and y[i - 1] == y[i]:
            continue

        nowTg = findTg(x[i - 1], x[i], y[i - 1], y[i])
        countSteps += i != 1 and math.fabs(nowTg - prevTg) > 0.000001
        if i != 1 and math.fabs(nowTg - prevTg) > 0.000001:
            print(prevTg, nowTg)
            print(x[i - 1], x[i], y[i - 1], y[i])
        prevTg = nowTg

    return countSteps // 2

def BresenhamInt(xStart, yStart, xEnd, yEnd):
    return int_bresenham_line(xStart, yStart, xEnd, yEnd)
    # print('int')
    # flagRotate = False
    # if abs((yEnd - yStart) / (xEnd - xStart)) > 1:
    #     flagRotate = True
    #     xStart, yStart = yStart, xStart
    #     xEnd, yEnd = yEnd, xEnd
    #
    # Px = xEnd - xStart
    # Py = yEnd - yStart
    # error = 2 * Py - Px
    # i = Px - 1
    #
    # pointsX = [xStart]
    # pointsY = [yStart]
    #
    # while i >= 0:
    #     xStart += 1
    #     if error >= 1:
    #         yStart += 1
    #         error += 2 * (Py - Px)
    #     else:
    #         error += 2 * Py
    #
    #     pointsX.append(math.floor(xStart))
    #     pointsY.append(math.floor(yStart))
    #
    #     i -= 1
    #
    # if flagRotate:
    #     return pointsY, pointsX
    #
    # return pointsX, pointsY


""" Обертка для метода Брезенхэма [int/float] для правильного расположения концов отрезка """

def BresenhamReal(xStart, yStart, xEnd, yEnd):
    return bresenham_line(xStart, xEnd, yStart, yEnd)

def BresenhamWrap(xStart, yStart, xEnd, yEnd, method=BresenhamReal):
    if method == BresenhamReal:
        return bresenham_line(xStart, xEnd, yStart, yEnd)
    else:
        return int_bresenham_line(xStart, xEnd, yStart, yEnd)
    # if xStart == xEnd and yStart == yEnd:
    #     return [xStart, xEnd], [yStart, yEnd]
    #
    # if xStart == xEnd:
    #     x, y = method(min(yStart, yEnd), xStart, max(yStart, yEnd), xEnd)
    #     return y, x
    #
    # if xStart > xEnd:
    #     xStart, yStart, xEnd, yEnd = xEnd, yEnd, xStart, yStart
    #
    # if yStart <= yEnd:
    #     return method(xStart, yStart, xEnd, yEnd)
    # else:
    #     x, y = method(xStart, -yStart, xEnd, -yEnd)
    #     for i in range(len(y)):
    #         y[i] = -y[i]
    #     return x, y



"""
4. Брезенхэм с устранением ступенчатости
А давайте закрашивать пиксели разными цветами
i — число доступных уровней интенсивности
"""


def BresenhamWithout(xStart, yStart, xEnd, yEnd, i=8):
    print('without')
    flagRotate = False
    if abs((yEnd - yStart) / (xEnd - xStart)) > 1:
        flagRotate = True
        xStart, yStart = yStart, xStart
        xEnd, yEnd = yEnd, xEnd

    Px = xEnd - xStart
    Py = yEnd - yStart

    m = i * Py / Px
    w = i - m
    e = 1 / 2

    pointsX = [xStart]
    pointsY = [yStart]
    intens = [m / 2]

    while xStart < xEnd:
        xStart += 1
        if e < w:
            e += m
        else:
            yStart += 1
            e -= w

        pointsX.append(math.floor(xStart))
        pointsY.append(math.floor(yStart))
        intens.append(math.ceil(e))                    # а хрен его знает нужно здесь округление или нет

    if flagRotate:
        return pointsY, pointsX, intens

    return pointsX, pointsY, intens


def BresenhamWithout_Wrap(xStart, yStart, xEnd, yEnd, i=8):
    return no_angle_bresenham_line(xStart, xEnd, yStart, yEnd)
    # if xStart == xEnd and yStart == yEnd:
    #     return [xStart, xEnd], [yStart, yEnd], [i, i]
    #
    # """ Обертка для Брезенхема без ступенчатости """
    #
    # if xStart == xEnd:
    #     x, y, e = BresenhamWithout(min(yStart, yEnd), xStart, max(yStart, yEnd), xEnd, i)
    #     return y, x, e
    #
    # if xStart > xEnd:
    #     xStart, yStart, xEnd, yEnd = xEnd, yEnd, xStart, yStart
    #
    # if yStart <= yEnd:
    #     return BresenhamWithout(xStart, yStart, xEnd, yEnd, i)
    # else:
    #     x, y, e = BresenhamWithout(xStart, -yStart, xEnd, -yEnd, i)
    #     for i in range(len(y)):
    #         y[i] = -y[i]
    #     return x, y, e


def wu(p_start, p_end, steps=False):
    if p_start[0] == p_end[0] and p_start[1] == p_end[1]:
        return [p_start[0], p_end[0]], [p_start[1], p_end[1]], [1, 1]

    print('wu')
    pointsX = []
    pointsY = []
    intens = []

    Imax = 255
    dx = p_end[0] - p_start[0]
    dy = p_end[1] - p_start[1]
    m = 1
    shag = 1
    step = 1
    if math.fabs(dy) > math.fabs(dx):
        if dy != 0:
            m = dx / dy
        m1 = m
        if p_start[1] > p_end[1]:
            m1 *= -1
            shag *= -1
        for y in range(round(p_start[1]), round(p_end[1]) + 1, shag):
            d1 = p_start[0] - math.floor(p_start[0])
            d2 = 1 - d1

            pointsX.append(math.floor(p_start[0]))
            pointsY.append(math.floor(y))
            intens.append(round(math.fabs(d2) * Imax) / Imax)

            pointsX.append(math.floor(p_start[0]) + 1)
            pointsY.append(math.floor(y))
            intens.append(round(math.fabs(d1) * Imax) / Imax)

            if steps and y < round(p_end[1]):
                if int(p_start[0]) != int(p_start[0] + m):
                    step += 1
            p_start[0] += m1
    else:
        if dx != 0:
            m = dy / dx
        m1 = m
        if p_start[0] > p_end[0]:
            shag *= -1
            m1 *= -1
        for x in range(round(p_start[0]), round(p_end[0]) + 1, shag):
            d1 = p_start[1] - math.floor(p_start[1])
            d2 = 1 - d1

            pointsX.append(math.floor(x))
            pointsY.append(math.floor(p_start[1]))
            intens.append(round(math.fabs(d2) * Imax) / Imax)

            pointsX.append(math.floor(x))
            pointsY.append(math.floor(p_start[1]) + 1)
            intens.append(round(math.fabs(d1) * Imax) / Imax)

            if steps and x < round(p_end[0]):
                if int(p_start[1]) != int(p_start[1] + m):
                    step += 1
            p_start[1] += m1


    return pointsX, pointsY, intens


def wu_steps(p_start, p_end):
    if p_start[0] == p_end[0] and p_start[1] == p_end[1]:
        return [p_start[0], p_end[0]], [p_start[1], p_end[1]], [1, 1]

    pointsX = []
    pointsY = []

    Imax = 255
    dx = p_end[0] - p_start[0]
    dy = p_end[1] - p_start[1]
    m = 1
    shag = 1
    if math.fabs(dy) > math.fabs(dx):
        if dy != 0:
            m = dx / dy
        m1 = m
        if p_start[1] > p_end[1]:
            m1 *= -1
            shag *= -1
        for y in range(round(p_start[1]), round(p_end[1]) + 1, shag):
            d1 = p_start[0] - math.floor(p_start[0])
            d2 = 1 - d1

            if round(math.fabs(d2) * Imax) / Imax > round(math.fabs(d1) * Imax) / Imax:
                pointsX.append(math.floor(p_start[0]))
                pointsY.append(math.floor(y))
            else:
                pointsX.append(math.floor(p_start[0]) + 1)
                pointsY.append(math.floor(y))

            p_start[0] += m1
    else:
        if dx != 0:
            m = dy / dx
        m1 = m
        if p_start[0] > p_end[0]:
            shag *= -1
            m1 *= -1
        for x in range(round(p_start[0]), round(p_end[0]) + 1, shag):
            d1 = p_start[1] - math.floor(p_start[1])
            d2 = 1 - d1

            if round(math.fabs(d2) * Imax) / Imax > round(math.fabs(d1) * Imax) / Imax:
                pointsX.append(math.floor(x))
                pointsY.append(math.floor(p_start[1]))
            else:
                pointsX.append(math.floor(x))
                pointsY.append(math.floor(p_start[1]) + 1)

            p_start[1] += m1

    return pointsX, pointsY

