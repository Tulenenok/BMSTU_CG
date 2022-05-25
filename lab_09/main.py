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

    root.iconphoto(True, PhotoImage(file=r'shared/a4.png'))
    root.title('Лабораторная работа №9')

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

    fg = '#1e1614'
    addSegmentForm = XYForm(root, Settings.COLOR_MAIN_BG, 'Add point', Settings.WIDTH_INPUT,
                       lambda: addPointKey(c, addSegmentForm), '  Add  ', fg=fg)
    delSegmentForm = XYForm(root, Settings.COLOR_MAIN_BG, 'Del point', Settings.WIDTH_INPUT,
                       lambda: delPointKey(c, delSegmentForm), '  Del  ', fg=fg)

    addSegmentForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + 30)
    delSegmentForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + Settings.STEP_INPUT + 30)

    var = IntVar()
    var.set(0)
    Radiobutton(text="Polygon", variable=var, value=0,
                command=lambda: drSeg(c), bg=Settings.COLOR_MAIN_BG).place(
        x=Settings.X_INPUT - 5, y=Settings.Y_INPUT)
    Radiobutton(text="Clipper", variable=var, value=1,
                command=lambda: drClip(c), bg=Settings.COLOR_MAIN_BG).place(
        x=Settings.X_INPUT + 85, y=Settings.Y_INPUT)

    selectMethod(root, c)

    root.mainloop()


def drSeg(c):
    c.canva.drawSegment()
    # c.changeColorRandom()

def drClip(c):
    c.canva.drawClipper()
    # c.changeColorRandom()


if __name__ == "__main__":
    main()

