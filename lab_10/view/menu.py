from tkinter import *
from tkinter.messagebox import *


class menuFrame:
    def __init__(self, window):
        self.menu = Menu()
        self.window = window
        self.name = '✔ Комментарии'
        self.gridName = '✔ Оси координат'
        self.settingMenu = None

        self.sp = ''

    def __makeDropDown(self, dictLabels):
        newItem = Menu(self.menu, tearoff=0)
        for item in dictLabels:
            newItem.add_command(label=item, command=dictLabels[item])
        return newItem

    def create(self, field, funcInput, funcLoad, funcClean, funcReturn):
        self.field = field

        self.settingMenu = Menu(self.menu, tearoff=0)

        submenu = Menu(self.settingMenu, tearoff=False)
        submenu.add_command(label="Многоугольник", command=field.changeColorNewPol)
        submenu.add_command(label="Отсекатель", command=field.changeColorDelObl)
        submenu.add_command(label="Результат", command=field.changeColorDel)

        self.settingMenu.add_command(label=self.name, command=self.__showComment)
        self.settingMenu.add_command(label=self.gridName, command=self.__showGrid)
        # self.settingMenu.add_cascade(label="Изменить цвет", menu=submenu)

        self.menu.add_cascade(label='File', menu=self.__makeDropDown({
                                                                      'Отменить ⏎': lambda: funcReturn(),
                                                                      'Очистить 🗑': lambda: funcClean(field),
                                                                      }))
        self.menu.add_cascade(label='Setting', menu=self.settingMenu)
        self.menu.add_cascade(label='Info', menu=self.__makeDropDown({'Информация о программе': self.__info_programm,
                                                                      'Информация об авторе': self.__info_author
                                                                      }))
        self.menu.add_cascade(label='Exit', menu=self.__makeDropDown({'Выход': self.window.destroy}))
        return self.menu

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
        showinfo('Info', 'Программа была создана 25.05 в 3:12 (но это не точно)\nАлгоритм Сазерленда Ходжмена.\n\n'
                         'Краткая справка: чтобы замкнуть отсекатель пригодится ctrl+space')