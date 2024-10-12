#第三方库
import importlib
import os
import sys

from pynput import keyboard,mouse
import win32gui
import threading
import win32clipboard
from time import sleep

#配置文件
import bin.config as config

#GUI
import bin.gui as GUI

#先增幅，后改造
class Worker:
    def __init__(self) -> None:
        # 是否持续洗
        self.fever_mode  = False
        self.roll_loop_lock_F = threading.Lock()
        self.roll_loop_thread = threading.Thread(target=self.roll_loop)
        self.roll_loop_lock_F.acquire()
        self.roll_loop_thread.start()
        # 上一个物品的详情
        self.last_info   = ''
        # 所有模板
        self.templates = {}
        # 所选择模板
        self.filter_func = None
        # 监听键盘事件
        self.listener = keyboard.Listener(on_press=self.onpress_callback)
        # 控制键盘
        self.key_ctrl = keyboard.Controller()
        # 控制鼠标
        self.mouse_ctrl = mouse.Controller()
        # 启动GUI
        templates_name=self.load_template()
        self.gui=GUI.GUI(templates_name)
        self.gui_Thread=threading.Thread(target=self.gui.gui)
        self.gui_Thread.start()

    def load_template(self):
        print('\n# -------------------------- #\n加载 Craft 模板 ...\n')

        if os.path.exists(config.TEMPLATES_DIR):
            templates_name = [_ for _ in os.listdir(config.TEMPLATES_DIR) if _.endswith('.py')]
            templates_name = [_.replace(".py", "") for _ in templates_name]
            print(templates_name)

            print('\n# -------------------------- #\n')

            try:
                sys.path.append(os.getcwd())
                for template_name in templates_name:
                    self.templates[template_name] = importlib.import_module(f'{config.TEMPLATES_DIR}.{template_name}')

            except Exception as e:
                print(e)
                win32gui.MessageBox(0, "模板库文件读取失败", "Error", 0)

        else:
            win32gui.MessageBox(0, "模板库不存在", "Error", 0)

        return templates_name

    def reload(self):
        print('POE - Auto Craft Ready to Rool.')
        self.filter_func = self.templates[self.gui.mode.get()].filter
        print('\nPress "insert" to craft item once, press "home" to craft until finish, press "end" to rechoose\n')

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

    def get_item(self,x,y):
        self.set_mouse(x,y)
        self.send_mouse_click_right()

    def get_Currency(self,currency):
        self.get_item(config.location[currency][0],config.location[currency][1])

    def use_Currency(self):
        self.set_mouse(config.location["Item"][0],config.location["Item"][1])
        self.send_mouse_click_left()

    def roll(self):
        self.safe_clear()
        self.copy()
        item_info = self.safe_paste()

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

    def roll_loop(self):
        while True:
            if self.fever_mode == False:
                self.roll_loop_lock_F.acquire()
                self.fever_mode = True
                self.roll_loop_lock_F.release()
            self.roll()
            
    def onpress_callback(self,key: keyboard.KeyCode):
        print(key)
        try:
            if key == keyboard.Key.insert:
                self.roll()

            if key == keyboard.Key.end:
                if self.fever_mode == True:
                    self.roll_loop_lock_F.acquire()
                    self.fever_mode = False
                    print('Auto Craft Mode End.')
                self.reload()

            if key == keyboard.Key.home:
                if self.fever_mode == True:
                    self.roll_loop_lock_F.acquire()
                    self.fever_mode = False
                    print('Auto Craft Mode End.')
                else:
                    self.last_info  = ''
                    self.roll_loop_lock_F.release()
                    print('Ready to Craft Equipment.')
            
        except Exception as e:
            print(e)

    def run(self):
        self.gui.lock.acquire()
        self.reload()
        self.gui.lock.release()
        self.listener.run()

worker = Worker()
worker.run()

#改用阻塞模式读取按键并运行
