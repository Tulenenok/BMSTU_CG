from tkinter import *
from tkinter.messagebox import *
from tkinter.colorchooser import askcolor
from model.Tools import *
from view.Settings import *


class menuFrame:
    def __init__(self, window):
        self.menu = Menu()
        self.window = window
        self.name = '✔ Комментарии'
        self.gridName = '✔ Оси координат'
        self.settingMenu = None

        self.sp = 'Горячие клавиши:\n\n' \
                  '  - Cntrl-Space -- начать новую фигуру, замкнув старую\n' \
                  '  - Cntrl-Shift-Space -- начать новую, не замыкая старую\n' \
                  '  - Cntrl-plus -- масштабирование х2\n' \
                  '  - Cntrl-minus -- масштабирование х0.5\n' \
                  '  - Cntrl-p -- поворот по часовой стрелке на 15 градусов\n' \
                  '  - Cntrl-o -- поворот против часовой стрелки на 15 градусов'

    def __makeDropDown(self, dictLabels):
        newItem = Menu(self.menu, tearoff=0)
        for item in dictLabels:
            newItem.add_command(label=item, command=dictLabels[item])
        return newItem

    def create(self, field, funcInput, funcLoad, funcClean, funcReturn):
        self.field = field
        self.settingMenu = Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label='File', menu=self.__makeDropDown({'Отменить ⏎': lambda: funcReturn(),
                                                                      'Очистить 🗑': lambda: funcClean(field),
                                                                      }))

        # self.menu.add_cascade(label='File', menu=self.__makeDropDown({'Открыть 📂': lambda: funcInput(field),
        #                                                               'Сохранить 📋': lambda: funcLoad(field),
        #                                                               'Отменить ⏎': lambda: funcReturn(),
        #                                                               'Очистить 🗑': lambda: funcClean(field),
        #                                                               }))
        self.menu.add_cascade(label='Setting', menu=self.settingMenu)
        self.menu.add_cascade(label='Info', menu=self.__makeDropDown({'Информация о программе': self.__info_programm,
                                                                      'Информация об авторе': self.__info_author,
                                                                      }))
        # 'Справка': lambda : showinfo('Info', self.sp)
        self.menu.add_cascade(label='Exit', menu=self.__makeDropDown({'Выход': self.window.destroy}))

        submenu = Menu(self.settingMenu, tearoff=False)
        submenu.add_command(label="Каноническое", command=lambda: self.plug(Tools.M_CANONICAL))
        submenu.add_command(label="Параметрическое", command=lambda: self.plug(Tools.M_PARAMETRIC))
        submenu.add_command(label="Брезенхэм", command=lambda: self.plug(Tools.M_BREZENHAM))
        submenu.add_command(label="Средняя точка", command=lambda: self.plug(Tools.M_MIDDLE_POINT))
        submenu.add_command(label="Библиотека", command=lambda: self.plug(Tools.M_USUAL))

        self.settingMenu.add_command(label=self.name, command=lambda: self.__showComment())
        self.settingMenu.add_command(label=self.gridName, command=lambda: self.__showGrid())
        self.settingMenu.add_cascade(label='Изменить цвета', menu=submenu)

        return self.menu


    def plug(self, event):
        color = askcolor()[1]
        if not color:
            return

        if event == Tools.M_CANONICAL:
            Settings.COLOR_CANONICAL = color
        elif event == Tools.M_PARAMETRIC:
            Settings.COLOR_PARAMETRIC = color
        elif event == Tools.M_BREZENHAM:
            Settings.COLOR_B = color
        elif event == Tools.M_MIDDLE_POINT:
            Settings.COLOR_MIDDLE_POINT = color
        elif event == Tools.M_USUAL:
            Settings.COLOR_USUAL = color
        else:
            print('Неверный метод')


        Settings.M_COLORS = (Settings.COLOR_CANONICAL, Settings.COLOR_PARAMETRIC, Settings.COLOR_B,
                             Settings.COLOR_MIDDLE_POINT, Settings.COLOR_WU, Settings.COLOR_USUAL)

        if self.field.canva.method == event:
            self.field.canva.colorNowPol = color

    def __showComment(self):
        self.field.radioShowComments()
        self.name = '✔ Комментарии' if self.name == '❌ Комментарии' else '❌ Комментарии'
        self.settingMenu.entryconfig(0, label=self.name)

    def __showGrid(self):
        self.field.canva.flagShowGrid(not self.field.canva.showArrows)
        self.gridName = '✔ Оси координат' if self.gridName == '❌ Оси координат' else '❌ Оси координат'
        self.settingMenu.entryconfig(1, label=self.gridName)


    def __info_author(self):
        showinfo('Info', 'Автор: Гурова Наталия ИУ7-44Б')

    def __info_programm(self):
        showinfo('Info', 'Задание:\n\nРеализовать различные алгоритмы построения окружностей и эллипсов. \n'
                         '  - Каноническое уравнение\n'
                         '  - Параметрическое уравнение\n'
                         '  - Брезенхем\n'
                         '  - Метод средней точки\n')