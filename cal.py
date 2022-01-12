import os
import math
import tkinter as tk 
from PIL import Image, ImageTk
import datetime as dt 
import calendar as cl 

m2 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 

def generate_calendar1(y1, m1): 
    global wd 
    global cal 
    for i1 in range( len(cal) ): 
        cal[i1] = ""
    date1 = dt.date( y1, m1, 1 ) 
    wd = date1.weekday() 
    if wd > 5: 
        wd = wd - 7 
    cal_max1 = cl.monthrange( y1, m1 )[1] 
    for i1 in range( cal_max1 ): 
        str1 = str( i1+1 ) 
        i2 = i1 + wd + 1 
        cal[i2] = str1 

def set_calendar1(cal, btn1): 
    for i1 in range( len(cal) ): 
        str1 = cal[i1] 
        btn1[i1]["text"] = str1 

def prev_next1( n1 ): 
    global y1 
    global m1 
    global btn1 
    m1 = m1 + n1 
    if m1 > 12: 
        y1 = y1 + 1 
        m1 = 1 
    elif m1 < 1: 
        y1 = y1 - 1 
        m1 = 12 
    label1["text"] = str(m1) 
    label2["text"] = m2[m1-1] 
    label3["text"] = str(y1) 
    generate_calendar1(y1, m1) 
    set_calendar1(cal, btn1)
    for i1 in range( len(cal) ):
        if btn1[i1]["text"] == str(now1.day) and y1 == now1.year and m1 == now1.month:
            btn1[i1]["relief"] = 'solid'
            btn1[i1]['borderwidth'] = 1
            break
        else:
            btn1[i1]["relief"] = 'flat'

def home():
    m1 = now1.month
    y1 = now1.year
    label1["text"] = str(m1) 
    label2["text"] = m2[m1-1] 
    label3["text"] = str(y1) 
    generate_calendar1(y1, m1) 
    set_calendar1(cal, btn1)
    for i1 in range( len(cal) ):
        if btn1[i1]["text"] == str(now1.day):
            btn1[i1]["relief"] = 'solid'
            break


def quit():
    root.destroy()

def btn_click1():
    return

