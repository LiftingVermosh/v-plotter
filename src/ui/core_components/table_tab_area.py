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
        
        # 创建标签页实例
        self.parent_table_tab = ParentTableTab(self, self.main_window)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.parent_table_tab)
        self.setLayout(layout)
    
    def get_current_table_container(self):
        """获取当前激活的表格标签页的数据容器"""
        current_widget = self.parent_table_tab.currentWidget()
        if current_widget and hasattr(current_widget, 'container'):
            return current_widget.container
        return None
    
    def get_current_table_tab(self):
        """获取当前活动的表格标签页"""
        current_widget = self.parent_table_tab.currentWidget()
        # 确保不是欢迎页
        if current_widget != self.parent_table_tab.welcome_tab:
            return current_widget
        else:
            QMessageBox.warning(self, "警告", "请先创建或打开一个表格文件！")
            return None
    