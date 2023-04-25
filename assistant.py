import pywintypes  # to avoid dll fail of win32clipboard
import sched
import time
import sys
import keyboard as kb
import win32clipboard as wcb  # requere: pywin32==255
import win32con
import easygui
import re

event_schedule = sched.scheduler(time.time, time.sleep)


def string_process(x):
    x = re.sub('\r', ' ', x)
    x = re.sub('\n', ' ', x)
    while '  ' in x:
        x = re.sub('  ', ' ', x)
    x = re.sub(' - ', '', x)
    x = re.sub('- ', '', x)
    x = re.sub(' -', '', x)
    return x


class CP:
    data_cache = ''

    def clipboard_process():
        try:
            wcb.OpenClipboard()
            data = wcb.GetClipboardData()
            CP.data_cache = data
            data = string_process(data)
            wcb.EmptyClipboard()
            wcb.SetClipboardText(data, win32con.CF_UNICODETEXT)
            wcb.CloseClipboard()
            time.sleep(1)  # avoid open clipboard again to cause error
        except Exception as e:
            print(e)
            try:  # try copy without reformatting
                wcb.OpenClipboard()
                wcb.EmptyClipboard()
                wcb.SetClipboardText(CP.data_cache, win32con.CF_UNICODETEXT)
                CP.data_cache = ''
                wcb.CloseClipboard()
                time.sleep(1)  # avoid open clipboard again to cause error wcb.CloseClipboard()
            except:
                pass


def action():
    if kb.is_pressed('ctrl+w'):  # costomized hotkey
        kb.send('ctrl+c')
        CP.clipboard_process()
        kb.send('ctrl+v')
        time.sleep(1)
    elif kb.is_pressed('ctrl+c') or kb.is_pressed('ctrl+x'):
        CP.clipboard_process()
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
