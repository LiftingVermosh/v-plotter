# src/ui/menu_components/help_menu.py
# 这个文件是帮助菜单的实现。

from PyQt6.QtWidgets import QMenu

class HelpMenu(QMenu):
    def __init__(self, parent=None, main_window = None):
        super().__init__("&帮助", parent)
        self.main_window = main_window
        
        # 帮助资源
        self.documentation_action = self.addAction("&文档")
        self.tutorials_action = self.addAction("&教程")
        self.addSeparator()
        
        # 支持
        self.support_action = self.addAction("&支持...")
        self.feedback_action = self.addAction("&反馈")
        self.addSeparator()
        
        # 关于
        self.check_updates_action = self.addAction("检查更新")
        self.about_action = self.addAction("&关于...")
        
        # 连接信号
        self.documentation_action.triggered.connect(self.open_documentation)
        self.tutorials_action.triggered.connect(self.open_tutorials)
        self.support_action.triggered.connect(self.open_support)
        self.feedback_action.triggered.connect(self.send_feedback)
        self.check_updates_action.triggered.connect(self.check_updates)
        self.about_action.triggered.connect(self.show_about)

    def open_documentation(self):
        pass

    def open_tutorials(self):
        pass

    def open_support(self):
        pass

    def send_feedback(self):
        pass

    def check_updates(self):
        pass

    def show_about(self):
        pass
