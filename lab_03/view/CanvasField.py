import math
import pickle

from PIL import ImageTk, Image

from view.CanvasPoint import CanvasPoint
from view.CanvasLine import CanvasLine
from view.CanvasCircle import CanvasCircle
from view.Settings import Settings
from view.CanvasPolygon import *
from view.keyInput import *

from model.Tools import Tools

from tkinter import *
from tkinter.colorchooser import askcolor

import copy


# пример создания  ResizingCanvas(myFrame, width=850, height=400, bg="red", highlightthickness=0)
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.resize)

        self.bind('<1>', lambda event: self.click(event), '+')
        self.bind("<Motion>", lambda event: self.showCoords(event), '+')
        self.bind("<Leave>", lambda event: self.hideCoords(event), '+')

        self.bind("<MouseWheel>", self.mouseZoom, '+')

        self.bind("<Shift-Down>", lambda event: self.shift(0, 10), '+')
        self.bind("<Shift-Left>", lambda event: self.shift(-10, 0), '+')
        self.bind("<Shift-Up>", lambda event: self.shift(0, -10), '+')
        self.bind("<Shift-Right>", lambda event: self.shift(10, 0), '+')

        # self.bind("<Right>", lambda event: self.arrowMoveAcrossField('X', 'right'), '+')
        # self.bind("<Left>", lambda event: self.arrowMoveAcrossField('X', 'left'), '+')
        # self.bind("<Up>", lambda event: self.arrowMoveAcrossField('Y', 'up'), '+')
        # self.bind("<Down>", lambda event: self.arrowMoveAcrossField('Y', 'down'), '+')

        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.image = None

    def mouseRotate(self, mode):
        pass

    def shift(self, xShift, yShift):
        pass

    def resize(self, event):
        self.width = event.width
        self.height = event.height

        self.config(width=self.width, height=self.height)

    def click(self, event):
        pass

    def showCoords(self, event):
        pass

    def hideCoords(self, event):
        pass

    def mouseZoom(self, event):
        pass

    def plug(self, event):
        pass

    def arrowMoveAcrossField(self, axis, side):
        pass

    def changeBGColor(self):
        color = askcolor()[1]
        if not color:
            return

        self.configure(bg=color)


