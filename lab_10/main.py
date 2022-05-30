from controll.controllView import *

from view.RootWithVersions import *
from view.menu import *
from view.CanvasField import *
from view.ActionsField import *
from view.keyInput import *
from model.hor_alg import *


def main():
    root = RootWithVersions()
    root.geometry('850x650')
    root['bg'] = Settings.COLOR_MAIN_BG

    root.iconphoto(True, PhotoImage(file=r'shared/a5.png'))
    root.title('Лабораторная работа №10')

    c = WrapCanva(root, Canva=PolygonField, highlightthickness=0)
    c.canva.changeLimits(-10, 10, -10, 10, True)
    menu = menuFrame(root)
    root.config(menu=menu.create(c, inputPointsFromFile, savePointsToFile, clearCanva, root.loadVersion))
    root.setSaveObjs(c)

    act = ActionsField(root, c)
    act.show(posx=105, posy=300)

    c.show(Settings.X_CANVA, Settings.Y_CANVA, Settings.REL_X_CANVA, Settings.REL_Y_CANVA)

    root.bind("<Control-s>", lambda event: savePointsToFile(c), '+')

    upBtns = UpButtons(root, c)
    upBtns.show()

    fg = '#154e79'
    XLimitsForm = XYXForm(root, Settings.COLOR_MAIN_BG, 'Limits X', Settings.WIDTH_INPUT - 1,
                          lambda: checkLimits(XLimitsForm), '  Save  ', fg=fg, showButton=False)

    XLimitsForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + 2)

    XLimitsForm.insertXY(-10, 10, 0.2)

    ZLimitsForm = XYXForm(root, Settings.COLOR_MAIN_BG, 'Limits Z', Settings.WIDTH_INPUT - 1,
                          lambda: checkLimits(ZLimitsForm), '  Save  ', fg=fg, showButton=False)

    w1 = 150
    ZLimitsForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + w1)

    ZLimitsForm.insertXY(-5, 5, 0.2)

    # rotateForm = XYXBtnForm(root, Settings.COLOR_MAIN_BG, 'Rotate', Settings.WIDTH_INPUT - 10,
    #                       lambda: checkLimits(ZLimitsForm), '  Go  ', fg=fg, showButton=True, fields=["OX:    ", "OY:    ", "OZ:    "])
    #
    # rotateForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + 155 * 2)
    # rotateForm.insertXY(0, 0, 0)

    XRotateForm = XForm(root, Settings.COLOR_MAIN_BG, 'Rotate', Settings.WIDTH_INPUT - 1,
                          lambda: c.canva.rotate(XRotateForm, "x"), '  Go  ', fg=fg, showButton=True, fields="OX:    ")
    YRotateForm = XForm(root, Settings.COLOR_MAIN_BG, 'Rotate', Settings.WIDTH_INPUT - 1,
                        lambda: c.canva.rotate(YRotateForm, "y"), '  Go  ', fg=fg, showButton=True,
                        fields="OY:    ")
    ZRotateForm = XForm(root, Settings.COLOR_MAIN_BG, 'Rotate', Settings.WIDTH_INPUT - 1,
                        lambda: c.canva.rotate(ZRotateForm, "z"), '  Go  ', fg=fg, showButton=True,
                        fields="OZ:    ")

    XRotateForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + w1 * 2)
    XRotateForm.insertXY(30)

    w = 100

    YRotateForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + w1 * 2 + w)
    YRotateForm.insertXY(30)

    ZRotateForm.show(Settings.COLOR_MAIN_BG, Settings.X_INPUT, Settings.Y_INPUT + w1 * 2 + w * 2)
    ZRotateForm.insertXY(30)




    cb = ttk.Combobox(root, values=[c.canva.saveFunc[0]], font=("Arial", 10),
                      postcommand=lambda: cb.configure(values=c.canva.saveFunc))
    root.option_add('*TCombobox*Listbox.font', ("Arial", 10))
    cb.place(relx=0.742, y=Settings.Y_INPUT + 34)
    cb.current(0)

    c.canva.funcKey = cb
    c.canva.XKey = XLimitsForm
    c.canva.ZKey = ZLimitsForm

    # root.bind("<Return>", goCut(root, c))

    globalParam.canva = c.canva

    root.mainloop()


if __name__ == "__main__":
    main()



