#自定义通货可在模板中加入坐标获取逻辑
#加入合法性检测
import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import threading

class GUI:
    def __init__(self,modes):
        # 线程锁
        self.lock = threading.Lock()
        self.lock.acquire()
        self.isFirst=True
        self.modes=modes

        
    def isLegal(self):
        return self.mode.get()!='' and (self.entry_prefix.get()!='' or self.entry_suffix.get()!='')
    
    def on_button_click(self):
        if self.isFirst:
            self.isFirst=False
            self.lock.release()
        keyboard.Controller.press(keyboard.Key.end)
        # self.text_box.insert(tk.END,self.entry_prefix.get()+self.entry_suffix.get()+\
                            # self.permission_combobox_prefix.get()+self.permission_combobox_suffix.get())
    def gui(self):
        # 创建主窗口
        root = tk.Tk()
        root.title("EquCraft")
        root.geometry("370x400")  # 设置窗口初始大小
        root.resizable(False, False)  # 禁止调整窗口大小

        # 创建居中的下拉式菜单
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        selected_option = tk.StringVar()
        self.mode = ttk.Combobox(top_frame, values=self.modes, textvariable=selected_option)
        self.mode.pack(side=tk.TOP, pady=10)
        self.mode.current(0)  # 设置默认值

        # 创建主框架，分为两列
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧输入框
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10)

        label_prefix = tk.Label(left_frame, text="前缀可选词条:")
        label_prefix.pack(pady=5)

        self.entry_prefix = tk.Entry(left_frame)
        self.entry_prefix.pack(pady=5)

        label_suffix = tk.Label(left_frame, text="后缀可选词条:")
        label_suffix.pack(pady=5)

        self.entry_suffix = tk.Entry(left_frame)
        self.entry_suffix.pack(pady=5)


        # 右侧下拉式菜单
        permissions = ["是", "否"]

        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10)

        permission_label_prefix = tk.Label(right_frame, text="是否允许含有杂词:")
        permission_label_prefix.pack(pady=5)

        self.permission_combobox_prefix = ttk.Combobox(right_frame, values=permissions)
        self.permission_combobox_prefix.pack(pady=5)
        self.permission_combobox_prefix.current(0)  # 设置默认值

        permission_label_suffix = tk.Label(right_frame, text="是否允许含有杂词:")
        permission_label_suffix.pack(pady=10)

        self.permission_combobox_suffix = ttk.Combobox(right_frame, values=permissions)
        self.permission_combobox_suffix.pack(pady=5)
        self.permission_combobox_suffix.current(0)  # 设置默认值


        # 提交按钮
        button = tk.Button(root, text="确定", command=self.on_button_click)
        button.pack(pady=20)

        self.text_box = tk.Text(root, height=5, width=50)
        self.text_box.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # 运行主循环
        root.mainloop()