class CoordGrid(ResizingCanvas):
    def __init__(self, window, XStart=-100, XEnd=100, YStart=-100, YEnd=100, gridCoef=10, showArrows=True, **kwargs):
        super(CoordGrid, self).__init__(window, **kwargs)
        self.XStart, self.XEnd, self.YStart, self.YEnd = XStart, XEnd, YStart, YEnd

        self.XLine, self.YLine = None, None
        self.gridLines = []
        self.gridDashes = []
        self.gridText = []

        self.gridCoefX = gridCoef
        self.gridCoefY = gridCoef

        self.showArrows = showArrows

    def changeLimits(self, XStart, XEnd, YStart, YEnd, flagChangeCoef=True):
        if flagChangeCoef:
            if self.controllCoef(XStart, XEnd, YStart, YEnd):
                return Tools.EXIT_FAILURE

        self.XStart, self.XEnd, self.YStart, self.YEnd = XStart, XEnd, YStart, YEnd
        self.update()

    def coordinateShift(self, canvasPoint):
        return self.XShiftPC(canvasPoint.x), self.YShiftPC(canvasPoint.y)

    # Перевод координаты X из представления человека в представление канвы
    def XShiftPC(self, x):
        return 0 + (x - self.XStart) * self.width / abs(self.XEnd - self.XStart)

    # Перевод координаты Y из представления человека в представление канвы
    def YShiftPC(self, y):
        return self.height - (y - self.YStart) * self.height / abs(self.YEnd - self.YStart)

    # Перевод координаты X из представления канвы в представление человека
    def XShiftCP(self, x):
        return self.XStart + x * abs(self.XEnd - self.XStart) / self.width

    # Перевод координаты Y из представления канвы в представление человека
    def YShiftCP(self, y):
        return self.YEnd - y * abs(self.YEnd - self.YStart) / self.height

    # Перевод длины отрезка из представления человека в представление канвы
    def XLineShiftPC(self, lenLine):
        return lenLine * self.width / abs(self.XEnd - self.YStart)

    def arrowsShow(self):
        if self.showArrows:
            self.XLine = self.create_line(0, self.height / 2, self.width, self.height / 2, fill='black', width=2, arrow=LAST)
            self.YLine = self.create_line(self.width / 2, self.height, self.width / 2, 0, fill='black', width=2, arrow=LAST)
        else:
            self.XLine = self.create_line(0, self.height / 2, self.width, self.height / 2, fill='grey', width=2, dash=(2, 2))
            self.YLine = self.create_line(self.width / 2, self.height, self.width / 2, 0, fill='grey', width=2, dash=(2, 2))

    def arrowsHide(self):
        if self.XLine:
            self.delete(self.XLine)
        if self.YLine:
            self.delete(self.YLine)
        self.XLine, self.YLine = None, None

    def arrowsUpdate(self):
        self.arrowsHide()
        self.arrowsShow()

    def gridShow(self):
        # вертикальная сетка (рисуем линии параллельные оси Y

        step = self.width / 2 / self.gridCoefX
        i = 0
        while i < self.width - step:
            i += step
            if math.fabs(i - self.width / 2) < 1:
                continue

            self.gridLines.append(self.create_line(i, self.height, i, 0, fill='grey', width=2, dash=(2, 2)))
            if self.showArrows:
                self.gridDashes.append(self.create_line(i, self.height / 2 - 4, i, self.height / 2 + 4, fill='black', width=2))
                self.gridText.append(self.create_text(i, self.height / 2 - 12, text="%.1f" % (self.XShiftCP(i)), font=('Arial', 8, 'bold'), justify=CENTER, fill='black'))

        # горизонтальная сетка (рисуем линии параллельные оси X)

        step = self.height / 2 / self.gridCoefY
        i = 0
        while i < self.height - step:
            i += step
            if math.fabs(i - self.height / 2) < 1:
                continue
            self.gridLines.append(self.create_line(0, i, self.width, i, fill='grey', width=2, dash=(2, 2)))
            if self.showArrows:
                self.gridDashes.append(self.create_line(self.width / 2 - 4, i, self.width / 2 + 4, i, fill='black', width=2))
                self.gridText.append(self.create_text(self.width / 2 + 12, i, text="%.1f" % (self.YShiftCP(i)),
                                                        font=('Arial', 8, 'bold'), justify=CENTER, fill='black'))

        # Подпись осей координат
        if self.showArrows:
            self.gridText.append(self.create_text(self.width / 2 + 12, 12, text='Y',
                                                        font=('Arial', 10, 'bold'), justify=CENTER, fill='black'))
            self.gridText.append(self.create_text(self.width - 12, self.height / 2 + 12, text='X',
                                                        font=('Arial', 10, 'bold'), justify=CENTER, fill='black'))

    def gridHide(self):
        for line in self.gridLines:
            self.delete(line)

        for dash in self.gridDashes:
            self.delete(dash)

        for text in self.gridText:
            self.delete(text)

        self.gridLines.clear()
        self.gridDashes.clear()

    def gridUpdate(self):
        self.gridHide()
        self.gridShow()

    def update(self):
        self.arrowsUpdate()
        self.gridUpdate()

    def resize(self, event):
        super().resize(event)
        self.correct_field()
        self.update()

    def correct_field(self):
        width = self.winfo_width()
        height = self.winfo_height()

        fwidth = self.XEnd - self.XStart
        fheight = self.YEnd - self.YStart

        fxmid = (self.XEnd + self.XStart) / 2
        new_fwidth = fheight * width / height
        self.XStart = fxmid - new_fwidth / 2
        self.XEnd = fxmid + new_fwidth / 2

        self.changeLimits(self.XStart, self.XEnd, self.YStart, self.YEnd)

    def zoomPlus(self, XStart, XEnd, YStart, YEnd):
        stepX = abs(XStart - XEnd) / 2 / self.gridCoefX
        while stepX < 1 and self.gridCoefX > 1:
            self.gridCoefX -= 1
            stepX = abs(XStart - XEnd) / 2 / self.gridCoefX

        stepY = abs(YStart - YEnd) / 2 / self.gridCoefY
        while stepY < 1 and self.gridCoefY > 1:
            self.gridCoefY -= 1
            stepY = abs(YStart - YEnd) / 2 / self.gridCoefY

    def zoomMinus(self, XStart, XEnd, YStart, YEnd):
        stepX = abs(XStart - XEnd) / 2 / self.gridCoefX
        while stepX >= 2 and self.gridCoefX < 10:
            self.gridCoefX += 1
            stepX = abs(XStart - XEnd) / 2 / self.gridCoefX

        stepY = abs(YStart - YEnd) / 2 / self.gridCoefY
        while stepY >= 2 and self.gridCoefY < 10:
            self.gridCoefY += 1
            stepY = abs(YStart - YEnd) / 2 / self.gridCoefY

    def arrowMoveAcrossField(self, axis, side):
        if axis == 'X':
            step = abs(self.XStart - self.XEnd) / self.gridCoefX / 2
            self.changeLimits(self.XStart + (step if side == 'right' else -step),
                              self.XEnd + (step if side == 'right' else -step),
                              self.YStart, self.YEnd)
        else:
            step = abs(self.YStart - self.YEnd) / self.gridCoefX / 2
            self.changeLimits(self.XStart, self.XEnd, self.YStart + (step if side == 'up' else -step),
                                     self.YEnd + (step if side == 'up' else -step))

    def controllCoef(self, XStart, XEnd, YStart, YEnd):
        if abs(XEnd - XStart) <= Settings.MIN_LEN_COORDS:
            print('Слишком маленький масштаб сетки для X')
            return Tools.EXIT_FAILURE

        if abs(YEnd - YStart) <= Settings.MIN_LEN_COORDS:
            print('Слишком маленький масштаб сетки для Y')
            return Tools.EXIT_FAILURE

        self.zoomPlus(XStart, XEnd, YStart, YEnd)
        self.zoomMinus(XStart, XEnd, YStart, YEnd)

        return Tools.EXIT_SUCCESS

    def mouseZoom(self, event):
        stepX = abs(self.XStart - self.XEnd) / self.gridCoefX / 2
        stepY = abs(self.YStart - self.YEnd) / self.gridCoefX / 2
        if event.delta > 0:
            self.changeLimits(self.XStart + stepX, self.XEnd - stepX, self.YStart + stepY, self.YEnd - stepY, True)
        elif event.delta < 0:
            self.changeLimits(self.XStart - stepX, self.XEnd + stepX, self.YStart - stepY, self.YEnd + stepY, True)

    def changeCoef(self, sign, *axis):
        if sign == '+':
            self.gridCoefX = self.gridCoefX - 1 if 'X' in axis and self.gridCoefX > 1 else self.gridCoefX
            self.gridCoefY = self.gridCoefY - 1 if 'Y' in axis and self.gridCoefY > 1 else self.gridCoefY
        else:
            self.gridCoefX = self.gridCoefX + 1 if 'X' in axis and self.gridCoefX < 10 else self.gridCoefX
            self.gridCoefY = self.gridCoefY + 1 if 'Y' in axis and self.gridCoefY < 10 else self.gridCoefY

        self.update()

    def flagShowGrid(self, flag):
        self.showArrows = flag
        self.update()


