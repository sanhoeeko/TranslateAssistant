import pywintypes  # to avoid dll fail of win32clipboard
import sched
import time
import sys
import keyboard as kb
import win32clipboard as wcb  # requere: pywin32==255
import easygui
import re

event_schedule = sched.scheduler(time.time, time.sleep)


def string_process(x):
    x = re.sub('\r', ' ', x)
    x = re.sub('\n', ' ', x)
    while '  ' in x:
        x = re.sub('  ', ' ', x)
    x = re.sub(' -', '', x)
    return x


def clipboard_process():
    wcb.OpenClipboard()
    data = wcb.GetClipboardData()
    data = string_process(data)
    # print(data)
    wcb.EmptyClipboard()
    wcb.SetClipboardText(data)
    wcb.CloseClipboard()


def action():
    if kb.is_pressed('ctrl+w'):  # costomized hotkey
        kb.send('ctrl+c')
        clipboard_process()
        kb.send('ctrl+v')
    elif kb.is_pressed('ctrl+c') or kb.is_pressed('ctrl+x'):
        clipboard_process()
    elif kb.is_pressed('ctrl+e'):
        show_info()
    elif kb.is_pressed('ctrl+q'):
        sys.exit(0)
    event_schedule.enter(0.1, 1, action)


def show_info():
    info = """
    Ctrl + W: normalize text.
    Ctrl + E: check the activation of the assistant.
    Ctrl + Q: quit the assistant.
    """
    easygui.msgbox(info, title="Nya~~")


show_info()
event_schedule.enter(0.1, 1, action)
event_schedule.run()
