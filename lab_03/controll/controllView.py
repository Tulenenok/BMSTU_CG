from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import tkinter.filedialog as fd

from view.Btn import WrapButton
from view.CanvasPoint import CanvasPoint
from view.Graphs import Analysis
from view.Settings import Settings
from view.keyInput import *

from model.Tools import Tools

import controll.controllModel
import copy


def addPointKey(canva, XYform):
    x1, y1, x2, y2 = XYform.getXY()
    if not Tools.isFloat(x1) or not Tools.isFloat(y1) or not Tools.isFloat(x2) or not Tools.isFloat(y2):
        showinfo('Error', 'Неверно введены координаты отрезка (должны быть целые числа)')
        return

    # if x1 == x2 and y1 == y2:
    #     showinfo('Error', 'Вы пытаетесь создать вырожденный отрезок')
    #     return

    canva.canva.addSegment(float(x1), float(y1), float(x2), float(y2))
    XYform.clear()

    canva.canva.update()
    canva.canva.save()

def addBeamKey(canva, XYXYXYform):
    x, y, len, start, end, step = XYXYXYform.getXY()
    if not Tools.isFloat(x) or not Tools.isFloat(y):
        showinfo('Error', 'Неверно введены координаты начала [float]')
        return

    if not Tools.isFloat(len) or float(len) <= 0:
        showinfo('Error', 'Неверно введена длина [float, > 0]')
        return

    if not Tools.isFloat(start) or not Tools.isFloat(end) or not Tools.isFloat(step):
        showinfo('Error', 'Неверный ввод углов [float]')
        return

    x, y, len = map(float, (x, y, len))
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

    pol = canva.canva.addSegment(x, y, x + len, y)
    p = CanvasPoint(x, y)
    i = start
    while i < end + step:
        polCopy = copy.deepcopy(pol)
        polCopy.rotatePol(p, i)
        canva.canva.polygons.append(polCopy)
        i += step

    canva.canva.update()
    canva.canva.save()

def delBeamKey(canva, XYform):
    x, y = XYform.getXY()
    if not Tools.isFloat(x) or not Tools.isFloat(y):
        showinfo('Error', 'Неверно введены координаты отрезка [float]')
        return

    x = canva.canva.XShiftPC(float(x))
    y = canva.canva.YShiftPC(float(y))

    canva.canva.rightClick(x, y)

    canva.canva.update()
    canva.canva.save()


def delPointKey(canva, XYform):
    x1, y1, x2, y2 = XYform.getXY()
    if not Tools.isFloat(x1) or not Tools.isFloat(y1) or not Tools.isFloat(x2) or not Tools.isFloat(y2):
        showinfo('Error', 'Неверно введены координаты точки (должны быть целые числа)')
        return

    startPoint = CanvasPoint(float(x1), float(y1))
    endPoint = CanvasPoint(float(x2), float(y2))
    flagWasPoint = canva.canva.delSegment(startPoint, endPoint)

    if not flagWasPoint:
        showinfo('Warning', 'Отрезка с такими координатами не найдено')
        return

    XYform.clear()
    canva.canva.save()


def inputPointsFromFile(canva):
    filetypes = (("Текстовый файл", "*.txt"), ("Excel", "*.xlsx"))
    filename = fd.askopenfilename(title="Открыть файл", initialdir=Settings.DIR_INPUT_POINTS,
                                  filetypes=filetypes, multiple=False)
    if filename and filename[-4::] == '.txt':
        coords = controll.controllModel.inputPointsTXT(filename)
        if Tools.isFloat(coords):
            showinfo('Ошибка открытия файла' if coords == Tools.INVALID_FILENAME else 'Неверный формат данных',
                     'Неверно указано название файла' if coords == -1 else f'Произошла ошибка на {coords} строке. \n\n'
                              'Проверьте, что координаты точек введены в формате x ; y и что каждая точка введена '
                              'на новой строке')
            return

    elif filename and filename[-5::] == '.xlsx':
        coords = controll.controllModel.inputPointsXLSX(filename)
        if Tools.isInt(coords):
            if coords == Tools.INVALID_FILENAME:
                showinfo('Ошибка открытия файла', 'Неверно указано название файла')
            elif coords == Tools.INVALID_LISTNAME:
                showinfo('Ошибка названия листа', 'Не удалось найти лист с названием Points')
            elif coords == Tools.INVALID_HEAD:
                showinfo('Ошибка заголовка таблицы', 'Проверьте, что заголовок таблицы содержит названия X и Y')
            elif coords == Tools.INVALID_DATA:
                showinfo('Ошибка чтения данных', 'Проверьте, что количество х-сов совпадает с количеством y-ков')
            elif coords == Tools.INVALID_FORMAT_DATA:
                showinfo('Ошибка чтения данных', 'Формат данных неверный (ожидались вещественные числа)')
            else:
                showinfo('Error', 'Непонятная ошибка, но мы работаем над этим')
            return
    elif filename:
        showinfo('Ошибка открытия файла', 'Неверно указано название файла')
        return
    else:
        return

    if coords == [[]]:
        showinfo('Empty file', 'Выбранный файл не содержит данных, точки не обновлены.')
        return

    canva.canva.clear()
    for c in coords:
        for p in c:
            canva.canva.showPoint(p[0], p[1])
        canva.canva.startNewPolygon('sdfv')

    canva.canva.update()
    canva.canva.save()


