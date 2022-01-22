# -*- coding: utf-8 -*-
from datetime import datetime as dt
import calendar
import googleapiclient.discovery
import google.auth
import os
import sys

# 編集スコープの設定(今回は読み書き両方OKの設定)
SCOPES = ['https://www.googleapis.com/auth/calendar']
# カレンダーIDの設定(基本的には自身のgmailのアドレス)
calendar_id = 'masaya.sj.gm@gmail.com'
    
# 認証ファイルを使用して認証用オブジェクトを作成
path = os.path.dirname(os.path.abspath(__file__))
# path = os.path.dirname(os.path.abspath(sys.argv[0]))
gapi_creds = google.auth.load_credentials_from_file(path+'/raspi-calendar-338212-acbf00829c2d.json', SCOPES)[0]
    
# 認証用オブジェクトを使用してAPIを呼び出すためのオブジェクト作成
service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)

def get_event_day(year, month):
    day_end = calendar.monthrange(year, month)[1]
    event_day = [0] * day_end
# Get events from Google Calendar API
    events_result = service.events().list(
            calendarId = calendar_id,
            timeMin = str(year)+"-"+str(month)+"-1T00:00:00+09:00",
            timeMax = str(year)+"-"+str(month)+"-"+str(day_end)+"T23:59:59+09:00",
            timeZone = None,
            singleEvents = True,
            orderBy = "startTime",
            ).execute() 

    # Pick up only start time, end time and summary info
    events = events_result.get('items', [])
    # Generate output text
    for event in events:
        if event['start'].get('dateTime') != None:
            date = dt.strptime(event['start'].get('dateTime'), '%Y-%m-%dT%H:%M:%S+09:00')
            start = date.day
            date = dt.strptime(event['end'].get('dateTime'), '%Y-%m-%dT%H:%M:%S+09:00')
            end = date.day

        else:
            date = dt.strptime(event['start'].get('date'), '%Y-%m-%d')
            start = date.day
            date = dt.strptime(event['end'].get('date'), '%Y-%m-%d')
            end = date.day-1

        if end-start >= 0:
            for i in range(start-1, end):    
                event_day[i] += 1
        else:
            for i in range(start-1, len(event_day)):
                event_day[i] += 1

    return event_day    