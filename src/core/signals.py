# src/core/signals.py
# 全局信号中心类

from PyQt6.QtCore import QObject, pyqtSignal

class ComponentSignals(QObject):
    """组件间通信的信号类"""
    container_updated = pyqtSignal(object)  # 容器更新信号 - 参数: 容器对象
    porperty_panel_changed = pyqtSignal(str)  # 属性面板改变信号 - 参数: 属性面板名称
    properties_updated = pyqtSignal(dict)    # 属性更新信号 - 参数: 属性字典
    plot_updated = pyqtSignal(dict)          # 绘图更新信号 - 参数: 绘图字典

class ContainerSignals(QObject):
    """数据容器通信的信号类"""
    container_created = pyqtSignal()        # 数据容器创建信号 - 参数: 无
    container_ready = pyqtSignal(object)    # 数据容器准备就绪信号 - 参数: 数据容器对象
    container_updated = pyqtSignal(object)  # 数据容器更新信号 - 参数: 数据容器对象
    container_deleted = pyqtSignal(object)  # 数据容器删除信号 - 参数: 数据容器对象

    _current_container = None
    
    def set_current_container(self, container):
        self._current_container = container
    
    def get_current_container(self):
        return self._current_container

class TabSignals(QObject):
    """标签页通信的信号类"""
    # 表格标签信号
    table_tab_created = pyqtSignal(str, str)  # (uuid, 名称)
    table_tab_closed = pyqtSignal(str)        # 关闭的标签页UUID
    activate_table_tab = pyqtSignal(str)      # 请求激活的表格标签页UUID

    # 缩略图标签信号
    thumbnnail_clicked = pyqtSignal(str)      # 缩略图点击信号 - 参数: 缩略图UUID
    thumbnnail_closed = pyqtSignal(str)       # 关闭的标签页UUID

class DataSignals(QObject):
    """数据通信的信号类"""
    data_modified = pyqtSignal(object, list)  # 数据修改信号 - 参数: 数据对象,列标题

class PlotSignals(QObject):
    """绘图通信的信号类"""
    chart_window_requested = pyqtSignal(object, str, dict)  # 创建窗口请求信号 - 参数：容器、图表类型、选项

class SettingsSignals(QObject):
    """设置通信的信号类"""
    settings_changed = pyqtSignal(dict)  # 设置改变信号 - 参数: 设置字典

class ThemeSignals(QObject):
    """主题相关信号类"""
    theme_changed = pyqtSignal(str)  # 主题改变信号 - 参数: 主题名称
    success_changed = pyqtSignal(bool, bool, str)  # 成功改变信号 - 参数: 成功状态、用户介入状态、主题名称

class EditSignals(QObject):
    """编辑相关信号类"""
    undo_available = pyqtSignal(bool)  # 撤销可用信号 - 参数: 是否可用
    redo_available = pyqtSignal(bool)  # 重做可用信号 - 参数: 是否可用
    find_available = pyqtSignal(bool)  # 查找可用信号 - 参数: 是否可用
    replace_available = pyqtSignal(bool)  # 替换可用信号 - 参数: 是否可用
    find_requested = pyqtSignal(str, bool, bool)        # 文本，是否区分大小写，是否全词匹配
    replace_requested = pyqtSignal(str, str, bool, bool)     # 文本, 替换文本，是否区分大小写，是否全词匹配
    replace_all_requested = pyqtSignal(str, str, bool, bool)  # 文本, 替换文本，是否区分大小写，是否全词匹配
    replace_all_finished = pyqtSignal()  # 替换全部完成信号


# 创建全局唯一实例
# 信号中心类实例
component_signals = ComponentSignals()

# 数据容器通信的信号中心类实例
container_signals = ContainerSignals()

# 标签页通信的信号中心类实例
tab_signals = TabSignals()

# 数据通信的信号中心类实例
data_signals = DataSignals()

# 绘图通信的信号中心类实例
plot_signals = PlotSignals()

# 设置通信的信号中心类实例
settings_signals = SettingsSignals()

# 主题相关信号中心类实例
theme_signals = ThemeSignals()

# 编辑相关信号中心类实例
edit_signals = EditSignals()