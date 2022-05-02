import math

from view.CanvasSegment import CanvasSegment
from view.CanvasPoint import *
import time


def colorPixelOnCanva(x, y, canva, colorBorder):
    try:
        allFigures = canva.find_overlapping(x - 0.5, y, x + 0.5, y)
        c1 = canva.itemcget(allFigures[-1], "fill")
        if c1 == colorBorder:
            return colorBorder
        return c1
    except:
        return Settings.COLOR_CANVA


def settingsColor(border, fill):
    print(border, fill)

    if border != fill:
        return border, fill

    if border == '#000000':
        return border, '#000001'

    if str(border).lower() == '#ffffff':
        return border, '#fffffe'

    r, g, b = int(border[1:3], 16), int(border[3:5], 16), int(border[5:7], 16)
    b += 1
    rh = '0' + str(hex(int(r * 255))[2:].lower())
    gh = '0' + str(hex(int(g * 255))[2:].lower())
    bh = '0' + str(hex(int(b * 255))[2:].lower())

    return border, f'#{rh[-2:]}{gh[-2:]}{bh[-2:]}'


def findNextStackPoints(x, y, xmax, ymax, xmin, ymin, borders, wasFill):
    stack = []
    if x == xmax - 1 or (x + 1, y) in borders:
        if y < ymax - 1:
            if (x, y + 1) not in borders and (x, y + 1) not in wasFill:
                stack.append((x, y + 1))
        if y > ymin:
            if (x, y - 1) not in borders and (x, y - 1) not in wasFill:
                stack.append((x, y - 1))
    else:
        if y < ymax - 1:
            if (x + 1, y + 1) in borders:
                stack.append((x, y + 1))
        if y > ymin:
            if (x + 1, y - 1) in borders:
                stack.append((x, y - 1))
                
    return stack


def fillRowPixels(xSeed, ySeed, canva, colorBorder, colorFill, borders, wasFill, delay=False, cutPixels=[]):
    fillPixels = []
    setCoord = set()
    stackPoints = []

    xLeft = math.floor(xSeed)
    # бежим влево, пока не дойдем до границы закраски или до конца холста
    while xLeft >= 0 and (xLeft, ySeed) not in borders:
        if (xLeft, ySeed) in wasFill:
            xLeft -= 1
            continue

        setCoord.add((xLeft, ySeed))

        if (xLeft, ySeed) not in cutPixels:
            newPix = Pixel(x=xLeft, y=ySeed, color=colorFill)
            fillPixels.append(newPix)

            if delay:
                newPix.show(canva)
                canva.update()
        
        stackPoints += findNextStackPoints(xLeft, ySeed, canva.winfo_width(), canva.winfo_height(), 0, 0, borders, wasFill)

        xLeft -= 1

    xRight = math.ceil(xSeed)
    while xRight <= canva.winfo_width() and (xRight, ySeed) not in borders:
        if (xRight, ySeed) in wasFill:
            xRight += 1
            continue

        setCoord.add((xRight, ySeed))

        if (xRight, ySeed) not in cutPixels:
            newPix = Pixel(x=xRight, y=ySeed, color=colorFill)
            fillPixels.append(newPix)

            if delay:
                newPix.show(canva)
                canva.update()

        stackPoints += findNextStackPoints(xRight, ySeed, canva.winfo_width(), canva.winfo_height(), 0, 0, borders, wasFill)

        xRight += 1

    return xLeft, xRight, fillPixels, setCoord, stackPoints


def fillWithPartitionWithDelay(segments, canva, setCutPixels=[],
                               startPixel=Pixel(x=0, y=0, color=Settings.COLOR_HOVER_BTN),
                               colorBorder=Settings.COLOR_LINE,
                               delay=False):
    if len(segments) == 0:
        print('Пустой массив отрезков')
        return []

    colorFill = startPixel.color

    # Собираем все пиксели на границах в одно множество, чтобы потом проверять, дошли мы до границы или нет
    allPixelsOnBorder = set()
    for s in segments:
        allPixelsOnBorder = allPixelsOnBorder.union(s.pixSet)

    stackSeed = [(startPixel.x, startPixel.y)]

    allPixels = []
    fillPixCoor = set()             # пиксели, которые уже были закрашены, чтобы эти строчки сразу пропускать
    while len(stackSeed) > 0:
        workPixel = stackSeed.pop()

        if workPixel in allPixelsOnBorder:
            print('border')
            continue

        if workPixel in fillPixCoor:
            print('fill')
            continue


        xL, xR, p, s, nextStack = fillRowPixels(workPixel[0], workPixel[1], canva,
                                     colorBorder=colorBorder, colorFill=colorFill,
                                     borders=allPixelsOnBorder, wasFill=fillPixCoor, delay=delay, cutPixels=setCutPixels)
        # if delay:
        #     canva.update()

        allPixels += p
        fillPixCoor = fillPixCoor.union(s)

        stackSeed += nextStack

        # if delay:
        #     time.sleep(0.2)

    return allPixels


