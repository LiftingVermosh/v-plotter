# src/ui/dialogs/data_convert_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel, QGroupBox, QGridLayout, QSpinBox, QDoubleSpinBox, QCheckBox, QMessageBox
from PyQt6.QtCore import Qt

class DataConvertDialog(QDialog):
    def __init__(self, container=None, parent=None):
        super().__init__(parent)

        if not container:
            self.hasError = True
            QMessageBox.warning(self, '错误', '请先打开一个表格文件！')
            return

        self.container = container
        self.hasError = False
        self.choosed_option = ""
        self.setWindowTitle('数据转换')
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 选择列
        column_layout = QHBoxLayout()
        column_layout.addWidget(QLabel('选择列:'))
        self.column_combo = QComboBox()
        if self.container:
            headers = self.container.get_table_headers()
            self.column_combo.addItems(headers)
        column_layout.addWidget(self.column_combo)
        layout.addLayout(column_layout)
        
        # 选择转换类型
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel('转换类型:'))
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            '数据类型转换', '数据标准化', '数据离散化', '编码转换',
            '数学运算', '文本处理', '日期时间处理', '缺失值处理'
        ])
        self.type_combo.currentTextChanged.connect(self.update_options)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # 选项区域
        self.options_group = QGroupBox('转换选项')
        self.options_layout = QVBoxLayout()
        self.options_group.setLayout(self.options_layout)
        layout.addWidget(self.options_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton('确定')
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('取消')
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.update_options()
    
    def update_options(self):
        # 清除现有选项
        while self.options_layout.count():
            child = self.options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # 根据选择的转换类型添加相应选项
        conversion_type = self.type_combo.currentText()
        
        if conversion_type == '数据类型转换':
            self.choosed_option = "数据类型转换"
            self.add_data_type_options()
        elif conversion_type == '数据标准化':
            self.choosed_option = "数据标准化"
            self.add_normalization_options()
        elif conversion_type == '数据离散化':
            self.choosed_option = "数据离散化"
            self.add_discretization_options()
        elif conversion_type == '编码转换':
            self.choosed_option = "编码转换"
            self.add_encoding_options()
        elif conversion_type == '数学运算':
            self.choosed_option = '数学运算'
            self.add_math_options()
        elif conversion_type == '文本处理':
            self.choosed_option = "文本处理"
            self.add_text_options()
        elif conversion_type == '日期时间处理':
            self.choosed_option = "日期时间处理"
            self.add_datetime_options()
    
    def add_data_type_options(self):
        """ 添加数据类型转换选项 """
        self.target_type_combo = QComboBox()
        self.target_type_combo.addItems(['整数', '浮点数', '字符串', '布尔值', '日期时间'])
        self.options_layout.addWidget(QLabel('目标类型:'))
        self.options_layout.addWidget(self.target_type_combo)
        
        self.format_edit = QLineEdit()
        self.options_layout.addWidget(QLabel('格式(可选):'))
        self.options_layout.addWidget(self.format_edit)
    def add_normalization_options(self):
        """ 添加数据标准化选项 """
        self.method_combo = QComboBox()
        self.method_combo.addItems(['最小-最大缩放', 'Z-score标准化', '小数定标标准化', '对数变换'])
        self.options_layout.addWidget(QLabel('标准化方法:'))
        self.options_layout.addWidget(self.method_combo)
        
        self.min_spin = QDoubleSpinBox()
        self.min_spin.setRange(-1000000, 1000000)
        self.min_spin.setValue(0)
        self.options_layout.addWidget(QLabel('最小值:'))
        self.options_layout.addWidget(self.min_spin)
        
        self.max_spin = QDoubleSpinBox()
        self.max_spin.setRange(-1000000, 1000000)
        self.max_spin.setValue(1)
        self.options_layout.addWidget(QLabel('最大值:'))
        self.options_layout.addWidget(self.max_spin)
    
    # TODO:添加其他选项的方法...
    def get_conversion_options(self):
        """ 获取转换选项 """
        options = {'choosed_option': self.choosed_option}
        
        if self.choosed_option == "数据类型转换":
            options['column'] = self.column_combo.currentText()
            options['target_type'] = self.target_type_combo.currentText()
            options['format'] = self.format_edit.text()
            
        elif self.choosed_option == "数据标准化":
            options['column'] = self.column_combo.currentText()
            options['method'] = self.method_combo.currentText()
            options['min'] = self.min_spin.value()
            options['max'] = self.max_spin.value()
        
        return options