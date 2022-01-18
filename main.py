# -*- coding: uTf-8 -*-
import tkinter

import my_calendar
import eshi_image
import analog_clock

root = tkinter.Tk()
root.title('lune_calender v1.2')
root.geometry("800x480")
root['background'] = '#EEEEE8'

if root.winfo_screenwidth() < 1080 and root.winfo_screenheight() < 720:
    root.attributes('-fullscreen', True)
else:
    root.resizable(width=False, height=False)

eshi_image.EshiImage(root)
analog_clock.analog_clock_setup(root)
my_calendar.cal_setup(root)


bg_color = "#EEEEE8"
font_ui = "Yu Gothic"

button_quit = tkinter.Button(root, text=" ", font=(font_ui, 10), 
    bg=bg_color,
    borderwidth=0,
    relief='flat' , command=lambda:quit(root) )
button_quit.place(x=750, y=5, width=30, height=30)

def quit(root):
    root.quit()

root.mainloop()