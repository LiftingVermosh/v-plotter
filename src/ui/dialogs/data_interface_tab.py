# src/ui/dialogs/data_interface_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QCheckBox, QSpinBox, QLabel, QComboBox, QHBoxLayout
from PyQt6.QtCore import Qt

class DataInterfaceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 显示设置组
        display_group = QGroupBox("显示设置")
        display_layout = QVBoxLayout()
        
        self.show_row_numbers = QCheckBox("显示行号")
        self.show_row_numbers.setChecked(True)
        display_layout.addWidget(self.show_row_numbers)
        
        self.show_grid = QCheckBox("显示网格线")
        self.show_grid.setChecked(True)
        display_layout.addWidget(self.show_grid)
        
        self.auto_resize_columns = QCheckBox("自动调整列宽")
        self.auto_resize_columns.setChecked(True)
        display_layout.addWidget(self.auto_resize_columns)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # 行为设置组
        behavior_group = QGroupBox("行为设置")
        behavior_layout = QVBoxLayout()
        
        behavior_row = QHBoxLayout()
        behavior_row.addWidget(QLabel("默认行数:"))
        self.default_row_count = QSpinBox()
        self.default_row_count.setRange(5, 100)
        self.default_row_count.setValue(10)
        behavior_row.addWidget(self.default_row_count)
        behavior_row.addStretch()
        behavior_layout.addLayout(behavior_row)
        
        behavior_row2 = QHBoxLayout()
        behavior_row2.addWidget(QLabel("默认列数:"))
        self.default_column_count = QSpinBox()
        self.default_column_count.setRange(2, 20)
        self.default_column_count.setValue(3)
        behavior_row2.addWidget(self.default_column_count)
        behavior_row2.addStretch()
        behavior_layout.addLayout(behavior_row2)
        
        behavior_row3 = QHBoxLayout()
        behavior_row3.addWidget(QLabel("默认列名格式:"))
        self.column_naming = QComboBox()
        self.column_naming.addItems(["列1, 列2, ...", "A, B, C, ...", "自定义前缀"])
        behavior_row3.addWidget(self.column_naming)
        behavior_row3.addStretch()
        behavior_layout.addLayout(behavior_row3)
        
        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)
        
        layout.addStretch()
        
    def get_settings(self):
        """获取数据界面设置"""
        return {
            "show_row_numbers": self.show_row_numbers.isChecked(),
            "show_grid": self.show_grid.isChecked(),
            "auto_resize_columns": self.auto_resize_columns.isChecked(),
            "default_row_count": self.default_row_count.value(),
            "default_column_count": self.default_column_count.value(),
            "column_naming": self.column_naming.currentText()
        }

    def load_settings(self, settings):
        """加载数据界面设置"""
        self.show_row_numbers.setChecked(settings.get("show_row_numbers", True))
        self.show_grid.setChecked(settings.get("show_grid", True))
        self.auto_resize_columns.setChecked(settings.get("auto_resize_columns", True))
        self.default_row_count.setValue(settings.get("default_row_count", 10))
        self.default_column_count.setValue(settings.get("default_column_count", 3))
        
        column_naming = settings.get("column_naming", "列1, 列2, ...")
        index = self.column_naming.findText(column_naming)
        if index >= 0:
            self.column_naming.setCurrentIndex(index)