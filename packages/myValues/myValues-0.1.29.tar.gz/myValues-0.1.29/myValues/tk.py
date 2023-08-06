from tkinter import *;from tkinter import messagebox,filedialog,ttk
import tkinter,_tkinter
TclError=_tkinter.TclError
window=tkinter.Tk()
def littlewindow():
    return Toplevel()
def show(type="info",args=["系统提示","信息"]):
    result=eval("messagebox.show"+type+"("+args[0]+','+args[1]+")")
    return result
from tkinter.ttk import *
class tkApp(tkinter.Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("我的作品")
    pass
class littleWin(tkinter.Toplevel):
    number=0
    def __init__(self,master=window):
        littleWin.number+=1
        Toplevel.__init__(self,master)
        self.title("第"+str(littleWin.number)+"个小窗口")