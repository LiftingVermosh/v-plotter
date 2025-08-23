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
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   │   ├── data_container.py      # 数据容器管理
│   │   ├── font_manager.py        # 字体管理
│   │   ├── settings_manager.py    # 设置管理
│   │   ├── signals.py             # 信号定义
│   │   └── plot/                  # 绘图相关模块
│   │       └── figure_config.py   # 图表配置
│   ├── ui/                # 用户界面模块
│   │   ├── core_components/       # 核心UI组件
│   │   │   ├── left_zone_data_overview.py     # 左侧数据概览区
│   │   │   ├── parent_table_tab.py            # 表格父标签页
│   │   │   ├── right_down_zone_property_panel.py  # 右下属性面板
│   │   │   ├── right_up_zone_plotarea.py      # 右上绘图区域
│   │   │   └── table_view_tab.py              # 表格视图标签页
│   │   ├── dialogs/               # 对话框组件
│   │   │   ├── data_interface_tab.py      # 数据界面设置标签页
│   │   │   ├── font_config_dialog.py      # 字体配置对话框
│   │   │   ├── plot_settings_tab.py       # 绘图参数设置标签页
│   │   │   └── preferences_dialog.py      # 偏好设置对话框
│   │   ├── menu_components/       # 菜单组件
│   │   │   ├── edit_menu.py       # 编辑菜单(未完成)
│   │   │   ├── file_menu.py       # 文件菜单(部分完成)
│   │   │   ├── help_menu.py       # 帮助菜单(未完成)
│   │   │   ├── tools_menu.py      # 工具菜单(部分完成)
│   │   │   └── view_menu.py       # 视图菜单(未完成)
│   │   ├── chart_windows.py       # 图表窗口
│   │   ├── main_window.py         # 主窗口
│   │   └── menu.py                # 菜单栏
│   └── utils/             # 工具函数
├── test/                  # 测试目录
│   └── data/              # 测试数据
├── main.py                # 应用程序入口点
├── requirements.txt       # 项目依赖
├── setup.py              # 安装脚本
└── README.md             # 项目说明文档
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

### 快捷键

- `Ctrl+O`: 打开数据表格
- `Ctrl+N`: 新建数据表格
- ==== 以下暂时失效 ====
- `Ctrl+S`: 保存数据表格
- `Ctrl+A+R`: 添加行
- `Ctrl+D+R`: 删除行
- `Ctrl+A+C`: 添加列
- `Ctrl+D+C`: 删除列
- ==== 分界线 ====
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

## 下一步的计划

- 完善菜单
- 重构图表
- 美化界面

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
