from tkinter import *
from tkinter.messagebox import *
import tkinter.filedialog as fd

from view.Btn import WrapButton
from view.CanvasPoint import CanvasPoint
from view.Settings import Settings
from view.keyInput import *
from tkinter import ttk

from model.Tools import Tools
from model.randomClipperAlg import randomCut

import controll.controllModel


def addPointKey(canva, XYform):
    x, y = XYform.getXY()
    if not Tools.isFloat(x) or not Tools.isFloat(y):
        showinfo('Error', 'Неверно введены координаты точки (должны быть целые числа)')
        return

    canva.canva.showPoint(float(x), float(y))
    XYform.clear()

    canva.canva.myUpdate()
    canva.canva.save()


def delPointKey(canva, XYform):
    x, y = XYform.getXY()
    print(x, y)
    if not Tools.isFloat(x) or not Tools.isFloat(y):
        showinfo('Error', 'Неверно введены координаты точки (должны быть целые числа)')
        return

    delPoint = CanvasPoint(float(x), float(y))
    flagWasPoint = canva.canva.delPoint(delPoint)

    if not flagWasPoint:
        showinfo('Warning', 'Точки с такими координатами не найдено')
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

    #canva.canva.clear()
    for c in coords:
        for p in c:
            canva.canva.showPoint(p[0], p[1])

        if len(c) > 1 and c[0] == c[-1]:
            canva.canva.polygons[-1].fillFlag = True

        canva.canva.startNewPolygon('sdfv')

    canva.canva.myUpdate()
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

        self.bClear = WrapButton(self.f, txt='🗑', command=lambda: clearCanva(self.canva), name='clear all')
        self.bInput = WrapButton(self.f, txt='📂', command=lambda: inputPointsFromFile(self.canva), name='take points from file')
        self.bSave = WrapButton(self.f, txt='📋', command=lambda: savePointsToFile(self.canva), name='save points')
        self.bReturn = WrapButton(self.f, txt='⏎', command=lambda: root.loadVersion(), name='cancel')
        self.bGo = WrapButton(self.f, txt='🚀', command=lambda: goCut(root, c), name='cut')

    def show(self, posx=Settings.X_CANVA, posy=Settings.Y_INPUT + 9):
        startX, startY = 0, 0
        lst_show = [self.bReturn, self.bInput, self.bSave, self.bClear, self.bGo]
        for i in range(len(lst_show)):
            lst_show[i].show(posx=startX + i * Settings.BTN_STEP, posy=startY)
        # self.bReturn.show(posx=startX, posy=startY)
        # self.bInput.show(posx=startX + 1 * Settings.BTN_STEP, posy=startY)
        # self.bSave.show(posx=startX + 2 * Settings.BTN_STEP, posy=startY)
        # self.bClear.show(posx=startX + 1 * Settings.BTN_STEP, posy=startY)
        # self.bGo.show(posx=startX + 2 * Settings.BTN_STEP, posy=startY)

        self.f.place(x=posx, y=posy)


def goCut(root, c):
    canva = c.canva
    clippers = []
    segments = []

    for i in canva.polygons:
        if i.segmentOrClipper and len(i.points) == 2:
            segments.append(i)

        if not i.segmentOrClipper and len(i.points) > 2:
            clippers.append(i)

    print(len(segments))
    print(len(clippers))
    print(len(canva.polygons))

    for s in segments:
        s.cutArea = []

        for c in clippers:
            c.findFieldLines(canva)

        for c in clippers:
            # SE -- [(x, y), (x, y)]
            SE = randomCut(s, c)
            print('SE = ', SE)
            if SE != 'error':
                if len(SE) == 0:
                    s.cutArea.append( () )
                    continue

                p1 = (round(SE[0][0]), round(SE[0][1]))
                p2 = (round(SE[1][0]), round(SE[1][1]))

                s.cutArea.append( (p1, p2) if p1[0] < p2[0] else (p2, p1) )

        s.updateWasGoFlag(True)
        s.reShow(canva)


def updateMethod(event, field):

    def updateInOrOut(flag):
        for p in field.canva.polygons:
            p.InOrOut = flag
        field.canva.InOrOut = flag

    def updateDiffColors(flag):
        if field.canva.diffColors == flag:
            return
        for p in field.canva.polygons:
            p.diffColors = flag
        field.canva.diffColors = flag

    if event == "In":
        updateInOrOut(True)
        updateDiffColors(False)
    elif event == "Out":
        updateInOrOut(False)
        updateDiffColors(False)
    elif event == "Different colors":
        updateDiffColors(True)
    else:
        print('Неверный метод')

def selectMethod(root, field):
    font = ("Arial", 10)
    cb = ttk.Combobox(root, values=["In", "Out", "Different colors"], font=font, state="readonly")
    root.option_add('*TCombobox*Listbox.font', font)
    cb.place(relx=0.742, y=Settings.Y_INPUT + 34)

    cb.current(0)

    cb.bind("<<ComboboxSelected>>", lambda event: updateMethod(cb.get(), field))