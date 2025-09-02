from PyQt6.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel, QGridLayout, QGroupBox, QHBoxLayout, QCheckBox, QFileDialog, QDialogButtonBox

class DataCleanDialog(QDialog):
    def __init__(self, container=None, parent=None):
        super().__init__(parent)

        if not container:
            QMessageBox.warning(self, '错误', '数据容器为空，请先打开数据文件')
            self.hasError = True
            self.close()
            return

        self.hasError = False
        self.container = container
        self.setWindowTitle('数据清洗')
        self.init_ui()



    def init_ui(self):
        layout = QVBoxLayout()

        tip_label = QLabel('请选择需要清洗的数据列：')
        layout.addWidget(tip_label)

        # 下拉选择框
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
        self.column_combobox.addItem('全部')
        layout.addWidget(self.column_combobox)

        layout.addWidget(QLabel('请选择清洗设置'))
        # 设置下拉框
        self.sensitive_combobox = QComboBox()
        self.sensitive_combobox.addItem("宽松清洗: 仅清洗空字符串、'None'、'null'")
        self.sensitive_combobox.addItem('严格清洗: 包括空字符串、NaN、None等')
        layout.addWidget(self.sensitive_combobox)

        layout.addWidget(QLabel('清洗为：'))
        # 替换值输入框
        self.output_lineedit = QLineEdit()
        self.output_lineedit.setPlaceholderText('请输入替换后的值')
        layout.addWidget(self.output_lineedit)

        # 选择按钮
        button_layout = QHBoxLayout()
        self.accept_button = QPushButton('清洗')
        self.accept_button.clicked.connect(self.accept)
        button_layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton('取消')
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_clean_options(self):
        column = self.column_combobox.currentText()
        sensitive_value = self.sensitive_combobox.currentText()
        sensitive_value = True if sensitive_value == '严格清洗: 包括空字符串、NaN、None等' else False
        output_line_value = self.output_lineedit.text()
        output_value = output_line_value or "0"
        return column, sensitive_value, output_value