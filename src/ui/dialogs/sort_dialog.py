from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt

class SortDialog(QDialog):
    def __init__(self, container, parent=None):
        super().__init__(parent)

        if not container:
            QMessageBox.warning(self, '警告', '容器为空！')
            self.hasError = True
            self.close()
            return

        self.hasError = False
        self.container = container
        self.setWindowTitle('数据排序')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 选择目标列
        layout.addWidget(QLabel('选择目标列：'))
        self.column_combobox = QComboBox()
        headers =self.container.get_table_headers()

        if not headers:
            QMessageBox.warning(self, '警告', '表格中没有可用的列！')
            self.hasError = True
            self.close()
            return

        for header in headers:
            self.column_combobox.addItem(header)
        layout.addWidget(self.column_combobox)

        # 选择排序方式
        self.sort_method_label = QLabel('选择排序方式：')
        self.sort_method_combobox = QComboBox()
        self.sort_method_combobox.addItem('升序')
        self.sort_method_combobox.addItem('降序')
        layout.addWidget(self.sort_method_label)
        layout.addWidget(self.sort_method_combobox)

        # 按钮布局
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton('确定')
        self.cancel_button = QPushButton('取消')
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

    def get_sort_options(self):
        """ 获取选择后的排序选项 """
        column = self.column_combobox.currentText()
        sort_method = self.sort_method_combobox.currentText() == '升序'
        return column, sort_method