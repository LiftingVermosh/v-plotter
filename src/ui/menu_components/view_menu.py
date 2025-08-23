# src/ui/menu_components/view_menu.py
# 这个文件是用来实现视图菜单栏的功能的，包括缩放、界面元素切换等功能。

from PyQt6.QtWidgets import QMenu

class ViewMenu(QMenu):
    def __init__(self, parent=None, main_window = None):
        super().__init__("&视图", parent)
        self.main_window = main_window
        
        # 视图选项
        self.zoom_in_action = self.addAction("放大(&I)")
        self.zoom_out_action = self.addAction("缩小(&O)")
        self.reset_zoom_action = self.addAction("重置缩放(&R)")
        self.addSeparator()
        
        # 界面元素切换
        self.toolbar_action = self.addAction("工具栏(&T)")
        self.toolbar_action.setCheckable(True)
        self.toolbar_action.setChecked(True)
        
        self.statusbar_action = self.addAction("状态栏(&S)")
        self.statusbar_action.setCheckable(True)
        self.statusbar_action.setChecked(True)
        
        # 连接信号
        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.zoom_out_action.triggered.connect(self.zoom_out)
        self.reset_zoom_action.triggered.connect(self.reset_zoom)
        self.toolbar_action.triggered.connect(self.toggle_toolbar)
        self.statusbar_action.triggered.connect(self.toggle_statusbar)

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def reset_zoom(self):
        pass

    def toggle_toolbar(self):
        pass

    def toggle_statusbar(self):
        pass
