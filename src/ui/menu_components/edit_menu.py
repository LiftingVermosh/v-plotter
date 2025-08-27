# src/ui/menu_components/edit_menu.py
# 这个文件是编辑菜单的实现文件，负责实现编辑菜单的功能，包括撤销、重做、剪切、复制、粘贴、删除、查找、替换等功能。

from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QKeySequence
from src.core.signals import edit_signals

find_requested = edit_signals.find_requested
replace_requested = edit_signals.replace_requested
replace_all_requested = edit_signals.replace_all_requested

class EditMenu(QMenu):
    def __init__(self, parent=None, main_window = None):
        super().__init__("&编辑", parent)
        self.main_window = main_window
        
        # 编辑操作
        self.undo_action = self.addAction("&撤销", QKeySequence("Ctrl+Z"))
        self.redo_action = self.addAction("&重做", QKeySequence("Ctrl+Y"))
        self.addSeparator()
        
        # 剪贴板操作
        self.cut_action = self.addAction("&剪切", QKeySequence("Ctrl+X"))
        self.copy_action = self.addAction("&复制", QKeySequence("Ctrl+C"))
        self.paste_action = self.addAction("&粘贴", QKeySequence("Ctrl+V"))
        self.delete_action = self.addAction("&删除")
        self.addSeparator()
        
        # 查找操作
        self.find_action = self.addAction("&查找...", QKeySequence("Ctrl+F"))
        self.replace_action = self.addAction("&替换...", QKeySequence("Ctrl+H"))
        
        # 连接信号
        self.undo_action.triggered.connect(self.undo)
        self.redo_action.triggered.connect(self.redo)
        self.cut_action.triggered.connect(self.cut)
        self.copy_action.triggered.connect(self.copy)
        self.paste_action.triggered.connect(self.paste)
        self.delete_action.triggered.connect(self.delete)
        self.find_action.triggered.connect(self.find)
        self.replace_action.triggered.connect(self.replace)

        find_requested.connect(self.handle_find)
        replace_requested.connect(self.handle_replace)  
        replace_all_requested.connect(self.handle_replace_all)

        # 连接命令管理器
        if self.main_window and hasattr(self.main_window, "command_manager"):
            self.main_window.command_manager.command_executed.connect(self.update_actions)
            self.main_window.command_manager.command_undone.connect(self.update_actions)
            self.main_window.command_manager.command_redone.connect(self.update_actions)
        
        # 连接信号
        edit_signals.undo_available.connect(self.setEnabled)
        edit_signals.redo_available.connect(self.setEnabled)
    
    def update_actions(self):
        """更新撤销/重做动作状态"""
        if self.main_window and hasattr(self.main_window, "command_manager"):
            self.undo_action.setEnabled(self.main_window.command_manager.can_undo)
            self.redo_action.setEnabled(self.main_window.command_manager.can_redo)

    def undo(self):
        if self.main_window and hasattr(self.main_window, "command_manager"):
            self.main_window.command_manager.undo()

    def redo(self):
        if self.main_window and hasattr(self.main_window, "command_manager"):
            self.main_window.command_manager.redo()

    def cut(self):
        current_tab = self.main_window.get_current_tab() if self.main_window else None
        if current_tab:
            current_tab.cut_selection()

    def copy(self):
        current_tab = self.main_window.get_current_tab() if self.main_window else None
        if current_tab:
            current_tab.copy_selection()

    def paste(self):
        current_tab = self.main_window.get_current_tab() if self.main_window else None
        if current_tab:
            current_tab.paste_to_selection()

    def delete(self):
        current_tab = self.main_window.get_current_tab() if self.main_window else None
        if current_tab:
            current_tab.clear_selection()

    def find(self):
        from src.ui.dialogs.find_replace_dialogs import FindReplaceDialog   
        self.find_dialog = FindReplaceDialog(self.main_window)
        self.find_dialog.show()

    def replace(self):
        from src.ui.dialogs.find_replace_dialogs import FindReplaceDialog   
        self.replace_dialog = FindReplaceDialog(self.main_window)
        self.replace_dialog.show()
    
    def handle_find(self, text, case_sensitive, whole_word):
        current_tab = self.main_window.get_current_tab() if self.main_window else None
        if current_tab:
            current_tab.find_text(text, case_sensitive, whole_word)

    def handle_replace(self, find_text, replace_text, case_sensitive, whole_word):
        current_tab = self.main_window.plot_area.get_current_table_tab() if self.main_window else None
        if current_tab:
            current_tab.replace_text(find_text, replace_text, case_sensitive, whole_word, False)  # 单个替换

    def handle_replace_all(self, find_text, replace_text, case_sensitive, whole_word):
        current_tab = self.main_window.plot_area.get_current_table_tab() if self.main_window else None
        if current_tab:
            current_tab.replace_text(find_text, replace_text, case_sensitive, whole_word, True)  # 全部替换
