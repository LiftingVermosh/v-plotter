# src/core/themes/dark_theme.py
from ..base_theme import BaseTheme
from PyQt6.QtGui import QColor, QFont, QIcon, QPalette
from PyQt6.QtWidgets import QApplication, QWidget

class DarkTheme(BaseTheme):
    """深色主题实现"""
    
    def __init__(self):
        super().__init__("Dark")
        # 深色主题的颜色定义
        self.colors = {
            "primary": QColor("#007acc"),
            "secondary": QColor("#6c757d"),
            "background": QColor("#1e1e1e"),
            "foreground": QColor("#f2f2f2"),
        }
        self.fonts = {
            "default": QFont("Segoe UI", 10),
            "title": QFont("Segoe UI", 12, QFont.Weight.Bold),
        }
    
    def get_stylesheet(self) -> str:
        return self.stylesheet
    
    def get_color(self, role: str) -> QColor:
        return self.colors.get(role, QColor("#000000"))
    
    def get_font(self, role: str) -> QFont:
        return self.fonts.get(role, QFont())
    
    def get_icon(self, name: str) -> QIcon:
        icon_path = self.resources_path / "icons" / f"{name}.svg"
        if icon_path.exists():
            return QIcon(str(icon_path))
        return QIcon()
    
    def apply_to_app(self, app):
        """应用主题到整个应用程序"""
        # 设置样式表
        app.setStyleSheet(self.stylesheet)
        
        # 设置字体
        app.setFont(self.get_font("default"))
        
        # 强制更新菜单栏
        for widget in app.topLevelWidgets():
            if hasattr(widget, 'menuBar') and widget.menuBar():
                self.apply_to_menu_bar(widget.menuBar())
        
        # 强制更新所有窗口
        for widget in app.topLevelWidgets():
            self.apply_to_widget(widget)

    def apply_to_menu_bar(self, menu_bar):
        """特别处理菜单栏"""
        # 设置菜单栏样式表
        menu_bar.setStyleSheet(self.stylesheet)

        # 强制更新菜单栏
        menu_bar.style().unpolish(menu_bar)
        menu_bar.style().polish(menu_bar)
        menu_bar.update()


    def apply_to_widget(self, widget):
        """将主题应用到特定部件及其所有子部件"""
        # 强制更新部件
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()