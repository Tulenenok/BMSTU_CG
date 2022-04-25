import math

from view.CanvasSegment import CanvasSegment
from view.CanvasPoint import CanvasPoint


def fillWithPartition(segments):               # segments -- массив отрезков типа CanvasSegments
    coords_x = []
    coords_y = []

    for s in segments:
        # используем fieldLine чтобы юзать координаты канвы
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

    x_partition = min_x + (max_x - min_x) // 2
    print('x_partition =', x_partition)
    print('min_x, max_x =', min_x, max_x)

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

    return pixels



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