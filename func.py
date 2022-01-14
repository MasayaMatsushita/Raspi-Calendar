import tkinter
import datetime as dt
import calendar as cl
import datetime as dt

display_time = dt.datetime.now()
dis_y1 = display_time.year
dis_m1 = display_time.month
dis_d1 = display_time.day

wd = 0
cal = [""]*40

month_str = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 


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


def cal_setup(root):
    bg_color = "#EEEEE8"
    font_ui = "Yu Gothic"
    monitor_month_num = tkinter.Label(font=(font_ui, 26),anchor=tkinter.CENTER, width=2)
    monitor_month_num["bg"] = bg_color
    monitor_month_num.place(x=425, y=78) 
    monitor_month_str = tkinter.Label(font=(font_ui, 10),anchor=tkinter.W, width=10)
    monitor_month_str["bg"] = bg_color 
    monitor_month_str.place(x=495, y=83)
    monitor_year_str = tkinter.Label(font=(font_ui, 12),anchor=tkinter.W, width=10)
    monitor_year_str["bg"] = bg_color 
    monitor_year_str.place(x=495, y=105)

    monitor_week = [""]*7 
    week_str = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" ] 
    for ver in range(len(week_str)): 
        monitor_week[ver] = tkinter.Label(text=week_str[ver], font=(font_ui, 8), anchor=tkinter.CENTER, width=10)
        monitor_week[ver]["bg"] = bg_color
        monitor_week[ver].place(x=405+47*ver, y=130)

    cal_cell = [""]*42 
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
            cal_cell[cal+7*ver] = tkinter.Label(font=(font_ui, 10), anchor=tkinter.NW, bg=bg1, fg=fg1, relief='flat')#, command=btn_click1) 
            x2 = 415 + 47 * cal 
            y2 = 150 + 47 * ver 
            cal_cell[cal+7*ver].place(x=x2, y=y2, width=45, height=45)

    button_prev = tkinter.Button(root, text="prev", font=(font_ui, 10), bg="#D0D0D0", relief='flat', command=lambda:prev_next(-1, monitor_month_num, monitor_month_str, monitor_year_str, cal_cell) )
    button_prev.place(x=530, y=440, width=60, height=30)

    button_next = tkinter.Button(root, text="next", font=(font_ui, 10), bg="#D0D0D0", relief='flat', command=lambda:prev_next(1, monitor_month_num, monitor_month_str, monitor_year_str, cal_cell) )
    button_next.place(x=690, y=440, width=60, height=30)

    button_home = tkinter.Button(root, text="home", font=(font_ui, 10), bg="#D0D0D0", relief='flat', command=lambda:home(monitor_month_num, monitor_month_str, monitor_year_str, cal_cell) )
    button_home.place(x=610, y=440, width=60, height=30)

    button_quit = tkinter.Button(root, text=" ", font=(font_ui, 10), 
        bg=bg_color,
        borderwidth=0,
        relief='flat' , command=lambda:quit(root) )
    button_quit.place(x=750, y=5, width=30, height=30)

    prev_next(0, monitor_month_num, monitor_month_str, monitor_year_str, cal_cell)

    return [monitor_month_num, monitor_month_str, monitor_year_str, cal_cell]

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

def set_cal(cal, cal_cell): 
    for i1 in range( len(cal) ): 
        str1 = cal[i1] 
        cal_cell[i1]["text"] = str1 

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
    set_cal(cal, cal_cell)

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
    set_cal(cal, cal_cell)
    for i1 in range( len(cal) ):
        if cal_cell[i1]["text"] == str(now.day) and y1 == now.year and m1 == now.month:
            cal_cell[i1]["relief"] = 'solid'
            cal_cell[i1]['borderwidth'] = 2
        else:
            cal_cell[i1]["relief"] = 'flat'


def quit(root):
    root.destroy()


    