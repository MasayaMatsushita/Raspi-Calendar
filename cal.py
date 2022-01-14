import os
import tkinter
from PIL import Image, ImageTk
import threading
import time
import datetime as dt

import func
import analog_clock

path = os.path.dirname(__file__) + '/pic/'
list_dir = os.listdir(path)
eshi_name = [f for f in list_dir if os.path.isdir(os.path.join(path, f))]
eshi_files_name = []
for dir in eshi_name:
    files = os.listdir(path+dir+'/')
    eshi_path = path+dir+'/'
    files_file = [f for f in files if os.path.isfile(os.path.join(eshi_path, f))]
    eshi_files_name.append(files_file)

def show_image():
    #外から触れるようにグローバル変数で定義
    global item, canvas
    global monitor_month_num, monitor_month_str, monitor_year_str, cal_cell

    root = tkinter.Tk()
    root.title('lune_calender v1.1')
    root.geometry("800x480")
    root['background'] = '#EEEEE8'

    if root.winfo_screenwidth() < 1080 and root.winfo_screenheight() < 720:
        root.attributes('-fullscreen', True)
    else:
        root.resizable(width=False, height=False)
    
    canvas = tkinter.Canvas(bg = "#EEEEE8", width=398, height=478, highlightthickness=0)
    canvas.place(x=20, y=2)
    item = canvas.create_image(1, 1, image=img, anchor=tkinter.NW)
    func.eshi_dir_set(eshi_files_name)
    [monitor_month_num, monitor_month_str, monitor_year_str, cal_cell] = func.cal_setup(root)
    analog_clock.analog_clock_setup(root)
    
    root.mainloop()

#スレッドを立ててtkinterの画像表示を開始する
thread1 = threading.Thread(target=show_image)
thread1.start()

img = []
img_coor = []
#切り替えたい画像を定義
for dir_name in range(len(eshi_name)):
    tmp_img = []
    tmp_img_coor = []
    for num in range(len(eshi_files_name[dir_name])):
        tmp_img_data = Image.open(path + '/' + eshi_name[dir_name] + '/' + eshi_files_name[dir_name][num])
        [pic_x, pic_y, pic_w, pic_h] = func.picture_setup(tmp_img_data)
        tmp_img_coor.append([pic_x, pic_y])
        tmp_img_data = tmp_img_data.resize((pic_w, pic_h))
        tmp_img.append(ImageTk.PhotoImage(tmp_img_data))
    img.append(tmp_img)
    img_coor.append(tmp_img_coor)



#繰り返し処理
img_num = 0
update_time = 0
before_time = dt.datetime.now()
before_eshi_dir_id = func.eshi_dir_id
while True:
    time.sleep(1)
    eshi_dir_id = func.eshi_dir_id
    if before_eshi_dir_id != eshi_dir_id:
        img_num = 0
        update_time = 0

    if len(eshi_name) != 0: 
        if update_time % (60 * 5) == 0:
            canvas.itemconfig(item, image=img[eshi_dir_id][img_num])
            canvas.place(x=img_coor[eshi_dir_id][img_num][0], y= img_coor[eshi_dir_id][img_num][1])
            img_num = (img_num+1) % len(img_coor[eshi_dir_id])
            update_time = 0
        update_time += 1

    if before_time.day != dt.datetime.now().day: #フラグ処理にするともっとスマートTODO 
        func.home(monitor_month_num, monitor_month_str, monitor_year_str, cal_cell)
    before_eshi_dir_id = eshi_dir_id
    before_time = dt.datetime.now()
    
    