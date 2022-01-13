import os
import tkinter
from PIL import Image, ImageTk
import threading
import time
import datetime as dt

import func

path = os.path.dirname(__file__) + '/pic/'
files = os.listdir(path)
files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]

def show_image():
    #外から触れるようにグローバル変数で定義
    global item, canvas
    global monitor_month_num, monitor_month_str, monitor_year_str, cal_cell

    root = tkinter.Tk()
    root.title('lune_calender v0.4')
    root.geometry("800x480")
    root['background'] = '#EEEEE8'

    if root.winfo_screenwidth() < 1080 and root.winfo_screenheight() < 720:
        root.attributes('-fullscreen', True)
    else:
        root.resizable(width=False, height=False)
    
    canvas = tkinter.Canvas(bg = "#EEEEE8", width=398, height=478, highlightthickness=0)
    canvas.place(x=20, y=2)
    item = canvas.create_image(1, 1, image=img, anchor=tkinter.NW)
    [monitor_month_num, monitor_month_str, monitor_year_str, cal_cell] = func.cal_setup(root)
    
    root.mainloop()


#スレッドを立ててtkinterの画像表示を開始する
thread1 = threading.Thread(target=show_image)
thread1.start()

img = []
img_coor = []
#切り替えたい画像を定義
for num in range(len(files_file)):
    img_data = Image.open(path + files_file[num])
    [pic_x, pic_y, pic_w, pic_h] = func.picture_setup(img_data)
    img_coor.append([pic_x, pic_y])
    img_data = img_data.resize((pic_w, pic_h))
    img.append(ImageTk.PhotoImage(img_data))

#繰り返し処理
img_num = 0
update_time = 0
before_time = dt.datetime.now()
while True:
    time.sleep(1)
    if update_time % 10 == 0:
        canvas.itemconfig(item, image=img[img_num])
        canvas.place(x=img_coor[img_num][0], y= img_coor[img_num][1])
        img_num = (img_num+1) % len(files_file)
        update_time = 0
    update_time += 1
    if before_time.day != dt.datetime.now().day: #フラグ処理にするともっとスマートTODO 
        func.home(monitor_month_num, monitor_month_str, monitor_year_str, cal_cell)
    before_time = dt.datetime.now()
    