""" ЭТО В ИТОГЕ НЕ ПРИГОДИЛОСЬ В ЛАБЕ, НО ТЕРЯТЬ ИНФУ НЕ ХОЧЕТСЯ """
""" здесь можно нарисовать гистограмму + таблицу на доп окне"""



from tkinter import *
from view.Settings import Settings
from view.Btn import WrapButton

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import random

class Analysis:
    def __init__(self, root, canva):
        self.root = root
        self.canva = canva

        self.z = Tk()
        self.z.geometry('650x500')
        self.z.title('А давайте построим гистограммы')
        self.z['bg'] = Settings.COLOR_MAIN_BG
        # self.z.resizable(0, 0)
        self.colors = plt.cm.BuPu(np.linspace(0.6, 1, 5))
        self.rows = ('DDA', 'B [float]', 'B [int]', 'B', 'WU')

        self.btnScale = WrapButton(self.z, txt='Scaling', padx=20, pady=3, command=lambda: self.plug(),
                                   font=('Arial', 10, 'bold'))

        self.btnScale.btn.place(x=10, y=60)

        self.fig = Figure(figsize=(5, 4), dpi=85)
        self.ax = self.fig.add_subplot(111)

        self.drawGraph()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.z)
        # self.updateGraph()

        self.headLabel = None

    def changeColors(self):
        """ Раскомментровать эту строку, если нужны будут цвета отрезков  """
        self.colors = [Settings.COLOR_DDA, Settings.COLOR_B_FLOAT, Settings.COLOR_B_INT, Settings.COLOR_B_WITHOUT, Settings.COLOR_WU]

    def clear(self):
        self.ax.clear()

    def updateGraph(self):
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=160, y=40, relwidth=0.7, relheight=0.8)

    def drawGraph(self):
        data = [[66386, 174296, 75131, 577908, 32015],
                [58230, 381139, 78045, 99308, 160454],
                [89135, 80552, 152558, 497981, 603535],
                [78415, 81858, 150656, 193263, 69638],
                [139361, 331509, 343164, 781380, 52269]]

        columns = ('α° = 0', 'α° = 0', 'α° = 0', 'α° = 0', 'α° = 0')

        n_rows = len(data)
        index = np.arange(len(columns)) + 0.3
        bar_width = 0.4                           # толщина одного столбца

        y_offset = np.zeros(len(columns))

        cell_text = []
        for row in range(n_rows):
            self.ax.bar(index, data[row], bar_width, bottom=y_offset, color=self.colors[row])
            y_offset = y_offset + data[row]
            cell_text.append(['%1.1f' % (x / 1000.0) for x in y_offset])

        colors = self.colors[::-1]
        cell_text.reverse()

        the_table = self.ax.table(cellText=cell_text,
                                  rowLabels=self.rows,
                                  rowColours=colors,
                                  colLabels=columns, loc='bottom', cellLoc='center')
        the_table.set_fontsize(9)

        self.fig.subplots_adjust(left=0.2, bottom=0.3)
        self.ax.set_ylabel("Количество ступенек")
        self.ax.set_xticklabels([])

    def plug(self):
        self.clear()
        self.drawGraph()
        self.updateGraph()
