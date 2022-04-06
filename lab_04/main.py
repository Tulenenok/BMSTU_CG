from controll.controllView import *

from view.RootWithVersions import *
from view.menu import *
from view.CanvasField import *
from view.ActionsField import *
from view.keyInput import *


def hideShow(frameShow, frameHide):
    for f in frameHide:
        f.hide()
    for f in frameShow:
        f.reShow()


def main():
    root = RootWithVersions()
    root.geometry('850x650')
    root['bg'] = Settings.COLOR_MAIN_BG

    root.iconphoto(True, PhotoImage(file=r'shared/rootIcon1.png'))
    root.title('Лабораторная работа №4')

    c = WrapCanva(root, Canva=PolygonField, highlightthickness=0)
    menu = menuFrame(root)
    root.config(menu=menu.create(c, inputPointsFromFile, savePointsToFile, clearCanva, root.loadVersion))
    root.setSaveObjs(c)

    act = ActionsField(root, c)
    act.show(posx=105, posy=300)

    c.show(Settings.X_CANVA, Settings.Y_CANVA, Settings.REL_X_CANVA, Settings.REL_Y_CANVA)

    root.bind("<Control-s>", lambda event: savePointsToFile(c), '+')

    upBtns = UpButtons(root, c)
    upBtns.show()

    addXYForm = XYXForm(root, Settings.COLOR_MAIN_BG, 'Add circle', Settings.WIDTH_INPUT,
                        lambda: controllAddCircle(c, addXYForm), '  Add  ')
    delXYForm = XYXForm(root, Settings.COLOR_MAIN_BG, 'Del circle', Settings.WIDTH_INPUT,
                        lambda: controllDelCircle(c, delXYForm), '  Del  ')

    addXYForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + 30)
    delXYForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + 30 + 45 + Settings.STEP_INPUT)

    addBeam = XYXYForm(root, Settings.COLOR_MAIN_BG, 'Add ellipse', Settings.WIDTH_INPUT, lambda: controllAddEllipse(c, addBeam), '  Add  ', labels=[' X: ', ' Y: ', ' a: ', ' b: '])
    addBeam.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + 30)
    addBeam.hide()

    delBeam = XYXYForm(root, Settings.COLOR_MAIN_BG, 'Del ellipse', Settings.WIDTH_INPUT, lambda: controllDelEllipse(c, delBeam), '   Del   ', labels=[' X: ', ' Y: ', ' a: ', ' b: '])
    delBeam.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + 230)
    delBeam.hide()

    var = IntVar()
    var.set(0)
    Radiobutton(text="Circle", variable=var, value=0, command=lambda: hideShow([addXYForm, delXYForm], [addBeam, delBeam]), bg=Settings.COLOR_MAIN_BG).place(x=Settings.X_INPUT - 5, y=Settings.Y_INPUT)
    Radiobutton(text="Ellipse", variable=var, value=1, command=lambda: hideShow([addBeam, delBeam], [addXYForm, delXYForm]), bg=Settings.COLOR_MAIN_BG).place(x=Settings.X_INPUT + 85, y=Settings.Y_INPUT)

    selectMethod(root, c)

    c.canva.change_min_len_coords()

    root.mainloop()


if __name__ == "__main__":
    main()

