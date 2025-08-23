# src/ui/dialogs/preferences_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QDialogButtonBox
from .data_interface_tab import DataInterfaceTab
from .plot_settings_tab import PlotSettingsTab

class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("偏好设置")
        self.resize(600, 400)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 数据界面设置标签页
        self.data_interface_tab = DataInterfaceTab()
        self.tab_widget.addTab(self.data_interface_tab, "数据界面设置")
        
        # 绘图参数设置标签页
        self.plot_settings_tab = PlotSettingsTab()
        self.tab_widget.addTab(self.plot_settings_tab, "绘图参数设置")
        
        layout.addWidget(self.tab_widget)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_layout.addWidget(button_box)
        
        layout.addLayout(button_layout)
        
    def get_settings(self):
        """获取所有设置"""
        return {
            "data_interface": self.data_interface_tab.get_settings(),
            "plot_settings": self.plot_settings_tab.get_settings()
        }
