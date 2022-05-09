from model.Point import *
from view.Settings import *
from view.CanvasLine import *
from view.CanvasSegment import *
from view.CanvasPoint import *
import time
from model.fillAlg import *


class CanvasPolLine:
    def __init__(self, points, color=Settings.COLOR_LINE, width=2, showComments=True, segmentOrClipper=True,
                 InOrOut=True, diffColors=False):
        self.points = points

        self.segmentOrClipper = segmentOrClipper

        self.colorLine = color
        self.colorPoints = color

        self.width = width

        self.lines = []
        self.updateLines()

        self.showComments = showComments

        self.pixels = []
        self.startPixel = None

        self.fillFlag = False
        self.WasGo = False
        self.cutArea = []

        self.InOrOut = InOrOut
        self.diffColors = diffColors

    def changeStartPixel(self, newX, newY, color, showComments=False):
        self.startPixel = Pixel(x=newX, y=newY, color=color, showComments=showComments)

    def findFieldLines(self, field):
        for l in self.lines:
            l.findFieldLine(field)

    def updatePixels(self, field, cutPixels=[]):
        setCutPixels = set()
        for p in cutPixels:
            setCutPixels.add((p.x, p.y))

        self.pixels.clear()

        for l in self.lines:
            l.findFieldLine(field)

        self.pixels = fillWithPartitionWithDelay(self.lines, field,
                                                 setCutPixels, self.startPixel,
                                                 colorBorder=self.colorLine, delay=False)

    def show(self, field):
        if not self.WasGo:
            for p in self.points:
                p.show(field)

        self.updateLines()

        for l in self.lines:
            if self.segmentOrClipper:
                l.show(field)
            else:
                l.showLikeClipper(field)

    def updateWasGoFlag(self, newValue):
        self.WasGo = newValue

    def showWithDelay(self, field):
        for p in self.points:
            p.show(field)

        self.updateLines()
        for l in self.lines:
            l.show(field)

        if self.startPixel:
            self.startPixel.showLikePoint(field)

    def hide(self, field):
        for p in self.points:
            p.hide(field)

        for l in self.lines:
            l.hide(field)

        self.lines.clear()

    def addPoint(self, field, newPoint):
        if len(self.points) > 0:
            self.lines.append(CanvasSegment(self.points[-1], newPoint, self.colorLine))

        self.points.append(newPoint)
        self.reShow(field)

    def reShowWithDelay(self, field, cutPixels=[], startPixel=Pixel(x=0, y=0, color=Settings.COLOR_NEW_POINT)):
        self.hide(field)
        self.pixels.clear()
        self.showWithDelay(field)

        for l in self.lines:
            l.findFieldLine(field)

        setCutPixels = set()
        for p in cutPixels:
            setCutPixels.add((p.x, p.y))

        self.pixels = fillWithPartitionWithDelay(self.lines, field,
                                                 setCutPixels, self.startPixel,
                                                 colorBorder=self.colorLine, delay=True)

    def reShow(self, field, cutPixels=[]):
        self.hide(field)
        self.show(field)

        # if self.fillFlag:
        #     self.updatePixels(field, cutPixels)
        #
        # if self.segmentOrClipper:
        #     for p in self.pixels:
        #         if (p.x, p.y) not in cutPixels:
        #             p.show(field)

    def delPoint(self, field, delPoint):
        wasDel = False
        for i, point in enumerate(self.points):
            if Point.isPointsEqual(point, delPoint):
                point.hide(field)
                self.points.pop(i)
                wasDel = True

        if len(self.points) > 1 and self.points[0] != self.points[-1]:
            self.addPoint(field, CanvasPoint(self.points[0].x, self.points[0].y, self.points[0].color, showComments=self.points[0].showComments))

        self.reShow(field)
        return wasDel

    def updateLines(self):
        self.lines.clear()
        for i in range(len(self.points) - 1):
            if not self.segmentOrClipper:
                self.lines.append(CanvasSegment(self.points[i], self.points[i + 1], self.colorLine, dash=(50, 1)))
            else:
                self.lines.append(CanvasSegment(self.points[i], self.points[i + 1], self.colorLine, WasGo=self.WasGo,
                                                cutArea=self.cutArea, InOrOut=self.InOrOut, diffColors=self.diffColors))

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

    # Проверка, является ли полигон выпуклым
    def isConvexPolygon(self):
        # self.updateLines()
        for i, line in enumerate(self.lines):
            for j, segment in enumerate(self.lines):
                if j != (i - 1) % len(self.lines) and j != i and j != (i + 1) % len(self.lines) and line.isInter(segment):
                    return False
        return True
