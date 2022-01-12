import os
import tkinter
from PIL import Image, ImageTk
import threading
import time

path = os.path.dirname(__file__) + '/pic/'
files = os.listdir(path)
files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]

def show_image():
    #外から触れるようにグローバル変数で定義
    global item, canvas
 
    root = tkinter.Tk()
    root.title('test')
    root.geometry("800x480")
    root['background'] = 'white'
    canvas = tkinter.Canvas(bg = "white", width=800, height=480, highlightthickness=0)
    canvas.place(x=20, y=2)
    item = canvas.create_image(0, 0, image=img, anchor=tkinter.NW)
    root.mainloop()
 
#スレッドを立ててtkinterの画像表示を開始する
thread1 = threading.Thread(target=show_image)
thread1.start()

img = []
#切り替えたい画像を定義
for num in range(len(files_file)):
    img_data = Image.open(path + files_file[num])
    img.append(ImageTk.PhotoImage(img_data))

img_num = 0
while True:
    canvas.itemconfig(item, image=img[img_num])
    time.sleep(3)
    img_num = (img_num+1) % len(files_file)