def savePointsToFile(canva):
    new_file = fd.asksaveasfile(title="Сохранить файл", defaultextension=".txt",
                                filetypes=(("Текстовый файл", "*.txt"), ))
    if new_file:
        for pol in canva.getPointsForSave():
            for p in pol:
                new_file.write(p.likeStr() + '\n')
            new_file.write(Tools.SEPARATOR_POL + '\n')
        new_file.close()


def clearCanva(canva):
    canva.clear()
    canva.canva.save()


def scaleShiftRotate(root, canva):
    z = ZoomRotateShift(root, canva)
    z.show()


class UpButtons:
    def __init__(self, root, c):
        self.root = root
        self.canva = c
        self.f = Frame(self.root, width=500, height=60)
        self.f['bg'] = Settings.COLOR_MAIN_BG

        self.bClear = WrapButton(self.f, txt='🗑', command=lambda: clearCanva(self.canva), name='clean all')
        self.bInput = WrapButton(self.f, txt='📂', command=lambda: inputPointsFromFile(self.canva), name='take points from file')
        self.bSave = WrapButton(self.f, txt='📋', command=lambda: savePointsToFile(self.canva), name='save points')
        self.bReturn = WrapButton(self.f, txt='⏎', command=lambda: root.loadVersion(), name='cancel')
        self.bGo = WrapButton(self.f, txt='🔄', command=lambda: scaleShiftRotate(root, c), name='scale shift rotate')
        self.bAn = WrapButton(self.f, txt='🚀', command=lambda: Analysis(root, c), name='analysis')

    def show(self, posx=Settings.X_CANVA, posy=Settings.Y_INPUT + 9):
        startX, startY = 0, 0
        self.bReturn.show(posx=startX, posy=startY)
        self.bInput.show(posx=startX + 1 * Settings.BTN_STEP, posy=startY)
        self.bSave.show(posx=startX + 2 * Settings.BTN_STEP, posy=startY)
        self.bClear.show(posx=startX + 3 * Settings.BTN_STEP, posy=startY)
        # self.bGo.show(posx=startX + 4 * Settings.BTN_STEP, posy=startY)
        self.bAn.show(posx=startX + 4 * Settings.BTN_STEP, posy=startY)

        self.f.place(x=posx, y=posy)


def updateMethod(event, field):
    print('Ok')
    if event == "ЦДА":
        field.canva.method = Tools.M_CDA
        field.canva.colorNowPol = Settings.COLOR_DDA # малиновый
    elif event == "Брезенхем [float]":
        field.canva.method = Tools.M_BREZENHAM_FLOAT
        field.canva.colorNowPol = Settings.COLOR_B_FLOAT
    elif event == "Брезенхем [int]":
        field.canva.method = Tools.M_BREZENHAM_INT
        field.canva.colorNowPol = Settings.COLOR_B_INT
    elif event == "Брезенхем с устранением ступенчатости":
        field.canva.method = Tools.M_BREZENHAM_ELIMINATION
        field.canva.colorNowPol = Settings.COLOR_B_WITHOUT
    elif event == "ВУ":
        field.canva.method = Tools.M_VY
        field.canva.colorNowPol = Settings.COLOR_WU
    elif event == "Граф примитив":
        field.canva.method = Tools.M_USUAL
        field.canva.colorNowPol = Settings.COLOR_USUAL
    else:
        print('Неверный метод')


def selectMethod(root, field):
    font = ("Arial", 10)
    cb = ttk.Combobox(root, values=["ЦДА", "Брезенхем [float]", "Брезенхем [int]",
                                    "Брезенхем с устранением ступенчатости", "ВУ", "Граф примитив"], font=font, state="readonly")
    root.option_add('*TCombobox*Listbox.font', font)
    cb.place(relx=0.742, y=Settings.Y_INPUT + 34)

    cb.current(0)

    cb.bind("<<ComboboxSelected>>", lambda event: updateMethod(cb.get(), field))