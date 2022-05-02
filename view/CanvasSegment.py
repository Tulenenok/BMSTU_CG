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

    return points


class CanvasSegment(Line):
    def __init__(self, pointA, pointB, color='black', width=4, dash=None, arrow=None):
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

    def show(self, field):
        try:                                                    # Такого метода у канвы может не оказаться
            xStart, yStart = field.coordinateShift(self.start)  # Точки перевели в понятие канвы
            xEnd, yEnd = field.coordinateShift(self.end)
        except:
            xStart, yStart = self.start.x, self.start.y
            xEnd, yEnd = self.end.x, self.end.y
            print("Вы не переводите координаты точек в координаты канвы, могут быть ошибки")

        xS, yS, xE, yE = xStart, yStart, xEnd, yEnd
        self.pixSet = dda_line(xS, yS, xE, yE)
        for p in self.pixSet:
            self.pixels.append(Pixel(x = p[0], y = p[1], color = self.color))
            self.pixels[-1].show(field)

        # if self.dash and self.arrow:
        #     self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, dash=self.dash, arrow=self.arrow)
        # elif self.dash:
        #     self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, dash=self.dash)
        # elif self.arrow:
        #     self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, arrow=self.arrow)
        # else:
        #     self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width)

    def findFieldLine(self, field):
        xStart, yStart = field.coordinateShift(self.start)
        xEnd, yEnd = field.coordinateShift(self.end)

        self.fieldLine = Line(CanvasPoint(xStart, yStart), CanvasPoint(xEnd, yEnd))
        self.pixSet = dda_line(xStart, yStart, xEnd, yEnd)


    def hide(self, field):
        # field.delete(self.l)
        # self.l = None
        for p in self.pixels:
            p.hide(field)
        self.pixels = []

    def reShow(self, field):
        self.hide(field)
        self.show(field)