class CartesianField(CoordGrid):
    def __init__(self, rootFrame, root, colorPoints=Settings.COLOR_LINE,
                 XStart=-100, XEnd=100, YStart=-100, YEnd=100, gridCoef=10, showArrows=False, **kwargs):
        super(CartesianField, self).__init__(rootFrame, XStart, XEnd, YStart, YEnd, gridCoef, showArrows, **kwargs)
        self.root = root

        self.points = []
        self.lines = []
        self.circles = []

        self.t = None

        self.colorPoints = colorPoints

        self.ShowComments = False

    def showCoords(self, event):
        if self.t:
            self.delete(self.t)

        if self.ShowComments:
            self.t = self.create_text(event.x + 10, event.y - 10,
                                      text=str(int(self.XShiftCP(event.x))) + ", " + str(int(self.YShiftCP(event.y))),
                                      font=('Arial', 8, 'bold'), justify=CENTER, fill='black')

    def hideCoords(self, event):
        if self.t:
            self.delete(self.t)

    def click(self, event):
        newPoint = CanvasPoint(int(self.XShiftCP(event.x)), int(self.YShiftCP(event.y)),
                               self.colorPoints, showComments=self.ShowComments)
        newPoint.show(self)
        self.points.append(newPoint)

    def clear(self):
        for point in self.points:
            point.hide(self)
        self.points.clear()
        self.clearResult()

    def clearResult(self):
        for line in self.lines:
            line.hide(self)
        for circle in self.circles:
            circle.hide(self)

        self.lines.clear()
        self.circles.clear()

    def changeColorPoints(self, points, newColor=Settings.COLOR_POINT_FIRST_SET):
        for p in points.getAll():
            p.changeColor(self, newColor)

    def showPoint(self, x, y, color=Settings.COLOR_NEW_POINT):
        point = CanvasPoint(float(x), float(y), showComments=self.ShowComments)
        self.points.append(point)
        point.show(self)

    def showLine(self, start, end, color=Settings.COLOR_LINE):
        line = CanvasLine(start, end, color)
        self.lines.append(line)
        line.show(self)

    def showCircle(self, center, r, color, width=2, activefill=None):
        circle = CanvasCircle(center, r, color, width, activefill, showComments=self.ShowComments)
        self.circles.append(circle)
        circle.show(self)

    def update(self):
        super().update()
        self.updateShowFlags()

        for point in self.points:
            point.reShow(self)

        for line in self.lines:
            line.reShow(self)

        for circle in self.circles:
            circle.reShow(self)

    def save(self):
        try:
            self.root.saveVersion()
        except:
            print('Вы не используете сохранение')

    def saveCanva(self, f):
        pickle.dump(self.points, f)
        pickle.dump(self.lines, f)
        pickle.dump(self.circles, f)

    def loadCanva(self, f):
        try:
            points = pickle.load(f)
            lines = pickle.load(f)
            circles = pickle.load(f)
        except:
            print('Ошибка загрузки данных')
            return Tools.EXIT_FAILURE

        self.clear()
        self.points = points
        self.lines = lines
        self.circles = circles

        self.update()
        return Tools.EXIT_SUCCESS

    def rightClick(self, XEvent, YEvent):
        if not XEvent or not YEvent:
            print('No')
            return

        for i, point in enumerate(self.points):
            if point.isClick(self, XEvent, YEvent):
                point.hide(self)
                self.points.pop(i)

    def updateShowFlags(self):
        for point in self.points:
            point.ShowComments = self.ShowComments
        for circle in self.circles:
            circle.ShowComments = self.ShowComments


