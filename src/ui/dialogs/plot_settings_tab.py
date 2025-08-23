# src/ui/dialogs/plot_settings_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QSpinBox, QLabel, QComboBox, QColorDialog, QPushButton, QHBoxLayout
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class PlotSettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 默认绘图设置组
        default_plot_group = QGroupBox("默认绘图设置")
        default_layout = QVBoxLayout()
        
        # 默认图表类型
        type_row = QHBoxLayout()
        type_row.addWidget(QLabel("默认图表类型:"))
        self.default_chart_type = QComboBox()
        self.default_chart_type.addItems(["折线图", "条形图", "饼图", "散点图"])
        type_row.addWidget(self.default_chart_type)
        type_row.addStretch()
        default_layout.addLayout(type_row)
        
        # 默认颜色主题
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("默认颜色主题:"))
        self.default_theme = QComboBox()
        self.default_theme.addItems(["默认", "深色", "亮色", "自定义"])
        theme_row.addWidget(self.default_theme)
        theme_row.addStretch()
        default_layout.addLayout(theme_row)
        
        # 默认图表尺寸
        size_row = QHBoxLayout()
        size_row.addWidget(QLabel("默认图表尺寸:"))
        self.default_width = QSpinBox()
        self.default_width.setRange(400, 2000)
        self.default_width.setValue(800)
        size_row.addWidget(QLabel("宽:"))
        size_row.addWidget(self.default_width)
        
        self.default_height = QSpinBox()
        self.default_height.setRange(300, 1500)
        self.default_height.setValue(600)
        size_row.addWidget(QLabel("高:"))
        size_row.addWidget(self.default_height)
        size_row.addStretch()
        default_layout.addLayout(size_row)
        
        default_plot_group.setLayout(default_layout)
        layout.addWidget(default_plot_group)
        
        # 颜色设置组
        color_group = QGroupBox("颜色设置")
        color_layout = QVBoxLayout()
        
        # 背景颜色
        bg_row = QHBoxLayout()
        bg_row.addWidget(QLabel("背景颜色:"))
        self.bg_color_btn = QPushButton()
        self.bg_color_btn.setFixedSize(50, 25)
        self.bg_color = QColor(255, 255, 255)  # 默认白色
        self.update_color_button(self.bg_color_btn, self.bg_color)
        self.bg_color_btn.clicked.connect(lambda: self.choose_color(self.bg_color_btn, "bg_color"))
        bg_row.addWidget(self.bg_color_btn)
        bg_row.addStretch()
        color_layout.addLayout(bg_row)
        
        # 网格颜色
        grid_row = QHBoxLayout()
        grid_row.addWidget(QLabel("网格颜色:"))
        self.grid_color_btn = QPushButton()
        self.grid_color_btn.setFixedSize(50, 25)
        self.grid_color = QColor(200, 200, 200)  # 默认灰色
        self.update_color_button(self.grid_color_btn, self.grid_color)
        self.grid_color_btn.clicked.connect(lambda: self.choose_color(self.grid_color_btn, "grid_color"))
        grid_row.addWidget(self.grid_color_btn)
        grid_row.addStretch()
        color_layout.addLayout(grid_row)
        
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)

        # 绘图对象设置组
        object_group = QGroupBox("绘图对象设置")
        object_layout = QVBoxLayout()
        
        # 坐标轴标签字体大小
        label_size_row = QHBoxLayout()
        label_size_row.addWidget(QLabel("坐标轴标签字体大小:"))
        self.label_size = QSpinBox()
        self.label_size.setRange(8, 30)
        self.label_size.setValue(12)
        label_size_row.addWidget(self.label_size)
        label_size_row.addStretch()
        object_layout.addLayout(label_size_row)
        
        # 坐标轴刻度字体大小
        tick_size_row = QHBoxLayout()
        tick_size_row.addWidget(QLabel("坐标轴刻度字体大小:"))
        self.tick_size = QSpinBox()
        self.tick_size.setRange(8, 30)
        self.tick_size.setValue(10)
        tick_size_row.addWidget(self.tick_size)
        tick_size_row.addStretch()
        object_layout.addLayout(tick_size_row)
        
        # 坐标轴标题字体大小
        title_size_row = QHBoxLayout()
        title_size_row.addWidget(QLabel("坐标轴标题字体大小:"))
        self.title_size = QSpinBox()
        self.title_size.setRange(8, 30)
        self.title_size.setValue(14)
        title_size_row.addWidget(self.title_size)
        title_size_row.addStretch()
        object_layout.addLayout(title_size_row)
        
        # 线宽
        line_width_row = QHBoxLayout()
        line_width_row.addWidget(QLabel("线宽:"))
        self.line_width = QSpinBox()
        self.line_width.setRange(1, 10)
        self.line_width.setValue(2)
        line_width_row.addWidget(self.line_width)
        line_width_row.addStretch()
        object_layout.addLayout(line_width_row)

        # 边框宽度
        border_width_row = QHBoxLayout()
        border_width_row.addWidget(QLabel("边框宽度:"))
        self.border_width = QSpinBox()
        self.border_width.setRange(1, 10)
        self.border_width.setValue(1)
        border_width_row.addWidget(self.border_width)
        border_width_row.addStretch()
        object_layout.addLayout(border_width_row)   

        # 标记点大小
        marker_size_row = QHBoxLayout()
        marker_size_row.addWidget(QLabel("标记点大小:"))
        self.marker_size = QSpinBox()
        self.marker_size.setRange(1, 10)
        self.marker_size.setValue(5)
        marker_size_row.addWidget(self.marker_size)
        marker_size_row.addStretch()
        object_layout.addLayout(marker_size_row)

        object_group.setLayout(object_layout)
        layout.addWidget(object_group)

        layout.addStretch()
        
    def update_color_button(self, button, color):
        """更新颜色按钮的背景色"""
        button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
        
    def choose_color(self, button, color_type):
        """选择颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            if color_type == "bg_color":
                self.bg_color = color
            elif color_type == "grid_color":
                self.grid_color = color
            self.update_color_button(button, color)
        
    def get_settings(self):
        """获取绘图设置"""
        return {
            "default_chart_type": self.default_chart_type.currentText(),
            "default_theme": self.default_theme.currentText(),
            "default_width": self.default_width.value(),
            "default_height": self.default_height.value(),
            "bg_color": self.bg_color.name(),
            "grid_color": self.grid_color.name(),
            "label_size": self.label_size.value(),
            "tick_size": self.tick_size.value(),
            "title_size": self.title_size.value(),
            "line_width": self.line_width.value(),
            "border_width": self.border_width.value(),
            "marker_size": self.marker_size.value()
        }
