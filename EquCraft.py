#第三方库
import importlib
import os
import sys
from time import sleep

import win32api
import win32clipboard
import win32con
import win32gui

from pynput import keyboard

#配置文件
import bin.config as config

#copy
def send_copy_singal():
    sleep(0.01)
    win32api.keybd_event(0x12, 0, 0, 0) # press down Alt
    sleep(0.01)
    win32api.keybd_event(17, 0, 0, 0) # press down Ctrl
    win32api.keybd_event(67, 0, 0, 0) # press down C
    sleep(0.01)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0) # release Ctrl
    win32api.keybd_event(67, 0, win32con.KEYEVENTF_KEYUP, 0) # release C
    sleep(0.01)
    win32api.keybd_event(0x12, 0, win32con.KEYEVENTF_KEYUP, 0) # press down Alt


def safe_paste():

    got_data = False
    while not got_data:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            got_data = True

        except Exception as e:
            pass
    return data

def safe_clear():

    clear = False
    while not clear:
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.SetClipboardText('')
            win32clipboard.CloseClipboard()
            clear = True

        except Exception as e:
            pass

def load_template():

    print('')
    print('# -------------------------- #')
    print('加载 Craft 模板 ...')

    if os.path.exists(config.TEMPLATES_DIR):

        templates = [_ for _ in os.listdir(config.TEMPLATES_DIR) if _.endswith('.py')]
        dictionary = {}

        for fidx, file in enumerate(templates):
            dictionary[fidx + 1] = str(file).replace('.py', '')
            print(f"{fidx + 1}. {str(file).replace('.py', '')}")

        print('# -------------------------- #')
        print('')

        selected = input(f'Select Craft Template [1 - {len(templates)}]: ')

        try:
            selected = int(selected)
            if selected >= 1 and selected <= len(templates):

                print('')
                print(f'Loading {dictionary[selected]}')
                sys.path.append(os.getcwd())            
                return importlib.import_module(f'{config.TEMPLATES_DIR}.{dictionary[selected]}')

            else:
                raise Exception('Index Out Of Range.')

        except Exception as e:
            print(e)
            win32gui.MessageBox(0, "模板库文件读取失败", "Error", 0)

    else:
        win32gui.MessageBox(0, "模板库文件不存在", "Error", 0)


#先增幅，后改造
class Worker:

    def __init__(self) -> None:
        self.fever_mode  = False
        self.last_info   = ''
        self.filter_func = None

    #left click
    def send_mouse_click_left(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0)

    #right click
    def send_mouse_click_right(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0, 0, 0)

    def get_item(self,x,y):
        isSelect = False
        while win32api.GetCursorPos()!=(x,y):
            win32api.SetCursorPos((x,y))
            sleep(config.MOUSE_DELAY)
        # item_info=safe_paste()
        # func(item_info)
        self.send_mouse_click_right()
        sleep(config.MOUSE_DELAY)

    def get_Currency(self,currency):
        self.get_item(config.location[currency][0],config.location[currency][1])

    def use_Currency(self):
        while win32api.GetCursorPos()!=(config.location["Item"][0],config.location["Item"][1]):
            win32api.SetCursorPos((config.location["Item"][0],config.location["Item"][1]))
            sleep(config.MOUSE_DELAY)
            # item_info=safe_paste()
            # isSelect = self.item_func(item_info)
        self.send_mouse_click_left()
        sleep(config.MOUSE_DELAY)



    def roll(self):
        safe_clear()
        sleep(config.ROLL_DELAY)
        send_copy_singal()
        item_info = safe_paste()

        if item_info == self.last_info or item_info == '': return
        isCrafted,Currency = self.filter_func(item_info)

        try:
            if isCrafted:
                print('Item has been crafted.')
                self.fever_mode = False
                return

            else:
                self.get_Currency(Currency)
                self.use_Currency()

        except Exception as e:
            print(e)
            self.fever_mode = False
            return

        self.last_info = item_info

def onpress_callback(key: keyboard.KeyCode):

    try:
        if key == keyboard.Key.end: 
            sys.exit(0)
        if key == keyboard.Key.insert:
            worker.roll()

    except Exception as e:
        print(e)

   

    if key == keyboard.Key.insert and worker.fever_mode == True:
        win32api.keybd_event(0x2D, 0, 0, 0) # press down space  


def onrelease_callback(key: keyboard.KeyCode):

    try:
        if key in {keyboard.Key.home}:
            if worker.fever_mode is True:
                worker.fever_mode = False
                print('Auto Craft Mode End.')
            else:
                worker.fever_mode = True
                worker.last_info  = ''
                print('Ready to Craft Equipment.')
                sleep(1)
                win32api.keybd_event(0x2D, 0, 0, 0) # press down space  

    except Exception as e:
        print(e)


worker = Worker()


print('POE - Auto Craft Ready to Rool.')

template           = load_template()

worker.filter_func = template.filter



print('')

print('Press "Space" to craft item once, press "Capslock" to craft until finish.')



hook = keyboard.Listener

with hook(on_press=onpress_callback, on_release=onrelease_callback, suppress=False) as listener:

    listener.join()