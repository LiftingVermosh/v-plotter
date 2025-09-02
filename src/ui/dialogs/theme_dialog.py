# src/ui/dialogs/theme_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel
from src.core.signals import theme_signals

class ThemeDialog(QDialog):
    theme_changed = theme_signals.theme_changed

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # parent应为MainWindow实例
        self.theme_manager = self.main_window.theme_manager
        self.settings_manager = self.main_window.settings_manager
        self.current_themes = self.theme_manager.get_available_themes()
        self.setWindowTitle('主题设置')
        self.init_ui()
        
        # 设置当前选中的主题
        current_theme = self.theme_manager.get_current_theme_name()
        if current_theme in self.current_themes:
            index = self.theme_combobox.findText(current_theme)
            if index >= 0:
                self.theme_combobox.setCurrentIndex(index)
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("选择主题:"))
        
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(self.current_themes)
        layout.addWidget(self.theme_combobox)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
    
    def accept(self):
        theme_name = self.theme_combobox.currentText()
        # 通过ThemeManager设置主题，标记为用户主动触发
        if self.theme_manager.set_theme(theme_name, user_initiated=True):
            super().accept()
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "错误", "主题切换失败")
    
    def reject(self):
        super().reject()
        