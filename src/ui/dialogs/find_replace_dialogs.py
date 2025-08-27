# src/ui/dialogs/find_replace_dialogs.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QGridLayout, QLabel, QCheckBox, QWidget
from src.core.signals import edit_signals

find_requested = edit_signals.find_requested
replace_requested = edit_signals.replace_requested
replace_all_requested = edit_signals.replace_all_requested

class FindReplaceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查找和替换")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # 查找部分 - 创建一个容器部件来包含布局
        find_widget = QWidget()
        find_layout = QHBoxLayout(find_widget)
        find_label = QLabel("查找：")
        self.find_edit = QLineEdit()
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_edit)
        find_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距

        # 替换部分 - 创建一个容器部件来包含布局
        replace_widget = QWidget()
        replace_layout = QHBoxLayout(replace_widget)
        replace_label = QLabel("替换为：")
        self.replace_edit = QLineEdit()
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_edit)
        replace_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距

        # 选项
        options_widget = QWidget()
        options_layout = QGridLayout(options_widget)
        self.case_sensitive_checkbox = QCheckBox("区分大小写")
        self.whole_word_checkbox = QCheckBox("全词匹配")
        options_layout.addWidget(self.case_sensitive_checkbox, 0, 0)
        options_layout.addWidget(self.whole_word_checkbox, 0, 1)
        options_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距

        # 按钮 - 创建一个容器部件来包含布局
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        self.find_button = QPushButton("查找下一个")
        self.replace_button = QPushButton("替换")
        self.replace_all_button = QPushButton("全部替换")
        self.close_button = QPushButton("关闭")
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.replace_button)
        button_layout.addWidget(self.replace_all_button)
        button_layout.addWidget(self.close_button)
        button_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        
        # 添加部件到主布局
        layout.addWidget(find_widget)
        layout.addWidget(replace_widget)
        layout.addWidget(options_widget)
        layout.addWidget(button_widget)
        
        self.setLayout(layout)

        # 信号连接
        self.find_button.clicked.connect(self.on_find)
        self.replace_button.clicked.connect(self.on_replace)
        self.replace_all_button.clicked.connect(self.on_replace_all)
        self.close_button.clicked.connect(self.close)

    def on_find(self):
        # 参数处理
        text = self.find_edit.text()
        case_sensitive = self.case_sensitive_checkbox.isChecked()
        whole_word = self.whole_word_checkbox.isChecked()
        # 发送信号
        find_requested.emit(text, case_sensitive, whole_word)

    def on_replace(self):
        # 参数处理
        find_text = self.find_edit.text()
        replace_text = self.replace_edit.text()
        case_sensitive = self.case_sensitive_checkbox.isChecked()
        whole_word = self.whole_word_checkbox.isChecked()
        # 发送信号
        replace_requested.emit(find_text, replace_text, case_sensitive, whole_word)

    def on_replace_all(self):
        # 参数处理
        find_text = self.find_edit.text()
        replace_text = self.replace_edit.text()
        case_sensitive = self.case_sensitive_checkbox.isChecked()
        whole_word = self.whole_word_checkbox.isChecked()
        # 发送信号
        replace_all_requested.emit(find_text, replace_text, case_sensitive, whole_word)
