#!/usr/bin/env python
# coding: utf-8

# # PySimpleGUI Clock
# - PySimpleGUI を使って時計ウィジェットを作成
# - フォント選択設定 [フォント選択設定 PySimpleGUI-github](https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Font_Previewer.py)

# In[5]:


# !/usr/bin/env python
# coding: utf-8

import PySimpleGUI as sg
import requests
import os
from datetime import datetime
from pyautogui import size
import platform
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import certifi

# .env ファイルを読み込む
load_dotenv()
API_KEY = os.getenv("WEATHER_COM_API_KEY")
CITY = "Sayama"
UNITS = "metric"
URL = r"http://api.weatherapi.com/v1/current.json"

print(API_KEY)


def get_weather(city):
    params = {"key": API_KEY, "q": city, "lang": "en"}
    try:
        response = requests.get(URL, params=params)
        data = response.json()
        if "current" in data:
            weather = data["current"]["condition"]["text"]
            temp = data["current"]["temp_c"]
            icon_url = "https:" + data["current"]["condition"]["icon"]
            print(icon_url)
            return f"{weather} {temp:.0f}°C", icon_url
        else:
            return "ERROR"
    except Exception as e:
        print(e)
        return "FAILED"


def date_info(time_format, date_format):
    now = datetime.now()
    time = now.strftime(time_format)
    date = now.strftime(date_format)
    weekday = now.strftime("%a")
    return time, date, weekday


def download_image(icon_url):
    try:
        response = requests.get(icon_url, verify=certifi.where())
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(e)
        return None


# OSごとの時間・日付フォーマットの設定
if platform.system() == "Windows":
    time_format = "%H:%M:%S"
    date_format = "%Y/%#m/%#d"
else:
    time_format = "%H:%M:%S"
    date_format = "%Y/%m/%d"

# Layout
layout = [
    [sg.Text(font=("impact", 50), text_color="gray", key="-time-")],
    [sg.Text(font=("impact", 20), text_color="gray", key="-date-")],
    [sg.Text(font=("impact", 20), text_color="gray", key="-weather-")],
]

# Window
window = sg.Window(
    title="clock",
    layout=layout,
    location=(size()[0] - 450, size()[1] - 450),
    transparent_color=sg.theme_background_color(),
    no_titlebar=True,
    right_click_menu=["menu", ["Exit", "!Properties"]],
    keep_on_top=True,
    grab_anywhere_using_control=True,
    alpha_channel=0.5,
)

# 天気を取得
weather_info, icon_url = get_weather(CITY)
weather_update_interval = 60000 * 1
last_weather_update = datetime.now()

if icon_url:
    weather_icon = download_image(icon_url)
    if weather_icon:
        weather_icon.thumbnail((50, 50))  # アイコンサイズ調整
        window["-icon-"].update(data=weather_icon)

while True:
    event, values = window.read(timeout=1000, timeout_key="-timeout-")
    if event in [sg.WIN_CLOSED, "Exit"]:
        break
    elif event == "-timeout-":
        time, date, weekday = date_info(time_format, date_format)
        window["-time-"].update(time)
        window["-date-"].update(f"{date} {weekday}")

        if (
            datetime.now() - last_weather_update
        ).seconds >= weather_update_interval / 1000:
            weather_info = get_weather(CITY)
            window["-weather-"].update(weather_info)
            last_weather_update = datetime.now()
            if icon_url:
                weather_icon = download_image(icon_url)
                if weather_icon:
                    weather_icon.thumbnail((50, 50))
                    window["-icon-"].update(data=weather_icon)

    elif event in ["-time-", "-date-", "-weather-"]:
        window[event].update(background_color="darkgray")

window.close()
