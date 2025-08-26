# src/ui/dialogs/preferences_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QDialogButtonBox
from src.core.signals import settings_signals
from .data_interface_tab import DataInterfaceTab
from .plot_settings_tab import PlotSettingsTab
from src.core.settings_manager import SettingsManager

class PreferencesDialog(QDialog):
    # 定义设置已更改的信号
    settings_changed = settings_signals.settings_changed
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = SettingsManager()
        self.current_settings = self.settings_manager.load_settings()
        self.setWindowTitle("偏好设置")
        self.resize(600, 400)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 数据界面设置标签页
        self.data_interface_tab = DataInterfaceTab()
        # 加载当前设置
        self.data_interface_tab.load_settings(self.current_settings.get("data_interface", {}))
        self.tab_widget.addTab(self.data_interface_tab, "数据界面设置")
        
        # 绘图参数设置标签页
        self.plot_settings_tab = PlotSettingsTab()
        # 加载当前设置
        self.plot_settings_tab.load_settings(self.current_settings.get("plot_settings", {}))
        self.tab_widget.addTab(self.plot_settings_tab, "绘图参数设置")
        
        layout.addWidget(self.tab_widget)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Apply
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_settings)
        button_layout.addWidget(button_box)
        
        layout.addLayout(button_layout)
        
    def get_settings(self):
        """获取所有设置"""
        return {
            "data_interface": self.data_interface_tab.get_settings(),
            "plot_settings": self.plot_settings_tab.get_settings()
        }
    
    def apply_settings(self):
        settings = self.get_settings()
        if self.settings_manager.save_settings(settings):
            self.settings_changed.emit(settings)
            # 应用UI设置，如字体
            self.settings_manager.apply_ui_settings(settings)
    
    def accept(self):
        self.apply_settings()
        super().accept()
