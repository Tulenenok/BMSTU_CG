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

from view.SergFunc import *


def controllAddCircle(canva, XYform):
    x, y, r = XYform.getXY()
    if not Tools.isFloat(x) or not Tools.isFloat(y) or not Tools.isFloat(r) :
        showinfo('Error', 'Неверно введены координаты отрезка (должны быть целые числа)')
        return

    if float(r) <= 0:
        showinfo('Error', 'R <= 0')
        return

    canva.canva.addCircle(float(x), float(y), float(r))
    XYform.clear()

    canva.canva.update()
    canva.canva.save()


def controllAddEllipse(canva, XYXYXYform):
    x, y, a, b = XYXYXYform.getXY()
    if not Tools.isFloat(x) or not Tools.isFloat(y) or not Tools.isFloat(a) or not Tools.isFloat(b):
        showinfo('Error', 'Неверный ввод [float]')
        return

    if float(a) <= 0:
        showinfo('Error', 'Неверно введно а [>0]')
        return

    if float(b) <= 0:
        showinfo('Error', 'Неверно введно b [>0]')
        return

    x, y, a, b = map(float, (x, y, a, b))

    canva.canva.addEllipse(x, y, a, b)
    XYXYXYform.clear()

    canva.canva.update()
    canva.canva.save()


def controllDelEllipse(canva, XYform):
    x, y, a, b = XYform.getXY()
    if not Tools.isFloat(x) or not Tools.isFloat(y) or not Tools.isFloat(a) or not Tools.isFloat(b):
        showinfo('Error', 'Неверно введены координаты (должны быть целые числа)')
        return

    center = CanvasPoint(float(x), float(y))
    flagWasPoint = canva.canva.delEllipse(center, float(a), float(b))

    if not flagWasPoint:
        showinfo('Warning', 'Эллипса с такими координатами не найдено')
        return

    XYform.clear()
    canva.canva.save()


def controllDelCircle(canva, XYform):
    x, y, r = XYform.getXY()
    if not Tools.isFloat(x) or not Tools.isFloat(y):
        showinfo('Error', 'Неверно введены координаты (должны быть целые числа)')
        return

    center = CanvasPoint(float(x), float(y))
    flagWasPoint = canva.canva.delCircle(center, float(r))

    if not flagWasPoint:
        showinfo('Warning', 'Окружности с такими координатами не найдено')
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
        # self.bInput = WrapButton(self.f, txt='📂', command=lambda: inputPointsFromFile(self.canva), name='take points from file')
        # self.bSave = WrapButton(self.f, txt='📋', command=lambda: savePointsToFile(self.canva), name='save points')
        self.bReturn = WrapButton(self.f, txt='⏎', command=lambda: root.loadVersion(), name='cancel')
        self.bGo = WrapButton(self.f, txt='🔄', command=lambda: scaleShiftRotate(root, c), name='scale shift rotate')
        #self.bAn = WrapButton(self.f, txt='🚀', command=lambda: Analysis(root, c), name='analysis')
        self.ksdc = WrapButton(self.f, txt='🚀', command=lambda: measure_time(), name='analysis')
        self.bAn = WrapButton(self.f, txt='💤', command=lambda: scaleShiftRotate(root, c), name='beam')

    def show(self, posx=Settings.X_CANVA, posy=Settings.Y_INPUT + 9):
        startX, startY = 0, 0
        self.bReturn.show(posx=startX, posy=startY)
        # self.bInput.show(posx=startX + 1 * Settings.BTN_STEP, posy=startY)
        # self.bSave.show(posx=startX + 2 * Settings.BTN_STEP, posy=startY)
        self.bClear.show(posx=startX + 1 * Settings.BTN_STEP, posy=startY)
        # self.bGo.show(posx=startX + 4 * Settings.BTN_STEP, posy=startY)
        self.bAn.show(posx=startX + 2 * Settings.BTN_STEP, posy=startY)
        self.ksdc.show(posx=startX + 3 * Settings.BTN_STEP, posy=startY)

        self.f.place(x=posx, y=posy)


def updateMethod(event, field):
    if event == "Канон. ур-ние":
        field.canva.method = Tools.M_CANONICAL
        field.canva.colorNowPol = Settings.COLOR_CANONICAL
    elif event == "Парам. ур-ние":
        field.canva.method = Tools.M_PARAMETRIC
        field.canva.colorNowPol = Settings.COLOR_PARAMETRIC
    elif event == "Брезенхем":
        field.canva.method = Tools.M_BREZENHAM
        field.canva.colorNowPol = Settings.COLOR_B
    elif event == "Средняя точка":
        field.canva.method = Tools.M_MIDDLE_POINT
        field.canva.colorNowPol = Settings.COLOR_MIDDLE_POINT
    elif event == "Библиотека":
        field.canva.method = Tools.M_USUAL
        field.canva.colorNowPol = Settings.COLOR_USUAL
    else:
        print('Неверный метод')


def selectMethod(root, field):
    font = ("Arial", 10)
    cb = ttk.Combobox(root, values=["Канон. ур-ние", "Парам. ур-ние", "Брезенхем", "Средняя точка", "Библиотека"], font=font, state="readonly")
    root.option_add('*TCombobox*Listbox.font', font)
    cb.place(relx=0.742, y=Settings.Y_INPUT + 34)

    cb.current(0)

    cb.bind("<<ComboboxSelected>>", lambda event: updateMethod(cb.get(), field))