# src/ui/theme_components/styled_widgets.py
from PyQt6.QtWidgets import QPushButton, QLineEdit, QComboBox, QSlider
from PyQt6.QtCore import pyqtSignal
from src.core.theme_manager import ThemeManager

class ThemedWidget:
    """支持主题化的部件混入类"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_manager = ThemeManager.instance()  # 假设ThemeManager有单例方法
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
        self._apply_theme()
    
    def _on_theme_changed(self, theme_name):
        self._apply_theme()
    
    def _apply_theme(self):
        """应用当前主题到部件"""
        if self.theme_manager.current_theme:
            self.theme_manager.apply_theme(widget=self)

class ThemedPushButton(ThemedWidget, QPushButton):
    """支持主题化的按钮"""
    pass

class ThemedLineEdit(ThemedWidget, QLineEdit):
    """支持主题化的文本输入框"""
    pass

class ThemedComboBox(ThemedWidget, QComboBox):
    """支持主题化的下拉框"""
    pass

class ThemedSlider(ThemedWidget, QSlider):
    """支持主题化的滑块"""
    pass

# 更多预样式化组件...