def picture_setup(image):
    """
    picture_info
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

"""
アナログ時計関数
"""

#時計サイズの設定
CLOCK_SIZE = 120
CLOCK_WIDTH = CLOCK_SIZE 
CLOCK_HEIGHT = CLOCK_SIZE
#時計の配置
CLOCK_X = 500
CLOCK_Y = 3
#針の長さの設定
LENGTH_HOUR_HAND = CLOCK_SIZE / 2 * 0.6
LENGTH_MINUTE_HAND = CLOCK_SIZE / 2 * 0.7
LENGTH_SECOND_HAND = CLOCK_SIZE / 2 * 0.8
#針の色の設定
COLOR_HOUR_HAND = "red"
COLOR_MINUTE_HAND = "blue"
COLOR_SECOND_HAND = "green"
#針の太さの設定
WIDTH_HOUR_HAND = 3
WIDTH_MINUTE_HAND = 2
WIDTH_SECOND_HAND = 1
#時計の前面と背景の色の設定
BG_COLOR = "white"
FG_COLOR = "gray"
#時計の盤面を表す円の半径の設定
CLOCK_OVAL_RADIUS = CLOCK_SIZE / 2
#時計の数字の位置の設定（中心からの距離）
DISTANCE_NUMBER = CLOCK_SIZE / 2 * 0.9

class Timer:
    """
    時刻を取得するクラス
    """
    def __init__(self):
        # タイムゾーンの設定
        self.JST = dt.timezone(dt.timedelta(hours=9))
    def time(self):
        # 時刻の取得
        now = dt.datetime.now(tz=self.JST)
        # 時・分・秒にわけて返却
        return now.hour, now.minute, now.second

class Drawer:
    """
    時計を描画するクラス
    """
    def __init__(self, master):
        # 各種設定を行なった後に時計の盤面を描画
        self.initSetting(master)
        self.createClock()
    def initSetting(self, master):
        """
        時計描画に必要な設定を行う
        """
        # ウィジェットの作成先を設定
        self.master = master
        # 描画した針のオブジェクトを覚えておくリストを用意
        self.hands = []
        # 針の色のリストを用意
        self.colors = [
            COLOR_HOUR_HAND, COLOR_MINUTE_HAND, COLOR_SECOND_HAND
        ]
        # 針の太さのリストを用意
        self.widths = [
            WIDTH_HOUR_HAND, WIDTH_MINUTE_HAND, WIDTH_SECOND_HAND
        ]
        # 針の長さのリストを用意
        self.lengths = [
            LENGTH_HOUR_HAND, LENGTH_MINUTE_HAND, LENGTH_SECOND_HAND
        ]
        # キャンバスの中心座標を覚えておく
        self.center_x = CLOCK_WIDTH / 2
        self.center_y = CLOCK_HEIGHT / 2

    def createClock(self):
        '''時計の盤面を作成する'''
        # キャンバスを作成して配置する
        self.canvas = tk.Canvas(
            self.master,
            width=CLOCK_WIDTH,
            height=CLOCK_HEIGHT,
            background=bg_color,
            highlightthickness=0
        )

        self.canvas.pack(anchor=tk.NE, padx=75, pady=3, ipadx=2, ipady=2)

        # 時計の盤面を表す円を描画する
        x1 = self.center_x - CLOCK_OVAL_RADIUS
        y1 = self.center_y - CLOCK_OVAL_RADIUS
        x2 = self.center_x + CLOCK_OVAL_RADIUS
        y2 = self.center_y + CLOCK_OVAL_RADIUS

        self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=BG_COLOR,
            width=2,
            outline=FG_COLOR
        )

        # 時計の盤面上に数字を描画する
        for hour in range(1, 13):
            # 角度を計算
            angle = hour * 360 / 12 - 90
            # 描画位置を計算
            x1 = self.center_x
            y1 = self.center_x
            dx = DISTANCE_NUMBER * math.cos(math.radians(angle))
            dy = DISTANCE_NUMBER * math.sin(math.radians(angle))
            x2 = x1 + dx
            y2 = y1 + dy
            self.canvas.create_text(
                x2, y2,
                font=("", 10),
                fill=FG_COLOR,
                text=str(hour)
            )

    def drawHands(self, hour, minute, second):
            """
            針を表現する線を描画する
            """
            # 各線の傾きの角度を計算指定リストに追加
            angles = []
            angles.append(hour * 360 / 12 - 90)
            angles.append(minute * 360 / 60 - 90)
            angles.append(second * 360 / 60 - 90)
            # 線の一方の座標をキャンバスの中心とする
            x1 = self.center_x
            y1 = self.center_y
            # initSettingで作成したリストから情報を取得しながら線を描画
            for angle, length, width, color in zip(angles, self.lengths, self.widths, self.colors):
                # 線の他方の座標を計算
                x2 = x1 + length * math.cos(math.radians(angle))
                y2 = y1 + length * math.sin(math.radians(angle))
                hand = self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color,
                    width=width
                )
                # 描画した線のIDを覚えておく
                self.hands.append(hand)
        
    def updateHands(self, hour, minute, second):
        """
        針を表現する線の位置を更新する
        """
        angles = []
        angles.append(hour * 360 / 12 - 90)
        angles.append(minute * 360 / 60 - 90)
        angles.append(second * 360 / 60 - 90)
        # 線の一方の点の座標は常に時計の中心
        x1 = self.center_x
        y1 = self.center_y
        # handは描画した線のID
        for hand, angle, length in zip(self.hands, angles, self.lengths):
            # 線の他方の点の座標は毎回時刻に合わせて計算する
            x2 = x1 + length * math.cos(math.radians(angle))
            y2 = y1 + length * math.sin(math.radians(angle))
            # coordsメソッドにより描画済みの線の座標を変更する
            hand = self.canvas.coords(
                hand,
                x1, y1, x2, y2
            )

class AnalogClock:
    """
    アナログ時計を実現するクラス
    """
    def __init__(self, master):
        # after実行用にウィジェットのインスタンスを保持
        self.master = master
        # 各種クラスのオブジェクトを生成
        self.timer = Timer()
        self.drawer = Drawer(master)
        # 針を描画
        self.draw()
        # １秒後に針を進めるループを開始
        self.master.after(1000, self.update)
    def draw(self):
        '''時計の針を描画する'''
        # 時刻を取得し、その時刻に合わせて針を描画する
        hour, minute, second = self.timer.time()
        self.drawer.drawHands(hour, minute, second)
    def update(self):
        '''時計の針を進める'''
        # 時刻を取得し、その時刻に合わせて針を進める
        hour, minute, second = self.timer.time()
        self.drawer.updateHands(hour, minute, second)
        # １秒後に再度時計の針を進める
        self.master.after(1000, self.update)

"""
Main Code
"""
root = tk.Tk()
root.title(u"lune_calendar v0.2")
root.geometry("800x480+0+0")
bg_color = "#EEEEE8"
root["bg"] = bg_color
font_ui = "Yu Gothic"

if root.winfo_screenwidth() < 800 and root.winfo_screenheight() < 480:
    root.attributes('-fullscreen', True)
else:
    root.resizable(width=False, height=False)
    
"""
画像表示
"""
image = Image.open(os.path.dirname(__file__)+"/mayo1.jpg")
[pic_x, pic_y, pic_w, pic_h] = picture_setup(image)
image = image.resize((pic_w, pic_h))
canvas = tk.Canvas(bg="white", width=pic_w, height=pic_h)
pic = ImageTk.PhotoImage(image, master=root)
canvas.place(x=pic_x, y=pic_y)
canvas.create_image(0, 0, image=pic, anchor=tk.NW)


"""
カレンダー表示
"""
now1 = dt.datetime.now() 
y1 = now1.year 
m1 = now1.month 
d1 = now1.day 
wd = 0
cal = [""]*40 


label1 = tk.Label(font=(font_ui, 26),anchor=tk.CENTER, width=2)
label1["bg"] = bg_color
label1.place(x=425, y=78) 

label2 = tk.Label(font=(font_ui, 10),anchor=tk.W, width=10)
label2["bg"] = bg_color 
label2.place(x=495, y=83) 

label3 = tk.Label(font=(font_ui, 12),anchor=tk.W, width=10)
label3["bg"] = bg_color 
label3.place(x=495, y=105) 

label4 = [""]*7 
a1 = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" ] 
for i1 in range( 7 ): 
    label4[i1] = tk.Label(text=a1[i1], font=(font_ui, 8), anchor=tk.CENTER, width=10)
    label4[i1]["bg"] = bg_color
    label4[i1].place(x=405+47*i1, y=130) 

btn1 = [""]*42 
for i1 in range( 6 ): 
    for i2 in range( 7 ): 
        fg1 = "#000000" 
        if i2 == 0: 
            bg1 = "#FFF0F0" 
            fg1 = "#FF0000" 
        elif i2 == 6: 
            bg1 = "#F6F0FF" 
            fg1 = "#0000A0" 
        else: 
            bg1 = "#FFFFFF"  
        btn1[i2+7*i1] = tk.Button(root, font=(font_ui, 10), anchor=tk.NW, bg=bg1, fg=fg1, relief='flat', command=btn_click1) 
        x2 = 415 + 47 * i2 
        y2 = 150 + 47 * i1 
        btn1[i2+7*i1].place(x=x2, y=y2, width=45, height=45)

btn2 = tk.Button(root, text="prev", font=(font_ui, 10), bg="#D0D0D0", relief='flat', command=lambda:prev_next1(-1) )
btn2.place(x=530, y=440, width=60, height=30)

btn3 = tk.Button(root, text="next", font=(font_ui, 10), bg="#D0D0D0", relief='flat', command=lambda:prev_next1(1) )
btn3.place(x=690, y=440, width=60, height=30)

btn4 = tk.Button(root, text="home", font=(font_ui, 10), bg="#D0D0D0", relief='flat', command=lambda:home() )
btn4.place(x=610, y=440, width=60, height=30)

btn5 = tk.Button(root, text=" ", font=(font_ui, 10), 
    #bg=bg_color,borderwidth=1,
    relief='flat' , command=lambda:quit() )
btn5.place(x=750, y=5, width=30, height=30)


prev_next1( 0 ) 

"""
アナログ時計表示
"""
AnalogClock(root)

root.mainloop()