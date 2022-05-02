from controll.controllView import *

from view.RootWithVersions import *
from view.menu import *
from view.CanvasField import *
from view.ActionsField import *
from view.keyInput import *


def main():
    root = RootWithVersions()
    root.geometry('850x650')
    root['bg'] = Settings.COLOR_MAIN_BG

    root.iconphoto(True, PhotoImage(file=r'shared/a.png'))
    root.title('Лабораторная работа №6')

    c = WrapCanva(root, Canva=PolygonField, highlightthickness=0)
    menu = menuFrame(root)
    root.config(menu=menu.create(c, inputPointsFromFile, savePointsToFile, clearCanva, root.loadVersion))
    root.setSaveObjs(c)

    act = ActionsField(root, c)
    act.show(posx=105, posy=300)

    c.show(Settings.X_CANVA, Settings.Y_CANVA, Settings.REL_X_CANVA, Settings.REL_Y_CANVA)

    # image = ImageTk.PhotoImage(file=r"C:\projects\Сomputer graphics\lab_02\data\lica.jpg", size=0.5)
    # c.canva.create_image(0, 0, image=image, anchor=NW)

    root.bind("<Control-s>", lambda event: savePointsToFile(c), '+')

    upBtns = UpButtons(root, c)
    upBtns.show()

    addXYForm = XYForm(root, Settings.COLOR_MAIN_BG, 'Add point', Settings.WIDTH_INPUT,
                       lambda: addPointKey(c, addXYForm), '  Add  ')
    delXYForm = XYForm(root, Settings.COLOR_MAIN_BG, 'Del point', Settings.WIDTH_INPUT,
                       lambda: delPointKey(c, delXYForm), '  Del  ')

    addXYForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + 30)
    delXYForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + Settings.STEP_INPUT + 30)

    var = IntVar()
    var.set(0)
    Radiobutton(text="Fill", variable=var, value=0,
                command=lambda: c.canva.drawFill(), bg=Settings.COLOR_MAIN_BG).place(
        x=Settings.X_INPUT - 5, y=Settings.Y_INPUT)
    Radiobutton(text="Cut", variable=var, value=1,
                command=lambda: c.canva.drawCut(), bg=Settings.COLOR_MAIN_BG).place(
        x=Settings.X_INPUT + 85, y=Settings.Y_INPUT)

    selectMethod(root, c)

    root.mainloop()


if __name__ == "__main__":
    main()
#
#
# # from tkinter import *
# # from PIL import ImageTk
# # from view.CanvasField import *
# #
# # root = Tk()
# # root.geometry('850x650')
# # root['bg'] = 'yellow'
# # f = WrapCanva(root, width=200, height=200, highlightthickness=0)
# # f.show(Settings.X_CANVA, Settings.Y_CANVA, Settings.REL_X_CANVA, Settings.REL_Y_CANVA)
# # image = ImageTk.PhotoImage(file = r"C:\projects\Сomputer graphics\lab_02\shared\rootIcon.png")
# # f.canva.create_line(10, 10, 100, 100)
# # f.canva.create_image(10, 10, image = image, anchor = NW)
# # f = Frame(root, width=200, height=200)
# # canvas = CartesianField(root, f, width=200, height=200, bg='blue')
# # canvas.place(x=0, y=0, relwidth=1)
# #
# # image = ImageTk.PhotoImage(file = r"C:\projects\Сomputer graphics\lab_02\shared\rootIcon.png")
# # canvas.create_image(10, 10, image = image, anchor = NW)
# # canvas.create_line(10, 10, 100, 100)
# # f.place(x=0, y=0, relwidth=0.7)
#
# # mainloop()
#
# # Очерк по политической культуре России

# from tkinter import *
# root = Tk()
# screen = Canvas(root)
# screen.pack()
# i=[]
# a=0
# colors = ['#f0f0f0', "green","blue",'black',"white","red","green","blue",'black',"white"]
# for j in colors:
#     a += 10
#     i.append(screen.create_rectangle((10+a, 10+a, 30+a, 30+a), fill=j))
#
# def onmotion(event): # самое интересное
#     x = event.x
#     y = event.y
#     # x = root.winfo_pointerx()-root.winfo_x() # получаем координаты курсора относительно окна
#     # y = root.winfo_pointery()-root.winfo_y() #
#     a = screen.find_overlapping(x+0.5,y-0.5,x+0.5,y+0.5)
#     print(a, x, y)                 # выводим, какую фигуру(-ы) накрывает квадрат 1х1 пиксель
#     print(screen.itemcget([a[-1]], "fill" ) ) # выводим цвет самой верхней фигуры
#
# screen.bind("<Button-1>",onmotion) #привязываем к клику лкм функцию
#
# root.mainloop() # запускаемся