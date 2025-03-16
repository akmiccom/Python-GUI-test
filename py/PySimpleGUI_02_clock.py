#!/usr/bin/env python
# coding: utf-8

# # PySimpleGUI Clock
# - PySimpleGUI を使って時計ウィジェットを作成
# - フォント選択設定 [フォント選択設定 PySimpleGUI-github](https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Font_Previewer.py)

# In[5]:


#!/usr/bin/env python
# coding: utf-8

import PySimpleGUI as sg
import requests
from datetime import datetime
from pyautogui import size
import platform  # add chatGPT

API_KEY = "51eed4f60902080d2ff757833123f255"
CITY = "Sayamashi"
UNITS = "metric"


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={UNITS}&lang=ja"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather = data["weather"][0]["description"]  # 天気の説明
            temp = data["main"]["temp"]  # 気温
            return f"{weather} {temp:.1f}°C"
        else:
            return "ERROR"
    except Exception as e:
        return "FAILED"


def date_info(time_format, date_format):
    now = datetime.now()
    time = now.strftime(time_format)
    date = now.strftime(date_format)
    weekday = now.strftime("%a")
    return time, date, weekday


# OSごとの時間・日付フォーマットの設定
if platform.system() == "Windows":
    time_format = "%H:%M:%S"
    date_format = "%Y/%#m/%#d"
else:
    time_format = "%H:%M:%S"
    date_format = "%Y/%m/%d"

layout = [
    [sg.Text(font=("impact", 50), text_color="gray", key="-time-")],
    [
        sg.Text(font=("impact", 20), text_color="gray", key="-date-"),
        sg.Text(font=("impact", 20), text_color="gray", key="-weather-"),
    ],
]

window = sg.Window(
    title="clock",
    layout=layout,
    location=(size()[0] - 450, size()[1] - 380),
    transparent_color=sg.theme_background_color(),
    no_titlebar=True,
    right_click_menu=["menu", ["Exit", "!Properties"]],
    keep_on_top=True,
    grab_anywhere_using_control=True,
    alpha_channel=0.5,
)

# 天気を取得
weather_info = get_weather(CITY)

while True:
    event, values = window.read(timeout=1000, timeout_key="-timeout-")
    if event in [sg.WIN_CLOSED, "Exit"]:
        break
    elif event in "-timeout-":
        time, date, weekday = date_info(time_format, date_format)
        window["-time-"].update(time)
        window["-date-"].update(f"{date} {weekday}")
        weather_info = get_weather(CITY)
        window["-weather-"].update(weather_info)

window.close()
