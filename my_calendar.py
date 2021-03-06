# -*- coding: utf-8 -*-
import os
from operator import ge
import tkinter
import datetime as dt
import calendar as cl
import datetime as dt
from webbrowser import get

import get_googlecal
from ping3 import ping, verbose_ping

display_time = dt.datetime.now()
dis_y1 = display_time.year
dis_m1 = display_time.month
dis_d1 = display_time.day

wd = 0
cal = [""]*40
monitor_week = [""]*7 

eshi_dir_id = 0
quit_flag = False

bg_color = "#EEEEE8"
fg_color = "#000000"
font_ui = "Yu Gothic"

month_str = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 
week_str = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"] 


def generate_cal(y1, m1): 
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

def set_cal(cal, cal_cell, year, month): 
    for i1 in range( len(cal) ): 
        str1 = cal[i1] 
        cal_cell[i1]["text"] = str1
        
    event_day_list = []
    #pingが通るか and googleapiに接続するjsonファイルが存在するか
    if ping("google.com") != False and os.path.isfile(os.path.dirname(os.path.abspath(__file__))+'/raspi-calendar.json'):
        import get_googlecal
        event_day_list = get_googlecal.get_event_day(year, month)
    list_data = []
    for i in range(len(event_day_list)):
        if event_day_list[i] > 0:
            list_data.append(str(i+1))
    for ver in range( 6 ): 
        for cal in range( 7 ): 
            if cal == 0: 
                bg1 = "#FFF0F0" 
            elif cal == 6: 
                bg1 = "#F6F0FF" 
            else: 
                bg1 = "#FFFFFF"

            if cal_cell[cal+7*ver]["text"] in list_data :
                bg1 = "#c1ffc1"
            cal_cell[cal+7*ver]["bg"] = bg1

def prev_next(n1, monitor_month_num, monitor_month_str, monitor_year_str, cal_cell): 
    global dis_y1
    global dis_m1
    dis_m1 = dis_m1 + n1 
    if dis_m1 > 12: 
        dis_y1 = dis_y1 + 1 
        dis_m1 = 1 
    elif dis_m1 < 1: 
        dis_y1 = dis_y1 - 1 
        dis_m1 = 12 
    monitor_month_num["text"] = str(dis_m1) 
    monitor_month_str["text"] = month_str[dis_m1-1] 
    monitor_year_str["text"] = str(dis_y1) 
    generate_cal(dis_y1, dis_m1) 
    set_cal(cal, cal_cell, dis_y1, dis_m1)

    now = dt.datetime.now()
    for i1 in range( len(cal) ):
        if cal_cell[i1]["text"] == str(now.day) and dis_y1 == now.year and dis_m1 == now.month:
            cal_cell[i1]["relief"] = 'solid'
            cal_cell[i1]['borderwidth'] = 2
        else:
            cal_cell[i1]["relief"] = 'flat'

def home(monitor_month_num, monitor_month_str, monitor_year_str, cal_cell):
    global display_time
    global dis_y1
    global dis_m1
    global dis_d1

    now = dt.datetime.now()
    m1 = now.month
    y1 = now.year

    display_time = dt.datetime.now()
    dis_y1 = display_time.year
    dis_m1 = display_time.month
    dis_d1 = display_time.day

    monitor_month_num["text"] = str(m1) 
    monitor_month_str["text"] = month_str[m1-1] 
    monitor_year_str["text"] = str(y1) 
    generate_cal(y1, m1) 
    set_cal(cal, cal_cell, y1, m1)
    for i1 in range( len(cal) ):
        if cal_cell[i1]["text"] == str(now.day) and y1 == now.year and m1 == now.month:
            cal_cell[i1]["relief"] = 'solid'
            cal_cell[i1]['borderwidth'] = 2
        else:
            cal_cell[i1]["relief"] = 'flat'



class Drawer:
    def __init__(self, master):
        self.initSetting(master)

    def initSetting(self, master):
        '''カレンダー表示に必要な設定'''
        self.master = master

        self.monitor_month_num = tkinter.Label(font=(font_ui, 26),anchor=tkinter.CENTER, width=2)
        self.monitor_month_num["fg"] = fg_color
        self.monitor_month_num["bg"] = bg_color
        self.monitor_month_num.place(x=425, y=78) 
        self.monitor_month_str = tkinter.Label(font=(font_ui, 10),anchor=tkinter.W, width=10)
        self.monitor_month_str["fg"] = fg_color
        self.monitor_month_str["bg"] = bg_color 
        self.monitor_month_str.place(x=495, y=83)
        self.monitor_year_str = tkinter.Label(font=(font_ui, 12),anchor=tkinter.W, width=10)
        self.monitor_year_str["fg"] = fg_color
        self.monitor_year_str["bg"] = bg_color 
        self.monitor_year_str.place(x=495, y=105)

        
        for ver in range(len(week_str)): 
            monitor_week[ver] = tkinter.Label(text=week_str[ver], font=(font_ui, 8), anchor=tkinter.CENTER, width=10)
            monitor_week[ver]["bg"] = bg_color
            monitor_week[ver]["fg"] = fg_color
            monitor_week[ver].place(x=405+47*ver, y=130)

        self.cal_cell = [""]*42 
        for ver in range( 6 ): 
            for cal in range( 7 ): 
                fg1 = "#000000" 
                if cal == 0: 
                    bg1 = "#FFF0F0" 
                    fg1 = "#FF0000" 
                elif cal == 6: 
                    bg1 = "#F6F0FF" 
                    fg1 = "#0000A0" 
                else: 
                    bg1 = "#FFFFFF"  
                self.cal_cell[cal+7*ver] = tkinter.Label(font=(font_ui, 10), anchor=tkinter.NW, bg=bg1, fg=fg1, relief='flat')#, command=btn_click1) 
                x2 = 415 + 47 * cal 
                y2 = 150 + 47 * ver 
                self.cal_cell[cal+7*ver].place(x=x2, y=y2, width=45, height=45)

        button_prev = tkinter.Button(master, text="<", font=(font_ui, 10), borderwidth=0, bg="#D0D0D0", fg=fg_color, relief='flat', command=lambda:prev_next(-1, self.monitor_month_num, self.monitor_month_str, self.monitor_year_str, self.cal_cell) )
        button_prev.place(x=560, y=440, width=30, height=30)
        button_next = tkinter.Button(master, text=">", font=(font_ui, 10), borderwidth=0, bg="#D0D0D0", fg=fg_color, relief='flat', command=lambda:prev_next(1, self.monitor_month_num, self.monitor_month_str, self.monitor_year_str, self.cal_cell) )
        button_next.place(x=690, y=440, width=30, height=30)
        button_home = tkinter.Button(master, text="home", font=(font_ui, 10), borderwidth=0, bg="#D0D0D0", fg=fg_color, relief='flat', command=lambda:home(self.monitor_month_num, self.monitor_month_str, self.monitor_year_str, self.cal_cell) )
        button_home.place(x=610, y=440, width=60, height=30)

    def update(self):
        prev_next(0, self.monitor_month_num, self.monitor_month_str, self.monitor_year_str, self.cal_cell)
        self.master.after(1000 * 1 * 1, self.update)


class Calendar:

    def __init__(self, master):
        self.master = master
        self.drawer = Drawer(master)

        prev_next(0, self.drawer.monitor_month_num, self.drawer.monitor_month_str, self.drawer.monitor_year_str, self.drawer.cal_cell)
        self.master.after(1000 * 1 * 1, self.drawer.update)