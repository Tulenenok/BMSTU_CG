from model.Line import Line
from model.Tools import Tools
from model.algConstructSeg import *
from view.CanvasPoint import *


class CanvasSegment(Line):
    def __init__(self, pointA, pointB, color='black', width=2, dash=None, arrow=None, method=Tools.M_CANONICAL):
        super().__init__(pointA, pointB)
        self.color = color
        self.width = width
        self.dash = dash
        self.arrow = arrow

        self.l = None

        self.ShowComments = True
        self.method = method
        self.pixels = []
        self.i = 2            # число доступных уровней интенсивности

    def show(self, field):
        if self.l:
            field.delete(self.l)
            self.l = None

        self.pixels.clear()

        if self.method == Tools.M_USUAL:
            self.updateUseGraphPrim(field)
            return

        if self.method == Tools.M_CANONICAL:
            self.updateUseCDA(field)
        elif self.method == Tools.M_PARAMETRIC:
            self.updateUseBrezReal(field)
        elif self.method == Tools.M_BREZENHAM:
            self.updateUseBrezInt(field)
        elif self.method == Tools.M_MIDDLE_POINT:
            self.updateUseBrezWithout(field)
        elif self.method == Tools.M_VY:
            self.updateUseWU(field)

        for p in self.pixels:
            p.show(field)

    def hide(self, field):
        if self.l:
            field.delete(self.l)
            self.l = None

        for p in self.pixels:
            p.hide(field)

    def reShow(self, field):
        self.hide(field)
        self.show(field)

    def StartEndShiftPC(self, field):
        try:
            xStart, yStart = field.coordinateShift(self.start)  # Точки перевели в понятие канвы
            xEnd, yEnd = field.coordinateShift(self.end)
        except:
            xStart, yStart = self.start.x, self.start.y
            xEnd, yEnd = self.end.x, self.end.y
            print("Вы не переводите координаты точек в координаты канвы, могут быть ошибки")
        return xStart, yStart, xEnd, yEnd

    def updateUseCDA(self, field):
        xStart, yStart, xEnd, yEnd = self.StartEndShiftPC(field)

        points = CDA(xStart, yStart, xEnd, yEnd)

        for point in points:
            newPixel = Pixel(x=point[0], y=point[1], showComments=False, color=self.color)
            self.pixels.append(newPixel)

    def updateUseBrezReal(self, field):
        xStart, yStart, xEnd, yEnd = self.StartEndShiftPC(field)

        pointsX, pointsY = BresenhamWrap(xStart, yStart, xEnd, yEnd, BresenhamReal)
        for i in range(len(pointsX)):
            newPixel = Pixel(x=pointsX[i], y=pointsY[i], showComments=False, color=self.color)
            self.pixels.append(newPixel)

    def updateUseBrezInt(self, field):
        xStart, yStart, xEnd, yEnd = self.StartEndShiftPC(field)

        pointsX, pointsY = BresenhamWrap(xStart, yStart, xEnd, yEnd, BresenhamInt)
        for i in range(len(pointsX)):
            newPixel = Pixel(x=pointsX[i], y=pointsY[i], showComments=False, color=self.color)
            self.pixels.append(newPixel)

    def updateUseBrezWithout(self, field):
        xStart, yStart, xEnd, yEnd = self.StartEndShiftPC(field)

        pointsX, pointsY, intens = BresenhamWithout_Wrap(xStart, yStart, xEnd, yEnd, self.i)
        for i in range(len(pointsX)):
            newPixel = Pixel(x=pointsX[i], y=pointsY[i], showComments=False, color=Tools.changeIntens(self.color, intens[i] / self.i))
            self.pixels.append(newPixel)

    def updateUseWU(self, field):
        xStart, yStart, xEnd, yEnd = self.StartEndShiftPC(field)

        pointsX, pointsY, intens = wu([xStart, yStart], [xEnd, yEnd])
        for i in range(len(pointsX)):
            newPixel = Pixel(x=pointsX[i], y=pointsY[i], showComments=False, color=Tools.changeIntens(self.color, intens[i]))
            self.pixels.append(newPixel)

    def updateUseGraphPrim(self, field):
        xS, yS, xE, yE = self.StartEndShiftPC(field)
        if self.dash and self.arrow:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, dash=self.dash,
                                       arrow=self.arrow)
        elif self.dash:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, dash=self.dash)
        elif self.arrow:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width, arrow=self.arrow)
        else:
            self.l = field.create_line(xS, yS, xE, yE, fill=self.color, width=self.width)