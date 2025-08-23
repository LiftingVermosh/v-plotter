# src/ui/menu.py
# This file contains the implementation of the menu bar of the application.

from PyQt6.QtWidgets import QMenuBar, QMenu
import src.ui.menu_components as menu_components

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        # 初始化菜单栏
        self.init_menu()

    def init_menu(self):
        # 创建所有菜单
        file_menu = menu_components.file_menu.FileMenu(self, self.main_window)
        edit_menu = menu_components.edit_menu.EditMenu(self, self.main_window)
        view_menu = menu_components.view_menu.ViewMenu(self, self.main_window)
        tools_menu = menu_components.tools_menu.ToolsMenu(self, self.main_window)
        help_menu = menu_components.help_menu.HelpMenu(self, self.main_window)
        
        # 添加到菜单栏
        self.addMenu(file_menu)
        self.addMenu(edit_menu)
        self.addMenu(view_menu)
        self.addMenu(tools_menu)
        self.addMenu(help_menu)
