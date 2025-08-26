# src/ui/menu_components/view_menu.py
# 这个文件是用来实现视图菜单栏的功能的，包括启用工具栏、界面主题切换等功能。

from PyQt6.QtWidgets import QMenu
from src.ui.dialogs.theme_dialog import ThemeDialog

class ViewMenu(QMenu):
    def __init__(self, parent=None, main_window = None):
        super().__init__("&视图", parent)
        self.main_window = main_window
        
        # 视图选项
        self.change_theme_action = self.addAction("主题(&T)")
        self.addSeparator()
        
        # 界面元素切换
        self.toolbar_action = self.addAction("工具栏")
        self.toolbar_action.setCheckable(True)
        self.toolbar_action.setChecked(True)
        
        self.statusbar_action = self.addAction("状态栏")
        self.statusbar_action.setCheckable(True)
        self.statusbar_action.setChecked(True)
        
        # 连接信号
        self.change_theme_action.triggered.connect(self.open_theme_dialog)
        self.toolbar_action.triggered.connect(self.toggle_toolbar)
        self.statusbar_action.triggered.connect(self.toggle_statusbar)

    def open_theme_dialog(self):
        """打开主题对话框"""
        theme_dialog = ThemeDialog(self.main_window)
        theme_dialog.exec()

    def toggle_toolbar(self):
        pass

    def toggle_statusbar(self):
        pass
