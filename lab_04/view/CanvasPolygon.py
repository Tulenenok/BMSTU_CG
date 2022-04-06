from model.Point import *
from view.Settings import *
from view.CanvasLine import *
from view.CanvasSegment import *

from model.circles import *
from model.ellipses import *


class CanvasPolygon:
    def __init__(self, points, bdColor=Settings.COLOR_LINE,
               bgColor=Settings.COLOR_LINE, actbdColor=Settings.COLOR_LINE, actbgColor=Settings.COLOR_LINE,
               width=2, showComments=True):
        self.points = points

        self.bdColor = bdColor
        self.bgColor = bgColor
        self.actbdColor = actbdColor
        self.actbgColor = actbgColor
        self.width = width

        self.p = None

        self.ShowComments = showComments

    def show(self, field):
        if self.points == []:
            return

        try:
            CanvasPoints = [field.coordinateShift(point) for point in self.points if point.p]
        except:
            CanvasPoints = [(point.x, point.y) for point in self.points if point.p]
            print("Вы не переводите координаты полигона в координаты канвы, могут быть ошибки")

        if CanvasPoints:
            self.p = field.create_polygon(CanvasPoints, outline=self.bdColor, fill=self.bgColor, width=self.width,
                                          activefill=self.actbgColor, activeoutline=self.actbdColor)

    def hide(self, field):
        if self.p:
            field.delete(self.p)
        self.p = None

    def reShow(self, field):
        self.hide(field)
        self.show(field)

    def addPoint(self, field, newPoint):
        self.points.append(newPoint)
        self.reShow(field)

    def delPoint(self, field, delPoint):
        for i, point in enumerate(self.points):
            if Point.isPointsEqual(point, delPoint):
                self.points.pop(i)

        self.reShow(field)


class CanvasPolCircle:
    def __init__(self, center, r, color=Settings.COLOR_LINE, width=2, showComments=True, method=Tools.M_CANONICAL):
        self.center = center
        self.radius = r

        self.colorLine = color
        self.colorPoints = color
        self.width = width

        self.points = []
        self.l = None

        self.showComments = showComments

        self.method = FUNC_METHODS[method] if method != Tools.M_USUAL else method

    def updateUseGraphPrim(self, field):
        x_c, y_c, r = self.shiftCoordToCanvas(field)
        self.l = field.create_oval(x_c - r, y_c + r, x_c + r, y_c - r, outline=self.colorLine, width=self.width)

    def countPoints(self):
        return len(self.points)

    def show(self, field):
        self.center.show(field)

        if self.method == Tools.M_USUAL:
            self.updateUseGraphPrim(field)
        else:
            self.updatePoints(field)
            for p in self.points:
                p.show(field)

    def hide(self, field):
        self.center.hide(field)
        for p in self.points:
            p.hide(field)

        if self.l:
            field.delete(self.l)
            self.l = None

        self.points.clear()

    def reShow(self, field):
        self.hide(field)
        self.show(field)

    def delPoint(self, field, delPoint):
        wasDel = False
        for i, point in enumerate(self.points):
            if Point.isPointsEqual(point, delPoint):
                point.hide(field)
                self.points.pop(i)
                wasDel = True

        self.reShow(field)
        return wasDel

    def shiftCoordToCanvas(self, field):
        x_c, y_c, = field.XShiftPC(self.center.x), field.YShiftPC(self.center.y)
        r = field.XShiftPC(self.center.x + self.radius)
        r -= x_c

        return x_c, y_c, r

    def updatePoints(self, field):
        self.points.clear()

        x_c, y_c, r = self.shiftCoordToCanvas(field)

        pointsX, pointsY = self.method(x_c, y_c, r)
        for i in range(len(pointsX)):
            newPixel = Pixel(x=pointsX[i], y=pointsY[i], showComments=False, color=self.colorLine)
            self.points.append(newPixel)

    def isPointOn(self, field, X, Y):
        if self.center.isClick(field, X, Y):
            return True

        for p in self.points:
            if p.isClick(field, X, Y):
                return True
        return False

    def PointOnWithPoint(self, field, X, Y):
        if self.center.isClick(field, X, Y):
            return self.center

        for p in self.points:
            if p.isClick(field, X, Y):
                return p
        return None

    def updateShowFlag(self, newFlag):
        self.showComments = newFlag
        self.center.ShowComments = self.showComments

    def changeColor(self, newColorPoint, newColorLine):
        self.colorLine = newColorLine
        self.colorPoints = newColorPoint

        for point in self.points:
            point.color = self.colorPoints
        self.center.color = self.colorPoints

    def rotatePol(self, pointCenter, alpha):
        self.center.rotate(pointCenter, alpha)
        for point in self.points:
            point.rotate(pointCenter, alpha)

    def shiftPol(self, xShift, yShift):
        self.center.action(xShift, yShift)
        for point in self.points:
            point.action(xShift, yShift)

    def scalePol(self, x, y, kx, ky):
        self.center.scale(x, y, kx, ky)
        for point in self.points:
            point.scale(x, y, kx, ky)

    def isEqualPol(self, pointStart, r):
        return Point.isPointsEqual(pointStart, self.center) and self.radius == r


