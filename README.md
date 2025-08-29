# V-Plotter

一个基于PyQt6和Matplotlib的简单数据可视化应用程序，提供表格数据管理和基本的图表绘制功能。
(好吧其实只是我不想每次写数据可视化的时候都用Pandas+Matplotlib重复造轮子,所以整合了一下)

## 功能特性

- 📊 数据表格管理：创建、编辑和保存数据表格
- 📈 图表类型支持：折线图、条形图、饼图、散点图等
- 🎨 自定义图表样式：可调整颜色、尺寸和样式参数
- ⚙️ 偏好设置：提供数据界面和绘图参数的详细配置选项
- 🖋️ 字体管理：支持自定义应用程序字体样式
- 💾 数据持久化：支持数据导入导出

## 安装指南

### 前提条件

- Python 3.9 或更高版本
- pip (Python包管理器)
- conda (可选，用于创建虚拟环境)

### 安装步骤

1. 克隆或下载项目代码
2. 创建并激活虚拟环境（可选但推荐）：

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

    或者使用conda

    ```bash
    conda create -n venv python=3.9
    conda activate venv
    ```

3. 安装依赖包：

   ```bash
   pip install -r requirements.txt
   ```

4. 运行应用程序：

   ```bash
   python main.py
   ```

## 项目结构

```text
v-plotter/
├── main.py                # 应用程序入口点
├── LICENSE               # 许可证文件
├── requirements.txt      # 项目依赖
├── setup.py             # 安装脚本
├── pytest.ini           # pytest配置
├── README.md            # 项目说明文档
└── __init__.py          
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   │   ├── base_theme.py          # 抽象主题基类
│   │   ├── command_manager.py     # 命令管理
│   │   ├── data_container.py      # 数据容器管理
│   │   ├── font_manager.py        # 字体管理
│   │   ├── settings_manager.py    # 设置管理
│   │   ├── signals.py             # 信号定义
│   │   ├── theme_manager.py       # 主题管理
│   │   └── themes/                # 主题实现目录
│   │       ├── dark_theme.py      # 深色主题实现
│   │       └── light_theme.py     # 浅色主题实现
│   ├── resources/         # 资源文件目录
│   │   ├── icons/                # 图标资源目录
│   │   └── themes/               # 主题资源目录
│   │       ├── dark/             # 深色主题资源
│   │       │   ├── styles.qss           # 深色主题样式表
│   │       │   └── theme.json          # 深色主题配置
│   │       └── light/            # 浅色主题资源
│   │           ├── styles.qss          # 浅色主题样式表
│   │           └── theme.json         # 浅色主题配置
│   ├── ui/                # 用户界面模块
│   │   ├── core_components/       # 核心UI组件
│   │   │   ├── data_overview.py       # 数据概览组件
│   │   │   ├── parent_table_tab.py    # 父表格标签页
│   │   │   ├── table_tab_area.py      # 表格标签区域
│   │   │   ├── table_view_tab.py      # 表格视图标签页
│   │   │   └── __init__.py            
│   │   ├── dialogs/               # 对话框组件
│   │   │   ├── data_interface_tab.py      # 数据界面设置标签页
│   │   │   ├── filter_dialogs.py         # 过滤对话框
│   │   │   ├── find_replace_dialogs.py   # 查找替换对话框
│   │   │   ├── plot_settings_tab.py      # 绘图参数设置标签页
│   │   │   ├── preferences_dialog.py     # 偏好设置对话框
│   │   │   └── theme_dialog.py           # 主题设置对话框
│   │   ├── menu_components/       # 菜单组件
│   │   │   ├── edit_menu.py       # 编辑菜单
│   │   │   ├── file_menu.py       # 文件菜单
│   │   │   ├── help_menu.py       # 帮助菜单
│   │   │   ├── tools_menu.py      # 工具菜单
│   │   │   ├── view_menu.py       # 视图菜单
│   │   │   └── __init__.py        
│   │   ├── theme_components/      # 主题相关组件
│   │   │   └── styled_widgets.py  # 样式化部件
│   │   ├── chart_windows.py       # 图表窗口
│   │   ├── main_window.py         # 主窗口
│   │   └── menu.py                # 菜单栏
│   └── utils/             # 工具函数目录
└── test/                  # 测试目录
    ├── __init__.py        
    └── data/              # 测试数据
```

## 使用说明

### 基本操作

1. **创建数据表格**：
   - 通过文件菜单或工具栏创建新的数据表格
   - 在表格视图中直接编辑数据
   - 使用右键菜单添加/删除行列

2. **绘制图表**：
   - 选择要绘制的数据表格
   - 通过工具菜单选择图表类型
   - 图表将在新窗口中显示

