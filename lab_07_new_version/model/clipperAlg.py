import math
from view.CanvasPoint import Pixel

# xLeft              yDown
# ---------------------
# |                   |
# |                   |
# ---------------------
# yUp                xRight


def findT(p, xLeft, xRight, yDown, yUp):
    return [p[0] < xLeft, p[0] > xRight, p[1] < yDown, p[1] > yUp]


def findS(t):
    return sum(t)


def findP(t1, t2):
    sum = 0
    for i in range(len(t1)):
        sum += t1[i] * t2[i]
    return sum


def findAll(p1, p2, xLeft, xRight, yDown, yUp):
    t1, t2 = findT(p1, xLeft, xRight, yDown, yUp), findT(p2, xLeft, xRight, yDown, yUp)
    s1, s2 = findS(t1), findS(t2)
    P = findP(t1, t2)

    return t1, t2, s1, s2, P


def findInter(p1, p2, xLeft, xRight, yDown, yUp):
    eps = 1e-6
    while abs(p1[0] - p2[0]) > eps or abs(p1[1] - p2[1]) > eps:

        mid = ((p2[0] + p1[0]) / 2, (p2[1] + p1[1]) / 2)
        tmid = findT(mid, xLeft, xRight, yDown, yUp)
        smid = findS(tmid)
        if smid == 0:                                                     # точка лежит внутри прямоугольника
            p1 = mid
        else:
            p2 = mid
    return p1

def cutBase(segmentPol, clipperPol, canva=None):
    """ segment и clipper -- два полигона канвы """
    """ Возвращает промежуток в [x1, x2], который нужно закрасить """
    """ ( с учетом того, что мы закрашиваем область внутри прямоугольника"""

    try:
        segment = segmentPol.lines[0]
        clipper = clipperPol.lines[0]     # здесь это точки диагонали
    except:
        return 'error'

    xLeft, xRight = min(clipper.xStart, clipper.xEnd), max(clipper.xStart, clipper.xEnd)
    yDown, yUp = min(clipper.yStart, clipper.yEnd), max(clipper.yStart, clipper.yEnd)

    # xLeft, xRight = 167, 372
    # yDown, yUp = 143, 192
    # p1, p2 = (0, 0), (0, 5)


    # if segment.xStart < segment.xEnd:
    #     p1, p2 = (segment.xStart, segment.yStart), (segment.xEnd, segment.yEnd)
    # else:
    #     p2, p1 = (segment.xStart, segment.yStart), (segment.xEnd, segment.yEnd)

    if segment.yStart < segment.yEnd:
        p1, p2 = (segment.xStart, segment.yStart), (segment.xEnd, segment.yEnd)
    else:
        p2, p1 = (segment.xStart, segment.yStart), (segment.xEnd, segment.yEnd)

    t1, t2, s1, s2, P = findAll(p1, p2, xLeft, xRight, yDown, yUp)

    """ Проверка полной невидимости """
    if P != 0:
        return []

    isP1inClipper = (s1 == 0)
    isP2inClipper = (s2 == 0)

    """ Проверка полной видимости """
    """ s == 0 -- точка видима (лежит внутри области)"""
    if isP1inClipper and isP2inClipper:
        return [p1, p2]

    """ Поиск дальних от p1 и p2 пересечений """
    farP1Inter = findInter(p1, p2, xLeft, xRight, yDown, yUp)
    farP2Inter = findInter(p2, p1,  xLeft, xRight, yDown, yUp)

    farP1S = findS(findT(farP1Inter, xLeft, xRight, yDown, yUp))
    farP2S = findS(findT(farP2Inter, xLeft, xRight, yDown, yUp))

    """ Если отрезки сошлись на невидимой точке, значит отрезок полностью невидим """
    if farP1S != 0 and farP2S != 0 and farP1Inter == farP2Inter:
        return []

    """ Если точка P1 лежит внутри """
    if isP1inClipper:
        print('p1 inside')
        return [p1, farP1Inter]

    """ Если точка P2 лежит внутри """
    if isP2inClipper:
        print('p2 inside')
        return [p2, farP2Inter]

    if farP1Inter == p1:
        farP1Inter = findInter(farP2Inter, p2, xLeft, xRight, yDown, yUp)

    if farP2Inter == p2:
        farP2Inter = findInter(farP1Inter, p1, xLeft, xRight, yDown, yUp)

    print('p1 = ', p1)
    print('f1 = ', farP1Inter, '\n')
    print('p2 = ', p2)
    print('f2 = ', farP2Inter, '\n')

    if canva:
        p1 = Pixel(x=farP1Inter[0], y=farP1Inter[1], color='red')
        p1.showLikePoint(canva)

        p2 = Pixel(x=farP2Inter[0], y=farP2Inter[1], color='red')
        p2.showLikePoint(canva)

    return [farP1Inter, farP2Inter]


def cut(segmentPol, clipperPol, canva=None):
    inter = cutBase(segmentPol, clipperPol, canva)
    if not inter or inter == 'error':
        return inter

    roundFunc = math.floor
    inter1 = (roundFunc(inter[0][0]), roundFunc(inter[0][1]))
    inter2 = (roundFunc(inter[1][0]), roundFunc(inter[1][1]))

    return [inter1, inter2]