class CanvasPolEllipse:
    def __init__(self, center, a, b, color=Settings.COLOR_LINE, width=2, showComments=True, method=Tools.M_CANONICAL):
        self.center = center
        self.a = a
        self.b = b

        self.colorLine = color
        self.colorPoints = color
        self.width = width

        self.points = []
        self.l = None

        self.showComments = showComments

        self.method = FUNC_ELLIPS[method] if method != Tools.M_USUAL else method

    def updateUseGraphPrim(self, field):
        x_c, y_c, a, b = self.shiftCoordToCanvas(field)
        self.l = field.create_oval(x_c - a, y_c + b, x_c + a, y_c - b, outline=self.colorLine, width=self.width)

    def countPoints(self):
        return len(self.points)

    def show(self, field):
        self.center.show(field)

        if self.method == Tools.M_USUAL:
            self.updateUseGraphPrim(field)
        else:
            self.updatePoints(field)
            for p in self.points:
                p.show(field)

    def hide(self, field):
        self.center.hide(field)
        for p in self.points:
            p.hide(field)

        if self.l:
            field.delete(self.l)
            self.l = None

        self.points.clear()

    def reShow(self, field):
        self.hide(field)
        self.show(field)

    def delPoint(self, field, delPoint):
        wasDel = False
        for i, point in enumerate(self.points):
            if Point.isPointsEqual(point, delPoint):
                point.hide(field)
                self.points.pop(i)
                wasDel = True

        self.reShow(field)
        return wasDel

    def shiftCoordToCanvas(self, field):
        x_c, y_c = field.XShiftPC(self.center.x), field.YShiftPC(self.center.y)

        a = field.XShiftPC(self.center.x + self.a)
        a -= x_c

        b = field.YShiftPC(self.center.y + self.b)
        b -= y_c
        b = abs(b)

        print(self.center.y, y_c)
        print(self.b, b)

        return x_c, y_c, a, b

    def updatePoints(self, field):
        self.points.clear()

        x_c, y_c, a, b = self.shiftCoordToCanvas(field)

        pointsX, pointsY = self.method(x_c, y_c, a, b)
        print(pointsX)
        print(pointsY)
        for i in range(len(pointsX)):
            newPixel = Pixel(x=pointsX[i], y=pointsY[i], showComments=False, color=self.colorLine)
            self.points.append(newPixel)

    def isPointOn(self, field, X, Y):
        if self.center.isClick(field, X, Y):
            return True

        for p in self.points:
            if p.isClick(field, X, Y):
                return True
        return False

    def PointOnWithPoint(self, field, X, Y):
        if self.center.isClick(field, X, Y):
            return self.center

        for p in self.points:
            if p.isClick(field, X, Y):
                return p
        return None

    def updateShowFlag(self, newFlag):
        self.showComments = newFlag
        self.center.ShowComments = self.showComments

    def changeColor(self, newColorPoint, newColorLine):
        self.colorLine = newColorLine
        self.colorPoints = newColorPoint

        for point in self.points:
            point.color = self.colorPoints
        self.center.color = self.colorPoints

    def rotatePol(self, pointCenter, alpha):
        self.center.rotate(pointCenter, alpha)
        for point in self.points:
            point.rotate(pointCenter, alpha)

    def shiftPol(self, xShift, yShift):
        self.center.action(xShift, yShift)
        for point in self.points:
            point.action(xShift, yShift)

    def scalePol(self, x, y, kx, ky):
        self.center.scale(x, y, kx, ky)
        for point in self.points:
            point.scale(x, y, kx, ky)

    def isEqualPol(self, pointStart, a, b):
        return Point.isPointsEqual(pointStart, self.center) and self.a == a and self.b == b