3. **调整设置**：
   - 通过工具菜单打开偏好设置
   - 调整数据界面和绘图参数
   - 应用设置以立即生效

### 主题切换操作

1. **通过菜单切换主题**：
   - 点击"视图"菜单
   - 选择"主题"选项
   - 在弹出的对话框中选择喜欢的主题
   - 点击"确定"应用主题

2. **主题自动保存**：
   - 应用程序会自动记住您选择的主题
   - 下次启动时会自动应用上次使用的主题

### 设置管理

1. **偏好设置**：
   - 通过"工具"菜单中的"偏好设置"访问
   - 包含"数据界面设置"和"绘图参数设置"两个标签页
   - 设置会自动保存并在应用程序重启后保持

2. **窗口状态记忆**：
   - 应用程序会记住窗口的大小、位置和布局
   - 关闭后重新打开时会恢复之前的窗口状态

### 快捷键

- `Ctrl+O`: 打开数据表格
- `Ctrl+N`: 新建数据表格
- `Ctrl+S`: 保存数据表格
- `Ctrl+Shift+R`: 添加行
- `Ctrl+Shift+D`: 删除行
- `Ctrl+Shift+T`: 添加列
- `Ctrl+Shift+X`: 删除列
- `Ctrl+A`: 全选
- `Esc`: 清除选择
- `Del`: 清除选中内容

## 开发指南

### 添加新的图表类型

1. 在 `src/ui/chart_windows.py` 中的 `ChartWindow` 类中添加新的绘图方法
2. 在 `src/ui/menu_components/tools_menu.py` 中添加对应的菜单项和信号处理
3. 在 `src/core/signals.py` 中添加相应的信号定义

### 自定义设置选项

1. 在 `src/ui/dialogs/` 目录下的相应标签页中添加新的设置控件
2. 在 `src/core/settings_manager.py` 中实现设置的保存和加载逻辑
3. 在应用程序中实现设置的应用逻辑

### 添加新主题

1. 在 `src/core/themes/`
2. 目录下创建新的主题类，继承自 `BaseTheme`
3. 实现所有抽象方法：`get_stylesheet()`, `get_icon()`, `apply_to_app()`, `apply_to_widget()`
4. 在 `src/resources/themes/` 目录下创建对应的资源文件夹，包含样式表和配置文件
5. 在 `ThemeManager` 的 `_discover_themes` 方法中添加对新主题的自动发现逻辑

### 自定义样式

1. 编辑主题目录下的 `styles.qss` 文件来自定义样式
2. 使用 Qt 样式表语法控制各个部件的 appearance
3. 可以通过 `theme.json` 配置文件定义颜色角色和字体设置

### 信号系统

应用程序使用基于 PyQt 信号的发布-订阅模式进行组件间通信：

- `theme_signals`：处理主题相关事件
- `settings_signals`：处理设置变更事件
- `plot_signals`：处理绘图相关事件

## 更新记录

### 2025.08.26

#### 主题系统架构

1. **BaseTheme**：抽象基类，定义主题接口
2. **ThemeManager**：主题管理器，负责主题的加载、切换和应用
3. **具体主题实现**：LightTheme 和 DarkTheme 等具体主题实现
4. **资源文件**：QSS样式表和JSON配置文件分离样式定义

#### 设置管理系统

1. **SettingsManager**：重构设置管理器，集中管理所有应用程序设置
2. **分层设置结构**：
   - UI设置：主题、字体、窗口状态等
   - 数据界面设置：表格显示选项等
   - 绘图设置：图表默认参数等
3. **自动持久化**：设置自动保存到用户目录的JSON文件中

### 2025.08.27

#### 调整主题设置

1. 重构部分UI界面(虽然还是很丑)
2. 优化主题切换逻辑，支持自动保存和应用

### 2025.08.28

#### 实现编辑菜单

1. 实现数据表格的复制、粘贴和删除功能
2. 实现撤销和重做栈，完善相关功能

### 2025.08.29

#### 完善工具菜单

1. 新增数据处理工具
2. 完善数据筛选功能

## 下一步的计划

- [ ] 增强绘图系统，支持更多图表类型
- [ ] 添加绘图导入/导出功能
- [ ] 实现主题编辑器，支持可视化定制
- [ ] 添加高对比度主题，提升可访问性
- [ ] 支持系统主题同步（跟随操作系统主题切换）
- [ ] 添加主题预览功能
- [ ] 实现设置项的版本管理，支持设置迁移

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进V-Plotter。

## 许可证

此项目使用MIT许可证 - 查看LICENSE文件了解详情。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交GitHub Issue
- 发送电子邮件至项目维护者

---

感谢看到这里~ V-Plotter只是一个简易项目，希望你能喜欢。
