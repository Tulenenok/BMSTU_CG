from tkinter import *
from tkinter import ttk
import platform


class ScrollFrame(Frame):
    def __init__(self, parent, width=120):
        super().__init__(parent)

        self.canvas = Canvas(self, borderwidth=0, background="white", width=133)
        self.viewPort = Frame(self.canvas,
                                 background="#ffffff")
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",
                                                       tags="self.viewPort")

        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)
        self.canvas.bind("<Configure>",
                         self.onCanvasConfigure)

        self.viewPort.bind('<Enter>', self.onEnter)
        self.viewPort.bind('<Leave>', self.onLeave)

        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window,
                               width=canvas_width)

    def onMouseWheel(self, event):
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def onEnter(self, event):
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")


class Check(Frame):
    def __init__(self, root, choises, width=120):
        Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self, root)
        self.bg = self.cget("background")

        self.vars = []                      # массив с элементами типа String
        self.strings = choises              # массив с названиями (обычные строки)
        self.checkBtns = []                 # массив с элементами типа Checkbutton

        self.countStr = 0

        self.scrollFrame.pack(side="top", fill="both", expand=True)

    def addString(self, string):
        self.strings.append(string)
        var = StringVar(value=string)
        self.vars.append(var)
        # anchor="w",  background=self.bg,relief="flat", highlightthickness=0
        cb = ttk.Checkbutton(self.scrollFrame.viewPort, var=var, text=string,
                         onvalue=string, offvalue="",
                         width=20, variable=""
                         )
        cb.grid(row=self.countStr, column=0)
        self.checkBtns.append(cb)
        self.countStr += 1

    def clearAll(self):
        for btn in self.checkBtns:
            btn.grid_forget()
        self.checkBtns.clear()
        self.vars.clear()
        self.strings.clear()

    def getCheckedItems(self):
        values = []
        for i, var in enumerate(self.vars):
            value = var.get()
            if 'selected' in self.checkBtns[i].state():
                values.append(value)
        return values

    def isInYet(self, value):
        for i in self.strings:
            if i == value:
                return True
        return False

    def delHighlighted(self):
        delnames = self.getCheckedItems()
        newNames = [i for i in self.strings if i not in delnames]
        self.clearAll()
        for i in newNames:
            self.addString(i)

    def getStrings(self):
        return self.strings.copy()