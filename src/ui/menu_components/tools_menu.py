# src/ui/menu_components/tools_menu.py
# 这个文件是工具菜单组件的实现，包括了一些工具选项和自定义工具，以及外部工具的管理。

from PyQt6.QtWidgets import QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from src.core.signals import plot_signals
from src.ui.chart_windows import ChartWindow
from src.ui.dialogs.filter_dialogs import FilterDialog
from src.ui.dialogs.preferences_dialog import PreferencesDialog

class ToolsMenu(QMenu):
    def __init__(self, parent=None, main_window=None):
        super().__init__("&工具", parent)
        self.main_window = main_window
        
        # 工具选项
        self.preferences_action = self.addAction("&偏好设置...")
        self.addSeparator()
        
        # 自定义工具
        # 绘图工具
        self.plotting_menu = self.addMenu("&绘图工具")
        self.setup_plotting_menu()
        
        # 计算器
        self.calculator_action = self.addAction("&计算器")
        self.addSeparator()
        
        # 外部工具
        self.data_process_menu = self.addMenu("&数据工具...")
        self.setup_data_process_menu()
        
        # 连接信号
        self.preferences_action.triggered.connect(self.open_preferences)
        self.calculator_action.triggered.connect(self.open_calculator)

    def setup_plotting_menu(self):
        """设置绘图工具子菜单"""
        # 柱状图
        self.bar_chart_action = QAction("&柱状图", self)
        self.bar_chart_action.triggered.connect(self.create_bar_chart)
        self.plotting_menu.addAction(self.bar_chart_action)
        
        # 折线图
        self.line_chart_action = QAction("&折线图", self)
        self.line_chart_action.triggered.connect(self.create_line_chart)
        self.plotting_menu.addAction(self.line_chart_action)
        
        # 饼图
        self.pie_chart_action = QAction("&饼图", self)
        self.pie_chart_action.triggered.connect(self.create_pie_chart)
        self.plotting_menu.addAction(self.pie_chart_action)
        
        # 分隔线
        self.plotting_menu.addSeparator()
        
        # 散点图
        self.scatter_plot_action = QAction("&散点图", self)
        self.scatter_plot_action.triggered.connect(self.create_scatter_plot)
        self.plotting_menu.addAction(self.scatter_plot_action)
        
        # 柱状图
        self.bar_chart_action = QAction("&柱状图", self)
        self.bar_chart_action.triggered.connect(self.create_bar_chart)
        self.plotting_menu.addAction(self.bar_chart_action)
        
        # 分隔线
        self.plotting_menu.addSeparator()
        
        # 更多图表选项
        self.more_charts_action = QAction("&更多图表...", self)
        self.more_charts_action.triggered.connect(self.show_more_charts)
        self.plotting_menu.addAction(self.more_charts_action)

    def setup_data_process_menu(self):
        """设置数据处理工具子菜单"""
        # 数据过滤
        self.data_filter_action = QAction("&数据过滤", self)
        self.data_filter_action.triggered.connect(self.filter_data)
        self.data_process_menu.addAction(self.data_filter_action)

        # 数据排序
        self.data_sort_action = QAction("&数据排序", self)
        self.data_sort_action.triggered.connect(self.sort_data)
        self.data_process_menu.addAction(self.data_sort_action)

        # 数据清洗
        self.data_clean_action = QAction("&数据清洗", self)
        self.data_clean_action.triggered.connect(self.clean_data)
        self.data_process_menu.addAction(self.data_clean_action)

        # 数据转换
        self.data_convert_action = QAction("&数据转换", self)
        self.data_convert_action.triggered.connect(self.convert_data)
        self.data_process_menu.addAction(self.data_convert_action)

        # 更多操作
        self.more_actions_dialogs = QAction("&更多操作...", self)
        self.addSeparator()

    def filter_data(self):
        """数据过滤"""
        # 实现数据过滤逻辑
        current_container = self.main_window.plot_area.get_current_table_container()
        fitler_dialog = FilterDialog(current_container, self.main_window)
        fitler_dialog.exec()  # 调用 exec() 方法显示对话框

    def sort_data(self):
        """数据排序"""
        # 实现数据排序逻辑
        pass

    def clean_data(self):
        """数据清洗"""
        # 实现数据清洗逻辑

    def convert_data(self):
        """数据转换"""
        # 实现数据转换逻辑
        pass

    # 偏好相关
    def open_preferences(self):
        """打开偏好设置"""
        dialog = PreferencesDialog(self.main_window)
        dialog.settings_changed.connect(self.apply_preferences)
        dialog.exec()  # 调用 exec() 方法显示对话框

    def apply_preferences(self, settings):
        """应用偏好设置"""
        
        # 更新主窗口中的设置
        if hasattr(self.main_window, 'settings'):
            self.main_window.settings = settings
        
        # 可以通知其他组件设置已更改
        if hasattr(self.main_window, 'update_all_components_with_settings'):
            self.main_window.update_all_components_with_settings(settings)
        
    def save_preferences(self, settings):
        """保存偏好设置到配置文件"""
        # 这里可以实现设置保存逻辑
        # 可以使用QSettings或其他方式保存设置
        pass

    # 计算器
    def open_calculator(self):
        """打开计算器"""
        # 实现计算器逻辑
        pass
    
    # 绘图相关
    def create_bar_chart(self):
        """创建柱状图"""
        self.request_chart('bar')
    
    def create_line_chart(self):
        """创建折线图"""
        self.request_chart('line')
    
    def create_pie_chart(self):
        """创建饼图"""
        self.request_chart('pie')

    def create_scatter_plot(self):
        """创建散点图"""
        self.request_chart('scatter')

    def request_chart(self, chart_type):
        # 获取当前激活的表格标签页的数据容器
        if hasattr(self.main_window, 'plot_area'):
            plot_area = self.main_window.plot_area
            current_table_tab = plot_area.parent_table_tab.currentWidget()
            
            if current_table_tab and hasattr(current_table_tab, 'container'):
                # 发射信号，请求创建图表窗口
                options = {
                    'title': f"{current_table_tab.container.name} - {chart_type}"
                }
                plot_signals.chart_window_requested.emit(
                    current_table_tab.container, 
                    chart_type, 
                    options
                )
            else:
                QMessageBox.warning(self.main_window, "警告", "请先打开或创建一个数据表格！")
        else:
            QMessageBox.warning(self.main_window, "警告", "绘图区域未初始化")

    def show_more_charts(self):
        """显示更多图表选项"""
        # 实现更多图表选项的逻辑
        pass
