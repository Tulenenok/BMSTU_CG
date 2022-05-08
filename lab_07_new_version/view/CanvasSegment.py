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
    def __init__(self, pointA, pointB, color='black', width=4, dash=None, arrow=None,
                 WasGo=False, cutArea=[], InOrOut=True):
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
        self.WasGo = WasGo

        # В координатах канвы
        self.xStart, self.yStart = None, None
        self.xEnd, self.yEnd = None, None

    def coordShift(self, field):
        self.xStart, self.yStart = field.coordinateShift(self.start)
        self.xEnd, self.yEnd = field.coordinateShift(self.end)

    def show(self, field):
        self.coordShift(field)

        self.pixSet = dda_line(self.xStart, self.yStart, self.xEnd, self.yEnd)
        for p in self.pixSet:
            self.pixels.append(Pixel(x=p[0], y=p[1], color=self.color))

            if not self.WasGo:
                self.pixels[-1].show(field)
                continue

            flagShow = not self.InOrOut
            for cut in self.cutArea:
                if len(cut) > 0 and cut[0][0] <= p[0] <= cut[1][0] and p[1] <= max(cut[0][1], cut[1][1]) and p[1] >= min(cut[0][1], cut[1][1]):
                    flagShow = self.InOrOut

            if flagShow:
                self.pixels[-1].show(field)


    def findFieldLine(self, field):
        self.coordShift(field)
        self.fieldLine = Line(CanvasPoint(self.xStart, self.yStart), CanvasPoint(self.xEnd, self.yEnd))
        self.pixSet = dda_line(self.xStart, self.yStart, self.xEnd, self.yEnd)

    def showLikeClipper(self, field):
        self.coordShift(field)

        self.rec = field.create_rectangle(self.xStart, self.yStart, self.xEnd, self.yEnd, outline=self.color, width=2)


    def hide(self, field):
        # field.delete(self.l)
        # self.l = None
        for p in self.pixels:
            p.hide(field)
        self.pixels = []

        if self.rec:
            field.delete(self.rec)
        self.rec = None

    def reShow(self, field):
        self.hide(field)
        self.show(field)