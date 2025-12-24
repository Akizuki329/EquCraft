#自定义通货可在模板中加入坐标获取逻辑
#加入合法性检测
import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import threading

class GUI:
    def __init__(self,modes=None):
        # 线程锁
        # self.lock = threading.Lock()
        # self.lock.acquire()
        # self.isFirst=True
        self.modes=modes
        self.key_ctrl=keyboard.Controller()

    # return [模式选择，前缀词条，后缀词条，前缀是否允许杂词，后缀是否允许杂词]
    def get_information(self):
        try:
            def to_int_or_zero(entry):
                v = entry.get()
                return int(v) if str(v).strip() != "" else 0
            
            info=[self.mode.get(), self.entry_prefix.get(), self.entry_suffix.get(), \
                    self.permission_var_prefix.get(),self.permission_var_suffix.get()\
                        ,to_int_or_zero(self.entry_prefix_need),to_int_or_zero(self.entry_suffix_need)]
            if hasattr(self, "text_box"):
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END,
                    f"模式: {info[0]}\n"
                    f"前缀允许杂词: {info[3]}, 前缀所需词条数: {info[5]}\n后缀允许杂词: {info[4]}, 后缀所需词条数: {info[6]}\n"
                    f"前缀: {info[1]}\n"
                    f"后缀: {info[2]}\n"
                )
            return info
        except Exception as e:
            print("gui中不合法的输入")

        
    def isLegal(self):
        return self.mode.get()!='' and (self.entry_prefix.get()!='' or self.entry_suffix.get()!='')
    
    def text_output(self,string):
        self.text_box.insert(tk.END,string)
    
    def on_button_click(self):
        # if self.isFirst:
        #     self.isFirst=False
        #     self.lock.release()
        self.key_ctrl.press(keyboard.Key.end)
        # self.text_box.insert(tk.END,self.entry_prefix.get()+self.entry_suffix.get()+\
                            # self.permission_combobox_prefix.get()+self.permission_combobox_suffix.get())
    def gui(self):
        # 创建主窗口
        root = tk.Tk()
        root.title("EquCraft")
        root.geometry("530x420")  # 设置窗口初始大小
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


        # 右侧勾选菜单
        middle_frame = tk.Frame(main_frame)
        middle_frame.grid(row=0, column=1, padx=10, pady=10)

        # 允许含有杂词的选择
        self.permission_var_prefix = tk.BooleanVar()
        permission_label_prefix = tk.Label(middle_frame, text="是否允许含有杂词（前缀）:")
        permission_label_prefix.pack(pady=5)

        self.permission_checkbox_prefix = tk.Checkbutton(middle_frame, text="是", variable=self.permission_var_prefix)
        self.permission_checkbox_prefix.pack(pady=5)

        # 允许含有杂词的选择
        self.permission_var_suffix = tk.BooleanVar()
        permission_label_suffix = tk.Label(middle_frame, text="是否允许含有杂词（后缀）:")
        permission_label_suffix.pack(pady=10)

        self.permission_checkbox_suffix = tk.Checkbutton(middle_frame, text="是", variable=self.permission_var_suffix)
        self.permission_checkbox_suffix.pack(pady=5)

        # 右侧输入框
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=3, padx=10, pady=10)

        label_prefix_need = tk.Label(right_frame, text="前缀所需词条数:")
        label_prefix_need.pack(pady=5)

        self.entry_prefix_need = tk.Entry(right_frame)
        self.entry_prefix_need.pack(pady=5)

        label_suffix_need = tk.Label(right_frame, text="后缀所需词条数:")
        label_suffix_need.pack(pady=5)

        self.entry_suffix_need = tk.Entry(right_frame)
        self.entry_suffix_need.pack(pady=5)

        # 提交按钮
        button = tk.Button(root, text="确定", command=self.on_button_click)
        button.pack(pady=20)

        self.text_box = tk.Text(root, height=15, width=50)
        self.text_box.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=10)
        
        # 运行主循环left_frame
        root.mainloop()