def fillWithPartition(segments, startPoint=Pixel(x=0, y=0)):
    coords_x = []
    coords_y = []

    for s in segments:
        try:
            coords_x += [s.fieldLine.start.x, s.fieldLine.end.x]
            coords_y += [s.fieldLine.start.y, s.fieldLine.end.y]
        except:
            coords_x += [s.start.x, s.end.x]
            coords_y += [s.start.y, s.end.y]
            print('Нет перевода в координаты канвы при закраске')

    min_x, max_x = min(coords_x), max(coords_x)
    min_y, max_y = min(coords_y), max(coords_y)

    pixels = dict()
    #listPixels = []

    x_partition = min_x + (max_x - min_x) // 2
    # print('x_partition =', x_partition)
    # print('min_x, max_x =', min_x, max_x)

    partition = CanvasSegment(CanvasPoint(x_partition, min_y), CanvasPoint(x_partition, max_y))

    for y in range(math.floor(min_y), math.floor(max_y) + 1):              # пробегаем горизонтальными линиями
        for s in segments:
            try:
                if y == min(math.floor(s.fieldLine.start.y), math.floor(s.fieldLine.end.y)):
                    continue

                if s.fieldLine.A == 0:
                    continue

            except:
                if s.A == 0:                                               # горизонтальные отрезки мы пропускаем
                    continue

            try:
                # горизонтальная прямая не пересекает отрезок
                if math.floor(min(s.fieldLine.start.y, s.fieldLine.end.y)) > y or math.floor(max(s.fieldLine.start.y, s.fieldLine.end.y)) < y:
                    continue

                intersection_segment = s.fieldLine.findXByY(y)             # пересечение с ребром
                intersection_partition = partition.findXByY(y)             # пересечение с перегородкой
            except:
                # горизонтальная прямая не пересекает отрезок
                if math.floor(min(s.start.y, s.end.y)) > y or math.floor(
                        max(s.start.y, s.end.y)) < y:
                    continue

                intersection_segment = s.findXByY(y)                       # пересечение с ребром
                intersection_partition = partition.findXByY(y)             # пересечение с перегородкой

            min_inter = round(min(intersection_segment, intersection_partition))
            max_inter = round(max(intersection_segment, intersection_partition))

            # min_point_in_seg = round(min(s.start.x, s.end.x))
            # max_point_in_seg = round(max(s.start.x, s.end.x))

            # закрашиваем пиксели между ними
            for x in range(min_inter, max_inter):
                if min_x <= x <= max_x:
                    pixels[(x, y)] = True if (x, y) not in pixels else not pixels[(x, y)]

            # for p in pixels.keys():
            #     if pixels[p]:
            #         listPixels.append(p)

    return pixels  #, listPixels



# segments -- массив отрезков типа (x_старт, y_старт, x_конец, y_конец)
def wrapFillWithPartition(segments):
    newSegments = []
    for s in segments:
        newSegments.append(CanvasSegment(CanvasPoint(s[0], s[1]), CanvasPoint(s[2], s[3])))

    return fillWithPartition(newSegments)


def linesFillWithPartition(segments):
    newSegments = []
    for s in segments:
        newSegments.append(CanvasSegment(CanvasPoint(s[0], s[1]), CanvasPoint(s[2], s[3])))

    return fillWithPartition(newSegments)


# seg = [(0, 2, 2, 4), (2, 4, 4, 2), (4, 2, 2, 0), (2, 0, 0, 2)]
# print(wrapFillWithPartition(seg))