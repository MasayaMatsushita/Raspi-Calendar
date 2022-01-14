
import datetime as dt
import math
import tkinter

"""
変数定義
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
        self.canvas = tkinter.Canvas(
            self.master,
            width=CLOCK_WIDTH,
            height=CLOCK_HEIGHT,
            background="#EEEEE8",
            highlightthickness=0
        )

        self.canvas.pack(anchor=tkinter.NE, padx=75, pady=3, ipadx=2, ipady=2)

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

def analog_clock_setup(root):
    AnalogClock(root)