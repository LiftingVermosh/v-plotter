# src/ui/core_components/right_up_zone_plotarea.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QMessageBox
from .parent_table_tab import ParentTableTab
from src.core.signals import component_signals, container_signals
from PyQt6.QtCore import pyqtSignal

class PlotArea(QWidget):
    view_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        
        # 在构造函数中创建实例
        self.parent_table_tab = ParentTableTab(self)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        self.top_level_tab = QTabWidget()
        
        # 使用成员变量
        self.top_level_tab.addTab(self.parent_table_tab, "表格视图")
        
        layout.addWidget(self.top_level_tab)
    
    def get_current_table_container(self):
        """获取当前激活的表格标签页的数据容器"""
        current_widget = self.parent_table_tab.currentWidget()
        if current_widget and hasattr(current_widget, 'container'):
            return current_widget.container
        return None
    