from time import sleep
import bin.config as config
from pynput import keyboard,mouse
import win32clipboard

class operation:
    def __init__(self,onpress_callback): 
        # 控制键盘
        self.key_ctrl = keyboard.Controller()
        # 控制鼠标
        self.mouse_ctrl = mouse.Controller()
        # 监听键盘事件
        self.listener = keyboard.Listener(on_press=onpress_callback)

    def listen_run(self):
        self.listener.run()

    def getCliboardData(self):
        self.safe_clear()
        self.copy()
        return self.safe_paste()

    def copy(self):
        self.key_ctrl.press(keyboard.Key.alt_l)
        #需要等待游戏响应按键并显示物品详情
        sleep(config.KEYBOARD_DELAY)
        self.key_ctrl.press(keyboard.Key.ctrl_l)
        self.key_ctrl.press('c')
        self.key_ctrl.release('c')
        self.key_ctrl.release(keyboard.Key.ctrl_l)
        self.key_ctrl.release(keyboard.Key.alt_l)
        sleep(config.KEYBOARD_DELAY)

    def safe_paste(self):
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

    def safe_clear(self):
        clear = False
        while not clear:
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.SetClipboardText('')
                win32clipboard.CloseClipboard()
                clear = True

            except Exception as e:
                pass

    #left click
    def send_mouse_click_left(self):
        self.mouse_ctrl.click(mouse.Button.left,1)
        sleep(config.MOUSE_DELAY)

    #right click
    def send_mouse_click_right(self):
        self.mouse_ctrl.click(mouse.Button.right,1)
        sleep(config.MOUSE_DELAY)

    def set_mouse(self,x,y):
        self.mouse_ctrl.position=(x,y)
        sleep(config.MOUSE_DELAY)