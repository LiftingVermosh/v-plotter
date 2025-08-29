# src/ui/dialogs/filter_dialogs.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QComboBox, QGroupBox, QLabel, QLineEdit, QMessageBox,
                             QSpinBox, QDoubleSpinBox, QDateEdit, QCheckBox, QWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QDoubleValidator, QIntValidator

class FilterDialog(QDialog):
    def __init__(self, data_container, parent=None):
        super().__init__(parent)        
        self.data_container = data_container    # 数据容器
        self.current_column = None             # 当前选择的列
        self.current_column_type = None        # 当前选择的列的类型
        self.current_operator = None           # 当前选择的运算符
        self.current_value = None              # 当前输入的值
        self.value_widget = None               # 动态值输入控件
        
        # 检查数据容器是否有效
        if self.data_container is None or not hasattr(self.data_container, 'get_table_headers'):
            QMessageBox.critical(self, "错误", "无效的数据容器！")
            self.reject()  # 直接关闭对话框
            return
            
        column_names = self.data_container.get_table_headers()

        if not column_names or len(column_names) == 0:
            QMessageBox.warning(self, "警告", "数据表中没有可用的列！")
            self.reject()  # 直接关闭对话框
            return
        
        # 如果数据有效，初始化UI
        self.init_ui()
        self.load_column_data(column_names)

    def init_ui(self):
        # 窗口设置
        self.setWindowTitle("数据过滤器")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setMinimumSize(400, 300)
        
        # 主布局
        main_layout = QVBoxLayout()
    
        # 列选择组
        column_group = QGroupBox("选择列")
        column_layout = QVBoxLayout()
        self.column_combo = QComboBox()
        self.column_combo.currentIndexChanged.connect(self.on_column_changed)
        column_layout.addWidget(QLabel("选择要过滤的列："))
        column_layout.addWidget(self.column_combo)
        column_group.setLayout(column_layout)
        main_layout.addWidget(column_group)

        # 运算符选择组
        operator_group = QGroupBox("过滤条件")
        operator_layout = QVBoxLayout()
        self.operator_combo = QComboBox()
        self.operator_combo.currentIndexChanged.connect(self.on_operator_changed)
        operator_layout.addWidget(QLabel("选择过滤条件："))
        operator_layout.addWidget(self.operator_combo)
        operator_group.setLayout(operator_layout)
        main_layout.addWidget(operator_group)

        # 值输入组 (动态创建)
        self.value_group = QGroupBox("过滤值")
        self.value_layout = QVBoxLayout()
        self.value_group.setLayout(self.value_layout)
        main_layout.addWidget(self.value_group)

        # 选项组
        options_group = QGroupBox("选项")
        options_layout = QVBoxLayout()
        self.case_sensitive_check = QCheckBox("区分大小写")
        self.case_sensitive_check.setChecked(False)
        options_layout.addWidget(self.case_sensitive_check)
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # 按钮组
        button_layout = QHBoxLayout()
        self.filter_button = QPushButton("应用过滤")
        self.filter_button.clicked.connect(self.on_filter_clicked)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.filter_button)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def load_column_data(self, column_names):
        """加载列数据并初始化UI"""
        self.column_combo.addItems(column_names)
        
        # 默认选择第一列
        if column_names:
            self.on_column_changed(0)

    def on_column_changed(self, index):
        """当选择的列改变时更新UI"""
        if index < 0:
            return
            
        column_name = self.column_combo.itemText(index)
        self.current_column = column_name
        
        # 获取列的数据类型
        column_type = self.data_container.get_column_type(column_name)
        self.current_column_type = column_type
        
        # 更新运算符选项
        self.update_operator_options(column_type)
        
        # 更新值输入控件
        self.update_value_input(column_type)
        
        # 更新区分大小写选项的可见性
        self.update_case_sensitive_visibility(column_type)

    def update_operator_options(self, column_type):
        """根据列类型更新运算符选项"""
        # 阻塞信号，避免触发on_operator_changed
        self.operator_combo.blockSignals(True)
        
        self.operator_combo.clear()
        operators = self.get_operators_for_type(column_type)
        self.operator_combo.addItems(operators)
        
        # 取消阻塞信号
        self.operator_combo.blockSignals(False)
        
        # 如果有运算符，选择第一个并触发更新
        if operators:
            self.operator_combo.setCurrentIndex(0)
            self.on_operator_changed(0)

    def get_operators_for_type(self, column_type):
        """根据列类型返回可用的运算符"""
        if column_type in ["int", "float"]:
            return ["等于", "不等于", "大于", "小于", "大于等于", "小于等于", "为空", "不为空"]
        elif column_type == "str":
            return ["等于", "不等于", "包含", "不包含", "开头为", "结尾为", "为空", "不为空"]
        elif column_type == "date":
            return ["等于", "不等于", "早于", "晚于", "早于或等于", "晚于或等于", "为空", "不为空"]
        elif column_type == "bool":
            return ["等于", "不等于"]
        else:
            return ["等于", "不等于", "为空", "不为空"]

    def update_value_input(self, column_type):
        """根据列类型更新值输入控件"""
        # 清除现有控件
        while self.value_layout.count():
            child = self.value_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # 创建占位符widget，避免布局问题
        placeholder = QWidget()
        self.value_layout.addWidget(placeholder)
        
        # 根据列类型创建相应的值输入控件
        if column_type in ["int", "float"]:
            if column_type == "int":
                self.value_widget = QSpinBox()
                self.value_widget.setRange(-999999, 999999)
                self.value_widget.setValue(0)  # 设置默认值
            else:
                self.value_widget = QDoubleSpinBox()
                self.value_widget.setRange(-999999.99, 999999.99)
                self.value_widget.setDecimals(2)
                self.value_widget.setValue(0.0)  # 设置默认值
        elif column_type == "date":
            self.value_widget = QDateEdit()
            self.value_widget.setDate(QDate.currentDate())
            self.value_widget.setCalendarPopup(True)
        elif column_type == "bool":
            self.value_widget = QComboBox()
            self.value_widget.addItems(["True", "False"])
            self.value_widget.setCurrentIndex(0)  # 设置默认值
        else:  # 字符串和其他类型
            self.value_widget = QLineEdit()
            self.value_widget.setPlaceholderText("输入过滤值")  # 设置占位符文本
        
        # 移除占位符widget
        self.value_layout.removeWidget(placeholder)
        placeholder.deleteLater()
        
        # 添加标签和控件到布局
        self.value_layout.addWidget(QLabel("输入过滤值："))
        self.value_layout.addWidget(self.value_widget)

    def update_case_sensitive_visibility(self, column_type):
        """根据列类型更新区分大小写选项的可见性"""
        # 只有字符串类型需要区分大小写
        if column_type == "str":
            self.case_sensitive_check.setVisible(True)
        else:
            self.case_sensitive_check.setVisible(False)
            self.case_sensitive_check.setChecked(False)  # 重置为不区分大小写

    def on_operator_changed(self, index):
        """当运算符改变时更新UI"""
        if index < 0:
            return
            
        self.current_operator = self.operator_combo.itemText(index)
        
        # 如果选择的是"为空"或"不为空"，禁用值输入
        if self.current_operator in ["为空", "不为空"]:
            if self.value_widget:
                self.value_widget.setEnabled(False)
        else:
            if self.value_widget:
                self.value_widget.setEnabled(True)

    def on_filter_clicked(self):
        """应用过滤条件"""
        # 获取当前选择的列
        column_index = self.column_combo.currentIndex()
        if column_index < 0:
            QMessageBox.warning(self, "警告", "请选择要过滤的列！")
            return
            
        column_name = self.column_combo.itemText(column_index)
        
        # 获取当前选择的运算符
        operator_index = self.operator_combo.currentIndex()
        if operator_index < 0:
            QMessageBox.warning(self, "警告", "请选择过滤条件！")
            return
            
        operator = self.operator_combo.itemText(operator_index)
        
        # 获取输入的值（如果运算符不需要值，则为None）
        value = None
        if operator not in ["为空", "不为空"]:
            if not self.value_widget:
                QMessageBox.warning(self, "警告", "值输入控件未初始化！")
                return
                
            if isinstance(self.value_widget, (QSpinBox, QDoubleSpinBox)):
                value = self.value_widget.value()
            elif isinstance(self.value_widget, QDateEdit):
                value = self.value_widget.date().toString("yyyy-MM-dd")
            elif isinstance(self.value_widget, QComboBox):
                value = self.value_widget.currentText()
                # 对于布尔值，转换为Python布尔类型
                if self.current_column_type == "bool":
                    value = value.lower() == "true"
            elif isinstance(self.value_widget, QLineEdit):
                value = self.value_widget.text().strip()
                if not value:
                    QMessageBox.warning(self, "警告", "请输入过滤值！")
                    return
        
        # 获取是否区分大小写
        case_sensitive = self.case_sensitive_check.isChecked() if self.case_sensitive_check.isVisible() else False
        
        # 创建过滤条件对象
        filter_condition = {
            "column": column_name,
            "operator": operator,
            "value": value,
            "case_sensitive": case_sensitive
        }
        
        # 应用过滤
        try:
            # 假设数据容器有一个apply_filter方法
            success = self.data_container.apply_filter(filter_condition)
            if success:
                self.accept()  # 关闭对话框并返回成功
            else:
                QMessageBox.warning(self, "警告", "过滤应用失败！")
        except Exception as e:
            # 这里处理从 DataContainer 抛出的异常
            QMessageBox.critical(self, "错误", f"过滤过程中发生错误：{str(e)}")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    # 模拟数据容器用于测试
    class MockDataContainer:
        def get_table_headers(self):
            return ["ID", "Name", "Age", "Salary", "JoinDate", "Active"]
            
        def get_column_type(self, column_name):
            types = {
                "ID": "int",
                "Name": "str",
                "Age": "int",
                "Salary": "float",
                "JoinDate": "date",
                "Active": "bool"
            }
            return types.get(column_name, "str")
            
        def apply_filter(self, condition):
            print(f"Applying filter: {condition}")
            return True
    
    app = QApplication(sys.argv)
    data_container = MockDataContainer()
    dialog = FilterDialog(data_container=data_container)
    
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print("Filter applied successfully")
    else:
        print("Filter dialog cancelled")
    
    sys.exit(app.exec())
