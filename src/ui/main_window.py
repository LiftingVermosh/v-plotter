# src/ui/main_window.py

import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import Qt
from src.ui.menu import MenuBar
from src.ui.core_components import (
    data_overview,
    table_tab_area
)
from src.core.signals import plot_signals, theme_signals
from src.core.settings_manager import SettingsManager
from src.core.theme_manager import ThemeManager
from src.core.command_manager import CommandManager
from src.ui.chart_windows import ChartWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("V-Plotter")
        
        self.data_containers = []
        self.current_container = None
        
        self.init_data_containers()
        self.init_managers()
        self.init_ui()
        self.restore_window_state()  # 使用SettingsManager恢复窗口状态
                
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        plot_signals.chart_window_requested.connect(self.handle_chart_window_request)
        
        QApplication.instance().processEvents()  # 处理所有 pending 事件
        self.on_theme_changed('light')  # 应用主题
        
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
        
        # 左侧数据概览区 (25%)
        self.left_overview = data_overview.LeftZoneDataOverview(main_splitter, self)
        main_splitter.addWidget(self.left_overview)
        
        # 表格区 (70%)
        self.plot_area = table_tab_area.PlotArea(self)
        
        main_splitter.addWidget(self.plot_area)
        
        # 设置主水平分割器的比例
        main_splitter.setSizes([int(self.width() * 0.25), int(self.width() * 0.75)])
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(main_splitter)
        main_layout.setContentsMargins(5, 5, 5, 5)

    def init_managers(self):
        """初始化管理器"""
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.load_settings()
        self.theme_manager = ThemeManager()
        theme_signals.theme_changed.connect(self.on_theme_changed)
        self.command_manager = CommandManager()
    
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
            
            # 更新属性面板
            self.update_property_panel()
    
    def update_property_panel(self):
        """更新属性面板"""
        if self.current_container:
            self.right_down_property.update_properties(self.current_container)
    
    def get_current_container(self):
        """获取当前活动的数据容器"""
        return self.current_container

    def get_current_tab(self):
        """获取当前活动的表格标签页"""
        return self.plot_area.get_current_table_tab()

    def get_command_manager(self):
        """获取命令管理器"""
        return self.command_manager

    def handle_chart_window_request(self, container, chart_type, options):
        """处理图表窗口请求"""
        chart_window = ChartWindow(container, chart_type, self, options)
        chart_window.exec()
 
    def restore_window_state(self):
        """恢复窗口几何信息和状态"""
        self.settings_manager.restore_window_state_and_geometry(self, default_size=(1200, 800))
     
    def closeEvent(self, event):
        """窗口关闭事件"""
        self.settings_manager.save_window_state_and_geometry(self)
        # 调用父类的关闭事件处理
        super().closeEvent(event)

    def on_theme_changed(self, theme_name):
        """主题更改时的处理"""
        # 重新应用主题到当前窗口
        app = QApplication.instance()
        self.theme_manager.apply_theme(app=app, widget=self)
