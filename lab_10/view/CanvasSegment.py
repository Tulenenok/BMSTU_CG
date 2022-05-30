from model.Line import Line
from view.CanvasPoint import *
import math


def dda_line(xStart, yStart, xEnd, yEnd):
    x, y = xStart, yStart

    x_arr = [math.floor(x)]
    y_arr = [math.floor(y)]
    points = set()
    points.add((math.floor(x), math.floor(y)))

    l = max(abs(xEnd - xStart), abs(yEnd - yStart)) + 1

    for i in range(int(l)):
        x += (xEnd - xStart) / l
        y += (yEnd - yStart) / l

        x_arr.append(math.floor(x))
        y_arr.append(math.floor(y))

        points.add((math.floor(x), math.floor(y)))
        points.add((math.floor(x) - 1, math.floor(y)))
        # points.add((math.floor(x) + 1, math.floor(y)))

    return points


class CanvasSegment(Line):
    def __init__(self, pointA, pointB, color='black', width=2, dash=(100, 2), arrow=None,
                 WasGo=False, cutArea=[], InOrOut=True, diffColors=False):
        super().__init__(pointA, pointB)
        self.color = color
        self.width = width
        self.dash = dash
        self.arrow = arrow

        self.l = None

        self.ShowComments = True

        self.fieldLine = None

        self.pixSet = set()
        self.pixels = []

        self.rec = None
        self.cutArea = cutArea

        self.InOrOut = InOrOut           # Флаг, оставляем мы пиксели внутри или снаружи области
        self.diffColors = diffColors     # Флаг, нужно ли закрашивать отрезок разными цветами вместо обрезки
        self.WasGo = WasGo

        self.needDash = False

        # В координатах канвы
        self.xStart, self.yStart = None, None
        self.xEnd, self.yEnd = None, None

    def coordShift(self, field):
        self.xStart, self.yStart = field.coordinateShift(self.start)
        self.xEnd, self.yEnd = field.coordinateShift(self.end)

    def show(self, field):
        self.coordShift(field)

        xS, yS, xE, yE, = self.xStart, self.yStart, self.xEnd, self.yEnd

        if self.dash and self.needDash:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, dash=self.dash)
        else:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width)

    def findFieldLine(self, field):
        self.coordShift(field)
        self.fieldLine = Line(CanvasPoint(self.xStart, self.yStart), CanvasPoint(self.xEnd, self.yEnd))

    def showLikeClipper(self, field):
        self.coordShift(field)
        self.rec = field.create_line(self.xStart, self.yStart, self.xEnd, self.yEnd, fill=self.color, width=2)

    def hide(self, field):
        field.delete(self.l)
        self.l = None

    def reShow(self, field):
        self.hide(field)
        self.show(field)

    def isInter(self, segment):
        firstSign = self.A * segment.start.x + self.B * segment.start.y + self.C
        secondSign = self.A * segment.end.x + self.B * segment.end.y + self.C

        if firstSign * secondSign <= 0:
            return True

        return False