from model.Point import *
from view.Settings import *
from view.CanvasLine import *
from view.CanvasSegment import *
from view.CanvasPoint import *
import time
from model.fillAlg import *


class CanvasPolLine:
    def __init__(self, points, color=Settings.COLOR_LINE, width=2, showComments=True, fillOrCut=True):
        self.points = points

        self.fillOrCut = fillOrCut

        self.colorLine = color
        self.colorPoints = color

        self.width = width

        self.lines = []
        self.updateLines()

        self.showComments = showComments

        self.pixels = []

        self.fillFlag = False

    def updatePixels(self, field, cutPixels=[]):
        setCutPixels = set()
        for p in cutPixels:
            setCutPixels.add((p.x, p.y))

        self.pixels.clear()

        # self.updateLines()
        for l in self.lines:
            l.findFieldLine(field)

        fillPixels = fillWithPartition(self.lines)
        for p in fillPixels.keys():
            if fillPixels[p] and p not in setCutPixels:
                self.pixels.append(Pixel(x=p[0], y=p[1], color=self.colorPoints))


    def show(self, field):
        for p in self.points:
            p.show(field)

        for l in self.lines:
            l.show(field)

        if self.fillOrCut:
            for p in self.pixels:
                p.show(field)

    def showWithDelay(self, field):
        for p in self.points:
            p.show(field)

        for l in self.lines:
            l.show(field)


    def hide(self, field):
        for p in self.points:
            p.hide(field)

        for l in self.lines:
            l.hide(field)

        for p in self.pixels:
            p.hide(field)

        self.lines.clear()
        self.pixels.clear()

    def addPoint(self, field, newPoint):
        if len(self.points) > 0:
            self.lines.append(CanvasSegment(self.points[-1], newPoint, self.colorLine))

        self.points.append(newPoint)
        self.reShow(field)

    def reShowWithDelay(self, field, cutPixels=[]):
        self.hide(field)
        self.updateLines()
        self.pixels.clear()
        self.showWithDelay(field)

        for l in self.lines:
            l.findFieldLine(field)

        setCutPixels = set()
        for p in cutPixels:
            setCutPixels.add((p.x, p.y))

        self.pixels = fillWithPartitionWithDelay(self.lines, field, setCutPixels)

        # if self.fillFlag:
        #     self.updatePixels(field, cutPixels)

    def reShow(self, field, cutPixels=[]):
        self.hide(field)
        self.updateLines()
        if self.fillFlag:
            self.updatePixels(field, cutPixels)
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

    def updateLines(self):
        self.lines.clear()
        for i in range(len(self.points) - 1):
            if not self.fillOrCut:
                self.lines.append(CanvasSegment(self.points[i], self.points[i + 1], self.colorLine, dash=(50, 1)))
            else:
                self.lines.append(CanvasSegment(self.points[i], self.points[i + 1], self.colorLine))


    def isPointOn(self, field, X, Y):
        for p in self.points:
            if p.isClick(field, X, Y):
                return True
        return False

    def PointOnWithPoint(self, field, X, Y):
        for p in self.points:
            if p.isClick(field, X, Y):
                return p
        return None

    def updateShowFlag(self, newFlag):
        self.showComments = newFlag
        for p in self.points:
            p.ShowComments = self.showComments

        for pix in self.pixels:
            pix.ShowComments = self.showComments

    def changeColor(self, newColorPoint, newColorLine):
        self.colorLine = newColorLine
        self.colorPoints = newColorPoint

        for point in self.points:
            point.color = self.colorPoints

        for pix in self.pixels:
            pix.color = self.colorPoints

    def rotatePol(self, pointCenter, alpha):
        for point in self.points:
            point.rotate(pointCenter, alpha)
        self.updateLines()

    def shiftPol(self, xShift, yShift):
        for point in self.points:
            point.shift(xShift, yShift)
        self.updateLines()

    def scalePol(self, x, y, kx, ky):
        for point in self.points:
            point.scale(x, y, kx, ky)
        self.updateLines()