class PolygonField(CartesianField):
    def __init__(self, rootFrame, root, **kwargs):
        super(PolygonField, self).__init__(rootFrame, root, **kwargs)

        self.colorNowPol = Settings.COLOR_POINT_SECOND_SET
        self.polygons = []

        self.fillPoint = None

        self.rotatePoint = CanvasPoint(0, 0)

        self.method = Tools.M_CDA

    def click(self, event):
        if len(self.polygons) == 0:
            self.startNewPolygon('plug')
        newPoint = CanvasPoint(float(self.XShiftCP(event.x)), float(self.YShiftCP(event.y)),
                               self.colorNowPol, showComments=self.ShowComments)
        if self.polygons[-1].countPoints() >= 2:
            self.startNewPolygon('plug')

        self.polygons[-1].addPoint(self, newPoint)

        self.save()

    def showCoords(self, event):
        super(PolygonField, self).showCoords(event)
        if event.x and event.y:
            if self.fillPoint:
                self.fillPoint.hideHightlight(self)

            self.fillPoint = self.pointInPolWithPoint(float(event.x), float(event.y))

            if self.fillPoint:
                self.fillPoint.highlight(self)
            # self.update()

    def clear(self):
        for pol in self.polygons:
            pol.hide(self)
        # self.polygons = [CanvasPolLine([], self.colorNowPol)]

    def clearAll(self):
        self.clear()
        self.polygons = []

    def update(self):
        super(PolygonField, self).update()
        for pol in self.polygons:
            pol.reShow(self)

        ''' РАСКОММЕНТИРОВАТЬ ЭТУ СТРОКУ ДЛЯ ПОКАЗА ТОЧКИ ПОВОРОТА '''
        # self.rotatePoint.reShow(self)

    def saveCanva(self, f):
        pickle.dump(self.polygons, f)

    def loadCanva(self, f):
        try:
            polygons = pickle.load(f)
        except:
            print('Ошибка загрузки полигона')
            return Tools.EXIT_FAILURE

        self.clear()

        self.polygons = polygons
        self.update()
        return Tools.EXIT_SUCCESS

    def updateShowFlags(self):
        super(PolygonField, self).updateShowFlags()
        for pol in self.polygons:
            pol.updateShowFlag(self.ShowComments)

    def editRightClick(self, root, XEvent, YEvent):
        for pol in self.polygons:
            for i, point in enumerate(pol.points):
                if point.isClick(self, XEvent, YEvent):
                    z = Toplevel(root)
                    z.geometry('200x200')
                    z.title('')
                    z['bg'] = Settings.COLOR_MAIN_BG
                    z.resizable(0, 0)

                    f = EditPoint(z, point, 200, 200, self)
                    f.show()

    def shiftRightClick(self, root, XEvent, YEvent):
        for pol in self.polygons:
            for i, point in enumerate(pol.points):
                if point.isClick(self, XEvent, YEvent):
                    z = Toplevel(root)
                    z.geometry('200x200')
                    z.title('')
                    z['bg'] = Settings.COLOR_MAIN_BG
                    z.resizable(0, 0)

                    f = ShiftSegPoint(z, pol, 200, 200, self)
                    f.show()

    def rightClick(self, XEvent, YEvent):
        j = 0
        while j >= 0 and j < len(self.polygons) and len(self.polygons) > 0:
            pol = self.polygons[j]
            for i, point in enumerate(pol.points):
                if point.isClick(self, XEvent, YEvent):
                    pol.hide(self)
                    self.polygons.pop(j)
                    j -= 1
            j += 1

        self.update()
        self.save()

    def changeColor(self, XEvent, YEvent):
        color = askcolor()[1]
        if not color:
            return

        for pol in self.polygons:
            for i, point in enumerate(pol.points):
                if point.isClick(self, XEvent, YEvent):
                    pol.changeColor(color, color)

        self.update()
        self.save()

    def startNewPolygon(self, event):
        self.polygons.append(CanvasPolLine([], color=self.colorNowPol, method=self.method))

    def startNewPolygonClose(self, event):
        try:
            lastPoint = CanvasPoint(self.polygons[-1].points[0].x, self.polygons[-1].points[0].y, color=self.colorNowPol)
            self.polygons[-1].addPoint(self, lastPoint)
        except:
            pass
        self.startNewPolygon(event)

    def updatePoints(self):
        self.points = []
        for pol in self.polygons:
            for i in pol.points:
                self.points.append(i)

    def isPointInPol(self, X, Y):
        for pol in self.polygons:
            if pol.isPointOn(self, X, Y):
                return True
        return False

    def pointInPolWithPoint(self, X, Y):
        for pol in self.polygons:
            p = pol.PointOnWithPoint(self, X, Y)
            if p:
                return p
        return None

    def polWithPoint(self, X, Y):
        for pol in self.polygons:
            p = pol.PointOnWithPoint(self, X, Y)
            if p:
                return pol
        return None

    def showPoint(self, x, y, color=Settings.COLOR_NEW_POINT):
        point = CanvasPoint(float(x), float(y), showComments=self.ShowComments, color=self.colorNowPol)
        if len(self.polygons) == 0 or self.polygons[-1].countPoints() >= 2:
            self.startNewPolygon('plug')
        self.polygons[-1].addPoint(self, point)

    def delPoint(self, point):
        wasDel = False
        for pol in self.polygons:
            wasDel += pol.delPoint(self, point)

        self.update()
        return wasDel

    def delSegment(self, pointStart, pointEnd):
        wasDel = False
        for i, pol in enumerate(self.polygons):
            rc = pol.isEqualPol(pointStart, pointEnd)
            wasDel += rc
            if rc:
                pol.hide(self)
                self.polygons.pop(i)

        self.update()
        return wasDel

    def rotate(self, pointerCenter, alpha):
        for pol in self.polygons:
            pol.hide(self)
            pol.rotatePol(pointerCenter, alpha)

        self.rotatePoint = pointerCenter
        self.update()
        self.save()

    def shift(self, xShift, yShift):
        for pol in self.polygons:
            pol.hide(self)
            pol.shiftPol(xShift, yShift)

        self.update()
        self.save()

    def scale(self, x, y, kx, ky):
        for pol in self.polygons:
            pol.hide(self)
            pol.scalePol(x, y, kx, ky)

        self.update()
        self.save()

    def mouseRotate(self, mode):
        if mode == 'r':
            self.rotate(self.rotatePoint, -15)
        elif mode == 'l':
            self.rotate(self.rotatePoint, 15)

    def addSegment(self, x1, y1, x2, y2, color=None):
        wasColor = self.colorNowPol
        if color:
            self.colorNowPol = color

        if len(self.polygons) > 0 and self.polygons[-1].countPoints() < 2:
            self.polygons[-1].hide(self)
            self.polygons.pop()

        if len(self.polygons) == 0:
            self.startNewPolygon('plug')

        if self.polygons[-1].countPoints() == 2:
            self.startNewPolygon('plug')

        start = CanvasPoint(x1, y1, self.polygons[-1].colorLine, showComments=self.ShowComments)
        end = CanvasPoint(x2, y2, self.polygons[-1].colorLine, showComments=self.ShowComments)

        self.polygons[-1].addPoint(self, start)
        self.polygons[-1].addPoint(self, end)

        self.colorNowPol = wasColor

        return self.polygons[-1]

    def copy(self, window, XEvent, YEvent, method, color):
        for pol in self.polygons:
            if pol.countPoints() < 2:
                continue

            flagStop = False
            for i, point in enumerate(pol.points):
                if point.isClick(self, XEvent, YEvent):
                    methodNow = self.method
                    colorNow = self.colorNowPol
                    self.method = method
                    self.colorNowPol = color
                    self.addSegment(pol.points[0].x, pol.points[0].y, pol.points[1].x, pol.points[1].y)
                    self.method = methodNow
                    self.colorNowPol = colorNow
                    flagStop = True
            if flagStop:
                break

        self.update()
        self.save()

    def change_min_len_coords(self):
        pass
        # width = self.winfo_reqwidth()
        # peopleWidth =


