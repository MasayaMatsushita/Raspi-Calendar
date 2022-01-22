# -*- coding: utf-8 -*-
import os
import sys
import random
import tkinter
from PIL import Image, ImageTk

def image_setup(image):
    """
    image_setup
    引数:
    JpegImageFile Class
    戻り値:
    po_x: 画像左上のx座標
    po_y: 画像左上のy座標
    re_w: 画像の横幅(px)
    re_h: 画像の縦幅(px)
    """
    w = image.width # 横幅を取得                                            
    h = image.height # 縦幅を取得
    if int(h * (397/w)) > 477:
        #縦幅が長いときのリサイズ処理
        re_w = int(w * (477/h))
        re_h = int(h * (477/h))
    else:
        #横幅が長いときのリサイズ処理
        re_w = int(w * (397/w))
        re_h = int(h * (397/w))
    #画像配置を中央にする処理
    if re_w == 397:
        po_x = 0
        po_y = int((480 - re_h) / 2)
    else:
        po_x = int((400 - re_w) / 2)
        po_y = 0
    return [po_x, po_y, re_w, re_h]

class Drawer:
    '''画像を表示するクラス'''
    def __init__(self, master):
        self.initSetting(master)

    def initSetting(self, master):
        '''画像表示に必要な設定'''
        self.master = master
        self.path = os.path.dirname(os.path.abspath(__file__)) + '/pic/'
        # self.path = os.path.dirname(os.path.abspath(sys.argv[0])) + '/pic/'
        self.list_dir = os.listdir(self.path)
        self.eshi_name = [f for f in self.list_dir if os.path.isdir(os.path.join(self.path, f))]
        self.eshi_files_name = []
        for dir in self.eshi_name:
            files = os.listdir(self.path+dir+'/')
            eshi_path = self.path+dir+'/'
            files_file = [f for f in files if os.path.isfile(os.path.join(eshi_path, f))]
            self.eshi_files_name.append(files_file)

        #切り替えたい画像を定義
        self.img = []
        self.img_coor = []
        
        for dir_name in range(len(self.eshi_name)):
            tmp_img = []
            tmp_img_coor = []
            for num in range(len(self.eshi_files_name[dir_name])):
                tmp_img_data = Image.open(self.path + '/' + self.eshi_name[dir_name] + '/' + self.eshi_files_name[dir_name][num])
                [pic_x, pic_y, pic_w, pic_h] = image_setup(tmp_img_data)
                tmp_img_coor.append([pic_x, pic_y])
                tmp_img_data = tmp_img_data.resize((pic_w, pic_h))
                tmp_img.append(ImageTk.PhotoImage(tmp_img_data))
            self.img.append(tmp_img)
            self.img_coor.append(tmp_img_coor)

        self.canvas = tkinter.Canvas(bg = "#EEEEE8", width=398, height=478, highlightthickness=0)
        self.canvas.place(x=20, y=2)
        self.eshi_id = 0
        self.image_id = random.randrange(len(self.img[self.eshi_id]))
        self.item = self.canvas.create_image(1, 1, image=self.img[self.eshi_id][self.image_id], anchor=tkinter.NW)

    def update(self):
        self.image_id = random.randrange(len(self.img[self.eshi_id]))
        self.canvas.itemconfig(self.item, image=self.img[self.eshi_id][self.image_id])
        self.canvas.place(x=self.img_coor[self.eshi_id][self.image_id][0], y= self.img_coor[self.eshi_id][self.image_id][1])


class EshiImage:
    
    def __init__(self, master):
        self.master = master
        self.drawer = Drawer(master)

        bg_color = "#EEEEE8"
        font_ui = "Yu Gothic"
        button_eshi_change = tkinter.Button(master, text=" ", font=(font_ui, 10), 
            bg=bg_color,
            borderwidth=0,
            relief='flat' , command=lambda:eshi_change(self))
        button_eshi_change.place(x=415, y=440, width=30, height=30)

        self.master.after(1000 * 60 * 3, self.update)

    def update(self):
        '''画像を更新する'''
        self.drawer.update()
        self.master.after(1000 * 60 * 3, self.update)


def eshi_change(self):
    self.drawer.eshi_id = (self.drawer.eshi_id+1) % len(self.drawer.eshi_name)
    self.drawer.image_id = 0
    self.drawer.update()