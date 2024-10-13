#第三方库
import importlib
import os
import sys

import win32gui
import threading
from pynput import keyboard

#配置文件
import bin.config as config

#GUI
import bin.gui as GUI

#鼠标键盘操作
import bin.operation as operation

#先增幅，后改造
class Worker:
    def __init__(self) -> None:
        # 是否持续洗
        self.roll_loop_lock_F = threading.Lock()
        self.roll_loop_thread = threading.Thread(target=self.roll_loop)
        self.fever_mode  = False
        self.roll_loop_lock_F.acquire()
        self.roll_loop_thread.start()
        # 上一个物品的详情
        self.last_info   = ''
        # 所有模板
        self.templates = {}
        # 所选择模板
        self.filter_mode = None
        self.filter_func = None
        # 模板合法性
        self.filter_func_isLegal = False
        # 启动GUI
        templates_name=self.load_template()
        self.gui=GUI.GUI(templates_name)
        self.gui_Thread=threading.Thread(target=self.gui.gui)
        self.gui_Thread.start()
        # 初始化控制类
        self.operate = operation.operation(self.onpress_callback)
        self.operate.listen_run()

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
        try:
            self.filter_mode = self.templates[self.gui.mode.get()]
            self.filter_func = self.filter_mode.filter
            if self.filter_mode.use_message_bool():
                self.filter_mode.set(self.gui.get_information())
            self.filter_func_isLegal = True
        except Exception as e:
            self.filter_func_isLegal == False
            print(e)
            print("reload():模板载入失败")

        print('\nPress "insert" to craft item once, press "home" to craft until finish, press "end" to rechoose\n')

    def get_item(self,x,y):
        self.operate.set_mouse(x,y)
        self.operate.send_mouse_click_right()

    def get_Currency(self,currency):
        self.get_item(config.location[currency][0],config.location[currency][1])

    def use_Currency(self):
        self.operate.set_mouse(config.location["Item"][0],config.location["Item"][1])
        self.operate.send_mouse_click_left()

    def roll(self):
        if self.filter_func_isLegal == False:
            return

        item_info = self.operate.getCliboardData()

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
    
    def roll_loop_begin(self):
        if self.fever_mode==False:
            self.roll_loop_lock_F.release()
    
    def roll_loop_end(self):
        print(2)
        if self.fever_mode==True:
            print(1)
            self.roll_loop_lock_F.acquire()
            self.fever_mode=False
            
    def onpress_callback(self,key: keyboard.KeyCode):
        # print(key)
        try:
            if key == keyboard.Key.insert:
                self.roll()

            if key == keyboard.Key.end:
                if self.fever_mode == True:
                    self.roll_loop_end()
                    print('Auto Craft Mode End.')
                self.reload()

            if key == keyboard.Key.home:
                if self.fever_mode == True:
                    self.roll_loop_end()
                    print('Auto Craft Mode End.')
                else:
                    self.last_info  = ''
                    self.roll_loop_begin()
                    print('Ready to Craft Equipment.')
            
        except Exception as e:
            print(e)

Worker()
#改用阻塞模式读取按键并运行