class WrapCanva:
    def __init__(self, window, Canva=PolygonField, **kwargs):
        self.window = window

        self.frame = Frame(window)
        self.canva = Canva(self.frame, self.window, showArrows=False, **kwargs)
        self.frame.bind('<Configure>', self.resize, '+')
        self.canva.place(x=0, y=0)

        self.pointMenu = None
        self.Xevent, self.Yevent = None, None
        self.bind()

        image = ImageTk.PhotoImage(file=r"C:\projects\Сomputer graphics\lab_02\shared\rootIcon4.png")
        self.canva.create_image(10, 10, image=image, anchor=NW)

    def bind(self):
        self.window.bind("<Right>", lambda event: self.canva.arrowMoveAcrossField('X', 'right'), '+')
        self.window.bind("<Left>", lambda event: self.canva.arrowMoveAcrossField('X', 'left'), '+')
        self.window.bind("<Up>", lambda event: self.canva.arrowMoveAcrossField('Y', 'up'), '+')
        self.window.bind("<Down>", lambda event: self.canva.arrowMoveAcrossField('Y', 'down'), '+')

        # self.window.bind("<Control-equal>", lambda event: self.canva
        # .changeCoef('+', 'X', 'Y'))
        # self.window.bind("<Control-minus>", lambda event: self.canva.changeCoef('-', 'X', 'Y'))

        self.window.bind("<Control-equal>", lambda event: self.canva.scale(0, 0, 2, 2), '+')
        self.window.bind("<Control-minus>", lambda event: self.canva.scale(0, 0, 0.5, 0.5), '+')

        self.window.bind("<Control-z>", lambda event: self.window.loadVersion(), '+')
        self.window.bind("<Control-s>", lambda event: self.window.loadVersion(), '+')
        self.window.bind("<Control-p>", lambda event: self.canva.mouseRotate('r'), '+')
        self.window.bind("<Control-o>", lambda event: self.canva.mouseRotate('l'), '+')

        self.window.bind("<Control-space>", lambda event: self.canva.startNewPolygonClose(event), '+')
        self.window.bind("<Control-Shift-space>", lambda event: self.canva.startNewPolygon(event), '+')


        submenu = Menu(self.pointMenu, tearoff=False)
        submenu.add_command(label="Copy use dda", command=lambda: self.canva.copy(self.window, self.Xevent, self.Yevent, Tools.M_CDA, Settings.COLOR_DDA))
        submenu.add_command(label="Copy use B[float]", command=lambda: self.canva.copy(self.window, self.Xevent, self.Yevent, Tools.M_BREZENHAM_FLOAT, Settings.COLOR_B_FLOAT))
        submenu.add_command(label="Copy use B[int]", command=lambda: self.canva.copy(self.window, self.Xevent, self.Yevent, Tools.M_BREZENHAM_INT, Settings.COLOR_B_INT))
        submenu.add_command(label="Copy use B with elimination", command=lambda: self.canva.copy(self.window, self.Xevent, self.Yevent, Tools.M_BREZENHAM_ELIMINATION, Settings.COLOR_B_WITHOUT))
        submenu.add_command(label="Copy use WU", command=lambda: self.canva.copy(self.window, self.Xevent, self.Yevent, Tools.M_VY, Settings.COLOR_WU))
        submenu.add_command(label="Copy use graphic primitives", command=lambda: self.canva.copy(self.window, self.Xevent, self.Yevent, Tools.M_USUAL, Settings.COLOR_USUAL))

        self.pointMenu = Menu(self.canva, tearoff=0)
        self.pointMenu.add_cascade(label="Copy", menu=submenu)
        self.pointMenu.add_command(label="Edit", command=lambda: self.canva.editRightClick(self.window, self.Xevent, self.Yevent))
        self.pointMenu.add_command(label="Delete", command=lambda: self.canva.rightClick(self.Xevent, self.Yevent))
        self.pointMenu.add_command(label="Shift", command=lambda: self.canva.shiftRightClick(self.window, self.Xevent, self.Yevent))
        self.pointMenu.add_command(label="Change color", command=lambda: self.canva.changeColor(self.Xevent, self.Yevent))
        self.pointMenu.add_command(label="Set rotate point", command=lambda: self.changeRotatePoint())
        self.pointMenu.add_command(label="Parallel beam", command=lambda: self.ParallelBeam(self.Xevent, self.Yevent))
        self.pointMenu.add_command(label="Сircular beam", command=lambda : self.circularBeam(self.Xevent, self.Yevent))

        self.mainMenu = Menu(self.canva, tearoff=0)
        self.mainMenu.add_command(label="Rotate", command=lambda: self.action(RotateFrame))
        self.mainMenu.add_command(label="Shift", command=lambda: self.action(ShiftFrame))
        self.mainMenu.add_command(label="Scale", command=lambda: self.action(ScaleFrameSecondVersion))
        self.mainMenu.add_command(label="Set rotate point", command=lambda: self.changeRotatePoint())
        self.mainMenu.add_command(label="Change bg color", command=lambda: self.canva.changeBGColor())

        self.window.bind("<Button-3>", lambda event: self.rightClick(event), '+')


    def ParallelBeam(self, x, y):
        pol = self.canva.polWithPoint(x, y)
        if not pol:
            print('Полигон не найден')
            return

        u = Toplevel(self.window)
        u.geometry('200x200')
        u.title('')
        u['bg'] = Settings.COLOR_MAIN_BG
        u.resizable(0, 0)
        f = XYForm(u, Settings.COLOR_MAIN_BG, 'Shift', Settings.WIDTH_INPUT,
                    lambda: self.sh(u, f, pol), '  Go  ')
        f.insertXY(5, 0)
        f.show(Settings.COLOR_MAIN_BG)

    def sh(self, u, f, pol):
        x, y = f.getXY()
        if not Tools.isFloat(x) or not Tools.isFloat(y):
            showinfo('Error', 'Неверный ввод')
            return

        x, y = float(x), float(y)

        wasMethod = self.canva.method
        wasColor = self.canva.colorNowPol

        j = 0
        for i in range(len(Tools.METHODS)):
            j += 1
            if Tools.METHODS[i] == pol.method:
                j -= 1
                continue
            self.canva.method = Tools.METHODS[i]
            self.canva.addSegment(pol.points[0].x + j * x, pol.points[0].y + j * y, pol.points[1].x + j * x, pol.points[1].y + j * y, color=Settings.M_COLORS[i])

        u.destroy()

        self.canva.method = wasMethod
        self.canva.color = wasColor
        self.canva.save()


    def circularBeam(self, x, y):
        pol = self.canva.polWithPoint(x, y)
        if not pol:
            print('Полигон не найден')
            return

        p = self.canva.pointInPolWithPoint(x, y)
        if not p:
            print('Точка в полиноме не найдена')
            return

        u = Toplevel(self.window)
        u.geometry('200x200')
        u.title('')
        u['bg'] = Settings.COLOR_MAIN_BG
        u.resizable(0, 0)
        f = XYXForm(u, Settings.COLOR_MAIN_BG, 'Rotate', Settings.WIDTH_INPUT,
                    lambda: self.rot(u, f, pol, p), '  Go  ')
        f.insertXY(0, 360, 5)
        f.show(Settings.COLOR_MAIN_BG)

    def rot(self, u, f, pol, p):
        start, end, step = f.getXY()
        if not Tools.isFloat(start) or not Tools.isFloat(end) or not Tools.isFloat(step):
            showinfo('Error', 'Неверный ввод')
            return

        start, end, step = map(float, (start, end, step))
        if start >= end:
            showinfo('Error', 'Start >= End')
            return

        if step > end - start:
            showinfo('Error', 'Step > end - start')
            return

        if step <= 0:
            showinfo('Error', 'Step <= 0')
            return

        i = start
        while i < end:
            polCopy = copy.deepcopy(pol)
            polCopy.rotatePol(p, i)
            self.canva.polygons.append(polCopy)
            i += step

        u.destroy()

        self.canva.update()
        self.canva.save()

    def changeRotatePoint(self):
        x = int(self.canva.XShiftCP(self.Xevent))
        y = int(self.canva.YShiftCP(self.Yevent))
        self.canva.rotatePoint = CanvasPoint(x, y,
                               self.canva.colorPoints, showComments=self.canva.ShowComments)
        showinfo('Info', 'Новый центр поворота установлен успешно.\n\n'
                         f'X: {x}\n'
                         f'Y: {y}\n')


    def action(self, frame):
        z = Toplevel(self.window)
        z.geometry('200x200')
        z.title('')
        z['bg'] = Settings.COLOR_MAIN_BG
        z.resizable(0, 0)
        f = frame(z, 200, 200, self)
        f.show()

    def rightClick(self, event):
        self.Xevent = event.x
        self.Yevent = event.y

        isPointHere = self.canva.isPointInPol(self.Xevent, self.Yevent)

        if isPointHere:
            self.pointMenu.post(event.x_root, event.y_root)
        else:
            self.mainMenu.post(event.x_root, event.y_root)

    def resize(self, event):
        self.canva.resize(event)
        self.canva.change_min_len_coords()

    def show(self, x, y, relwidth, relheight):
        self.frame.place(x=x, y=y, relwidth=relwidth, relheight=relheight)

    def clear(self):
        self.canva.clearAll()

    def getPoints(self):
        return [point for p in self.canva.polygons for point in p.points]

    def getPointsForSave(self):
        return [[point for point in p.points] for p in self.canva.polygons]

    def saveVersion(self, f):
        self.canva.saveCanva(f)

    def loadVersion(self, f):
        return self.canva.loadCanva(f)

    def radioShowComments(self):
        self.canva.ShowComments = not self.canva.ShowComments
        self.canva.update()

    def changeColorNewPol(self):
        color = askcolor()[1]
        if not color:
            return

        self.canva.colorNowPol = color
        self.canva.polygons[-1].changeColor(color, color)

        self.canva.update()
        self.canva.save()
