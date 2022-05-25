import math

EPS = 1e-6


# Возвращает некоторую точку на отрезке (середину)
def findFi(clipper):
    return (clipper.xStart + clipper.xEnd) / 2, (clipper.yStart + clipper.yEnd) / 2


def diff(t1, t2):
    return t1[0] - t2[0], t1[1] - t2[1]


def getLen(vector):
    sum = 0
    for i in vector:
        sum += i * i

    return math.sqrt(sum)


def getNormal(clipper):
    p1 = (clipper.xStart, clipper.yStart)
    p2 = (clipper.xEnd, clipper.yEnd)
    v = diff(p2, p1)
    l = getLen(v)
    return v[1] / l, -v[0] / l


def scalarProd(v1, v2):
    if not v1 or not v2 or len(v1) != len(v2):
        print(f'Errors with lens in scalarProd, v1 = {v1}, v2 = {v2}')
        return
    sum = 0
    for i in range(len(v1)):
        sum += v1[i] * v2[i]
    return sum


def findPointUseT(p1, p2, t):

    def findX(x1, x2, t):
        return x1 + (x2 - x1) * t

    return findX(p1[0], p2[0], t), findX(p1[1], p2[1], t)


def cutBase(segmentPol, clipperPol, canva=None):
    """ segment и clipper -- два полигона канвы """
    """ Возвращает промежуток в [x1, x2], который нужно закрасить """
    """ ( с учетом того, что мы закрашиваем область внутри прямоугольника"""

    try:
        segment = segmentPol.lines[0]
        clippers = clipperPol.lines
    except:
        return 'error'

    countClipSegments = len(clippers)
    tn, tv = 0, 1

    p1 = (segment.xStart, segment.yStart)
    p2 = (segment.xEnd, segment.yEnd)

    print('p1 = ', p1)
    print('p2 = ', p2)

    d = diff(p2, p1)
    for i, clip in enumerate(clippers):
        fi = findFi(clip)

        """ Ищем для стороны вектор нормали"""
        """ Доп точка нужна, чтобы контролировать, что вектор точно направлен внутрь фигуры"""
        help_fi_in_other_side = findFi(clippers[(i + 1) % countClipSegments])
        help_v = diff(help_fi_in_other_side, fi)
        n = getNormal(clip)
        if scalarProd(n, help_v) < 0:
            n = (-n[0], -n[1])

        wi = diff(p1, fi)

        w_ck = scalarProd(n, wi)
        d_ck = scalarProd(n, d)

        if abs(d_ck) < EPS:
            if abs(w_ck) < EPS:
                print('Невидимый отрезок 1')
                return []
            continue

        t = - w_ck / d_ck

        if d_ck > 0:
            if t > 1:
                print('Невидимый отрезок 2')
                return []
            tn = max(t, tn)

        if d_ck <= 0:
            if t < 0:
                print('Невидимый отрезок 3')
                return []
            tv = min(t, tv)

    if tn <= tv:
        print('Видимый отрезок')
        return [findPointUseT(p1, p2, tn), findPointUseT(p1, p2, tv)]

    print('Невидимый отрезок 4')
    return []


def randomCut(segmentPol, clipperPol, canva=None):
    inter = cutBase(segmentPol, clipperPol, canva)
    if not inter or inter == 'error':
        return inter

    roundFunc = math.floor
    inter1 = (roundFunc(inter[0][0]), roundFunc(inter[0][1]))
    inter2 = (roundFunc(inter[1][0]), roundFunc(inter[1][1]))

    return [inter1, inter2]







