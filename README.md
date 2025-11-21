**概述**
- **项目说明**: `EquCraft` 是用于在《流放之路》类流程中自动化判断物品并选择对应通货（例如增幅、改造、崇高等）执行特定脚本进行装备制作的工具。
- **代码位置**: 主要实现位于 `bin/` 目录；模板文件放在 `Templates/`。

**GUI 使用**
- **启动**: 在 Windows 下可运行 `go-Craft.bat` 或在所在目录直接运行 `python EquCraft.py`。确保已安装依赖（参见“运行与依赖”）。
- **主窗口字段**:
-  **模式（下拉）**: 选择模板或运行模式，对应传入模板的模式参数（`self.modes`）。
-  **前缀可选词条**: 在此输入以空格分隔的前缀关键词集合（例: `敏捷 力量 攻击速度`）。
-  **后缀可选词条**: 同上，输入后缀关键词集合。
-  **是否允许含有杂词（前缀/后缀）**: 勾选后允许物品包含非目标词条。
-  **前缀/后缀所需词条数**: 输入整数，空值会被视为 `0`。
-  **确定 按钮**: 当前按钮触发 `on_button_click`（默认只按 End 键并不自动调用 `get_information()`）。如果希望点击“确定”后在文本框显示所有读取信息，可在 `bin/gui.py` 中把 `on_button_click` 改为调用 `self.get_information()`。
- **输出文本框**: 程序会在 GUI 底部的文本框中显示读取到的信息或运行提示。若需要更高的显示区域，可修改 `bin/gui.py` 中 `root.geometry(...)` 和 `self.text_box` 的 `height` / `fill` / `expand` 参数。

**`config` 文件说明**
- **文件路径**: `bin/config.py`。
-  **主要常量**:
-   - `TEMPLATES_DIR`: 模板目录名（默认 `'Templates'`）。
-   - `ROLL_DELAY`: 脚本内某些轮询或按键间的延迟（秒）。
-   - `MOUSE_DELAY`: 鼠标操作后的等待时间（秒）。
-   - `KEYBOARD_DELAY`: 键盘操作后的等待时间（秒）。
-  **位置字典 `location`**: 将逻辑通货名映射到界面坐标，例如 `location={"Item":(340,460),"Aug":(230,330),...}`。如果游戏窗口或分辨率不同，需调整这些坐标以保证点击正确。

**自定义模板说明**
- **模板路径**: 放在 `Templates/` 下，每个模板实现一个 `Template` 类并继承 `Templates/words/AbstractTemplate.py` 中的 `AbstractTemplate`。
- **必须实现的方法**:
-  - `introduction(self)`: 输出模板信息（可用于调试和加载提示）。
-  - `filter_init(self)`: 在调用 `set(information)` 后运行，用来初始化模板的内部状态（例如检查 `prefix_need` 范围等）。
-  - `filter(self, item: str) -> bool`: 接受物品文本（从粘贴板获得），返回一个 `(bool, currency)` 或 `(bool, '')` 规则（示例模板中有更完整的返回逻辑）。
-  - `use_message_bool(self)`: 返回 `True` 或 `False`，表示模板是否使用 GUI 传入的参数。
- **`set(information)` 的数据格式**:
-  调用 `set(information)` 时，`information` 应为列表，内部解包为 `[_, prefix, suffix, prefix_otherwords, suffix_otherwords, prefix_need, suffix_need]`。
-  其中 `prefix` 与 `suffix` 在内部会用 `str.split(..., ' ')` 切分成词条列表；`prefix_need` 与 `suffix_need` 必须为整数（或 0）。
- **实现提示**:
-  - 查看 `Templates/改造增幅洗魔法物品.py` 中的示例实现，了解如何统计词缀、判断物品稀有度、以及返回期望的通货字符串。
-  - 在 `AbstractTemplate.situation(...)` 中已有对“允许杂词”、“词条数量是否足够”等判定逻辑，可复用该函数来简化模板判断。
-  - 当模板需要 GUI 传入参数时，`use_message_bool` 返回 `True`，框架会在运行时把 GUI 的 `get_information()` 返回值传入模板的 `set()` 中。

**运行与依赖**
- **依赖**: 请确保安装了 `pynput`、`pywin32`（用于 Windows 剪贴板访问）等。可以使用项目根目录下的 `requirments.txt`（注意文件名拼写）来安装：

```powershell
pip install -r requirments.txt
```

- **启动**: 推荐使用 `go-Craft.bat`（Windows）或直接运行：

```powershell
python EquCraft.py
```

**调试提示**
- **文本框太小**: 编辑 `bin/gui.py`，把 `root.geometry("530x420")` 的高度改大（例如 `"530x600"`），并将 `self.text_box = tk.Text(..., height=20, ...)`，以及使用 `self.text_box.pack(..., fill=tk.BOTH, expand=True)` 来让文本框占满底部空间。
- **确保生效**: 修改代码后保存并重启程序，避免同时运行旧实例导致“没变化”。