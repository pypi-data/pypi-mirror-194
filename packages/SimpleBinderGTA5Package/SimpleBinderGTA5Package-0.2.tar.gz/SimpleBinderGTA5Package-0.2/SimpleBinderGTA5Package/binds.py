from time import sleep

import keyboard
from win32gui import GetWindowText, GetForegroundWindow

def keypress(key):
    keyboard.press(key)
    sleep(0.1)
    keyboard.release(key)

def is_gta_active():
    return GetWindowText(GetForegroundWindow()) == "GTA:5:RP"

def send_to_chat(message):
    if is_gta_active():
        keypress("F6")
        keyboard.write(message)
        keypress('Enter')

def send_messages_to_chat(messages_list, delay=0):
    for message in messages_list:
        send_to_chat(message)
        sleep(delay)


keyboard.add_hotkey("Ctrl + 1", lambda: send_to_chat("/me Достал документ из правого кармана."))
keyboard.add_hotkey("Ctrl + 2", lambda: send_messages_to_chat(
    ["Админ вы здесь?", "Игрок напротив использует читы"], 2
))

while True:
    pass