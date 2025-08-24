# src/ui/main_window.py

import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QSplitter, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from src.ui.menu import MenuBar
from src.ui.core_components import (
    left_zone_data_overview,
    right_up_zone_plotarea,
    right_down_zone_property_panel
)
from src.core.signals import plot_signals
from src.core.settings_manager import SettingsManager  # 导入设置管理器
from src.ui.chart_windows import ChartWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("V-Plotter")
        self.resize(1200, 800)
        
        # 数据容器管理
        self.data_containers = []
        self.current_container = None
        
        self.init_data_containers()  # 初始化数据容器

        self.init_settings_manager()  # 初始化设置管理器

        self.init_ui()  # 初始化界面
                
        # 设置全局默认背景和前景颜色
        pg.setConfigOption('background', 'w')  # 白色背景
        pg.setConfigOption('foreground', 'k')  # 黑色前景（文本、坐标轴等）
        # 连接信号
        plot_signals.chart_window_requested.connect(self.handle_chart_window_request)
        
        self.show()

    def init_ui(self):
        # 创建菜单
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 水平分割器
        main_splitter = QSplitter(Qt.Orientation.Horizontal, central_widget)
        
        # 1. 左侧数据概览区 (25%)
        self.left_overview = left_zone_data_overview.LeftZoneDataOverview(self)
        main_splitter.addWidget(self.left_overview)
        
        # 2. 右侧区域 - 垂直分割器 (75%)
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 2.1 右上表格区 (70%)
        self.plot_area = right_up_zone_plotarea.PlotArea(self)
        
        # 2.2 右下对象属性区 (30%)
        self.property_panel = right_down_zone_property_panel.PropertyPanel(
            self,
            plot_area=self.plot_area
        )
        
        right_splitter.addWidget(self.plot_area)
        right_splitter.addWidget(self.property_panel)
        
        # 设置右侧垂直分割器的比例 (70% 表格区, 30% 属性面板)
        right_splitter.setSizes([int(self.height() * 0.7), int(self.height() * 0.3)])
        
        main_splitter.addWidget(right_splitter)
        
        # 设置主水平分割器的比例 (25% 左侧, 75% 右侧)
        main_splitter.setSizes([int(self.width() * 0.25), int(self.width() * 0.75)])
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(main_splitter)
        main_layout.setContentsMargins(5, 5, 5, 5)

    def init_settings_manager(self):
        # 初始化设置管理器
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.load_settings()
        
        # 使用设置中的默认尺寸
        default_width = self.settings.get("data_interface", {}).get("default_width", 1200)
        default_height = self.settings.get("data_interface", {}).get("default_height", 800)
        self.resize(default_width, default_height)
        
    def init_data_containers(self):
        """初始化数据容器"""
        self.data_containers = []
        self.current_container = None

    def update_all_components_with_settings(self, settings):
        """使用新设置更新所有组件"""
        self.settings = settings
        
        # 更新数据界面设置
        data_interface = settings.get("data_interface", {})
        if hasattr(self, 'plot_area'):
            # 更新表格视图的设置
            pass
        
        # 可以添加其他组件的更新逻辑
        
        # 保存设置
        self.settings_manager.save_settings(settings)

    def showEvent(self, event):
        """窗口显示后调整分割器比例"""
        super().showEvent(event)
        
        # 获取窗口实际尺寸
        width = self.width()
        height = self.height()
        
        # 查找所有分割器并设置比例
        for child in self.findChildren(QSplitter):
            if child.orientation() == Qt.Orientation.Horizontal:
                # 主水平分割器：左侧20%，右侧80%
                child.setSizes([int(width * 0.2), int(width * 0.8)])
            else:
                # 右侧垂直分割器：上70%，下30%
                child.setSizes([int(height * 0.7), int(height * 0.3)])
    
    def on_container_selected(self):
        """当选择数据容器时更新视图"""
        selected_row = self.left_overview.data_list.currentRow()
        if 0 <= selected_row < len(self.data_containers):
            self.current_container = self.data_containers[selected_row]
            
            # 更新绘图区
            self.update_plot_area()
            
            # 更新属性面板
            self.update_property_panel()
    
    def update_property_panel(self):
        """更新属性面板"""
        if self.current_container:
            self.right_down_property.update_properties(self.current_container)
    
    def get_current_container(self):
        """获取当前活动的数据容器"""
        return self.current_container

    def handle_chart_window_request(self, container, chart_type, options):
        """处理图表窗口请求"""
        chart_window = ChartWindow(container, chart_type, self, options)
        chart_window.exec() 
