from tkinter import *
from view.Settings import Settings
from view.Btn import WrapButton
from view.keyInput import *
from view.frames import *
from model.Point import *
from model.algConstructSeg import *
# from controll.controllView import selectMethod

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import random


def random_color():
    return f"#{random.randrange(0x1000000):06x}"


class Analysis:
    def __init__(self, root, canva):
        self.root = root
        self.canva = canva

        self.z = Tk()
        self.z.geometry('690x420')
        self.z.title('А давайте построим гистограммы')
        self.z['bg'] = Settings.COLOR_MAIN_BG
        # self.z.resizable(0, 0)
        self.colors = plt.cm.BuPu(np.linspace(0.6, 1, 5))
        self.mainColor = Settings.COLOR_BAR

        self.data = []
        self.alpha = []
        self.lenSeg = None

        self.fig = Figure(figsize=(5, 4), dpi=73)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.z)

        self.segmentForm = XYXYForm(self.z, Settings.COLOR_MAIN_BG, 'Start segment', Settings.WIDTH_INPUT,
                       lambda: self.plug(), '  Show  ', showButton=False)
        self.segmentForm.show(Settings.COLOR_MAIN_BG, 10, 10)
        self.segmentForm.insertXY(0, 0, 1, 0)

        #self.changeGraph(self.data, self.alpha, self.lenSeg)

        self.xEntry = Entry(self.z, width=10)
        self.xEntry.place(x=10, y=195)
        self.xEntry.insert(0, 90)

        self.addbtn = Button(self.z, text='add α', command=self.add)
        self.addbtn.place(x=80, y=192)
        self.delbtn = Button(self.z, text='del ✔', command=self.delHighlighted)
        self.delbtn.place(x=125, y=192)

        self.gobtn = Button(self.z, text='go 💡', command=self.go)
        self.gobtn.place(x=10, rely=0.9, relwidth=0.97)

        self.alphaFrame = Check(self.z, [])
        self.alphaFrame.addString('0')
        self.alphaFrame.place(x=10, y=222, relheight=0.32)

        self.t = Label(self.z, text="Нажмите go, чтобы построить первую гистограмму", bg=Settings.COLOR_MAIN_BG, font=('Arial', 10, 'bold'), fg="#f1e4de")
        self.t.place(x=265, y=190)

        self.menu = Menu(self.z, tearoff=0)
        self.menu.add_cascade(label='Clean', menu=self.__makeDropDown({'Clean all': lambda: self.clearResult(),
                                                                       'Clean segment': lambda: self.segmentForm.insertXY('', '', '', ''),
                                                                       'Clean corners': lambda: self.alphaFrame.clearAll(),
                                                                       'Clean graph': lambda: self.clear(),
                                                                       'Clean canva': lambda: self.canva.canva.clear(),
                                                                      }))
        self.menu.add_cascade(label='Generate', menu=self.__makeDropDown({'Gen α': lambda: self.genAlphaField()}))
        self.z.config(menu=self.menu)

        self.oneColorBtn = Checkbutton(self.z, text="One color", bg=Settings.COLOR_MAIN_BG, command=self.toogleColor)
        self.cleanCanvaBtn = Checkbutton(self.z, text="Clean canva", bg=Settings.COLOR_MAIN_BG, command=self.toogleClean)
        self.cleanCanvaBtn.select()
        self.cleanCanvaFlag = True
        self.oneColorFlag = False

        self.settingFlags()
        self.bind()

        # selectMethod(self.z, self.canva)

    def __makeDropDown(self, dictLabels):
        newItem = Menu(self.menu, tearoff=0)
        for item in dictLabels:
            newItem.add_command(label=item, command=dictLabels[item])
        return newItem

    def settingFlags(self):
        self.cleanCanvaBtn.place(x=300, y=10)
        self.oneColorBtn.place(x=200, y=10)

    def toogleColor(self):
        self.oneColorFlag = not self.oneColorFlag

    def toogleClean(self):
        self.cleanCanvaFlag = not self.cleanCanvaFlag

    def genAlphaField(self):
        u = Toplevel(self.z)
        u.geometry('200x200')
        u.title('')
        u['bg'] = Settings.COLOR_MAIN_BG
        u.resizable(0, 0)
        f = XYXForm(u, Settings.COLOR_MAIN_BG, 'Gen alpha', Settings.WIDTH_INPUT,
                       lambda: self.gen(u, f), '  Gen  ')
        f.insertXY(0, 360, 5)
        f.show(Settings.COLOR_MAIN_BG)

    def gen(self, u, f):
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

        self.alphaFrame.clearAll()

        i = start
        while i < end + step:
            self.alphaFrame.addString(i)
            i += step

        u.destroy()


    def clearResult(self):
        self.canva.canva.clear()
        self.clear()
        self.segmentForm.insertXY('', '', '', '')
        self.alphaFrame.clearAll()

    def bind(self):
        self.xEntry.bind('<Return>', lambda event: self.add())
        self.addbtn.bind("<Enter>", self.onEnter)
        self.addbtn.bind("<Leave>", self.onLeave)
        self.delbtn.bind("<Enter>", self.onEnter)
        self.delbtn.bind("<Leave>", self.onLeave)
        self.gobtn.bind("<Enter>", self.onEnter)
        self.gobtn.bind("<Leave>", self.onLeave)

    def changeColors(self):
        """ Раскомментровать эту строку, если нужны будут цвета отрезков  """
        self.colors = [Settings.COLOR_DDA, Settings.COLOR_B_FLOAT, Settings.COLOR_B_INT, Settings.COLOR_B_WITHOUT, Settings.COLOR_WU]

    def clear(self):
        self.ax.clear()
        self.canvas.draw()

    def updateGraph(self):
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=190, y=41, relwidth=0.7, relheight=0.75)

    def drawGraph(self, data, xlabels, lenSeg):
        cat_par = xlabels
        width = 0.3
        x = np.arange(len(cat_par))

        if lenSeg:
            bars = self.ax.bar(x, data, width, label=f'lenSeg = {lenSeg}')
        else:
            bars = self.ax.bar(x, data, width)

        for b, c in zip(bars, self.colors):
            b.set_color(c)

        self.ax.set_title('Зависимость количества ступенек от угла наклона')
        self.ax.set_xlabel('Угол')
        self.ax.set_ylabel('Количество ступенек')

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(cat_par)

    def changeGraph(self, data, xLabels, lenSeg):
        if data is None or xLabels is None:
            return

        self.clear()
        self.drawGraph(data, xLabels, lenSeg)
        self.updateGraph()

    def plug(self):
        pass

    def add(self):
        alpha = self.xEntry.get()
        if not Tools.isInt(alpha):
            showinfo('Error', 'Неверно указан угол')
            return
        if self.alphaFrame.isInYet(alpha):
            showinfo('Error', 'Угол уже добавлен')
            return
        self.alphaFrame.addString(alpha)
        self.xEntry.delete(0, END)
        self.xEntry.focus_set()

    def delHighlighted(self):
        self.alphaFrame.delHighlighted()

    def onEnter(self, btn):
        btn.widget['background'] = '#deebf1'

    def onLeave(self, btn):
        btn.widget['background'] = 'SystemButtonFace'

    def go(self):
        x1, y1, x2, y2 = self.segmentForm.getXY()
        if not Tools.isFloat(x1) or not Tools.isFloat(y1) or not Tools.isFloat(x2) or not Tools.isFloat(y2):
            showinfo('Error', 'Неверно введены координаты отрезка')
            return

        alphas = self.alphaFrame.getStrings()
        if len(alphas) == 0:
            showinfo('Error', 'Вы не выбрали значения углов')
            return

        x1, y1, x2, y2 = map(float, (x1, y1, x2, y2))

        alphas.sort(key=lambda i: int(i))

        if self.cleanCanvaFlag:
            self.canva.clear()

        countStepsAr = []
        self.colors = []
        oneColor = random_color()
        for alpha in alphas:

            start = Point(x1, y1)
            end = Point(x2, y2)
            end.rotate(start, int(alpha))

            start_x_canva = self.canva.canva.XShiftPC(start.x)
            end_x_canva = self.canva.canva.XShiftPC(end.x)
            start_y_canva = self.canva.canva.YShiftPC(start.y)
            end_y_canva = self.canva.canva.YShiftPC(end.y)

            countStepsAr.append(countSteps(start_x_canva, start_y_canva, end_x_canva, end_y_canva, self.canva.canva.method))

            print(self.oneColorFlag)
            if self.oneColorFlag:
                self.colors.append(oneColor)
            else:
                self.colors.append(random_color())
            self.canva.canva.addSegment(start.x, start.y, end.x, end.y, self.colors[-1])

        if self.t:
            self.t.place_forget()
            self.t = None

        self.changeGraph(countStepsAr, alphas, str(1))

        self.canva.canva.save()