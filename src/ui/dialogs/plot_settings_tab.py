# src/ui/dialogs/plot_settings_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QDoubleSpinBox, QSpinBox, QLabel, QComboBox, QColorDialog, QPushButton, QHBoxLayout, QFontComboBox
from PyQt6.QtGui import QColor, QFontDatabase, QFont
from PyQt6.QtCore import Qt
from matplotlib import font_manager as fm

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

        # 字体设置组
        font_group = QGroupBox("字体设置")
        font_layout = QVBoxLayout()
        
        # 字体族
        font_family_row = QHBoxLayout()
        font_family_row.addWidget(QLabel("字体族:"))
        self.font_family = QFontComboBox()
        
        # 设置默认字体为系统中支持中文的字体
        available_fonts = set(f.name for f in fm.fontManager.ttflist)
        chinese_fonts = [f for f in available_fonts if self.is_chinese_font(f)]
        if chinese_fonts:
            # 修复：使用 findText 和 setCurrentIndex 而不是 setCurrentFont
            index = self.font_family.findText(chinese_fonts[0])
            if index >= 0:
                self.font_family.setCurrentIndex(index)
        
        font_family_row.addWidget(self.font_family)
        font_family_row.addStretch()
        font_layout.addLayout(font_family_row)
        
        # 坐标轴标签字体大小
        label_size_row = QHBoxLayout()
        label_size_row.addWidget(QLabel("坐标轴标签字体大小:"))
        self.label_size = QSpinBox()
        self.label_size.setRange(8, 30)
        self.label_size.setValue(12)
        label_size_row.addWidget(self.label_size)
        label_size_row.addStretch()
        font_layout.addLayout(label_size_row)
        
        # 坐标轴刻度字体大小
        tick_size_row = QHBoxLayout()
        tick_size_row.addWidget(QLabel("坐标轴刻度字体大小:"))
        self.tick_size = QSpinBox()
        self.tick_size.setRange(8, 30)
        self.tick_size.setValue(10)
        tick_size_row.addWidget(self.tick_size)
        tick_size_row.addStretch()
        font_layout.addLayout(tick_size_row)
        
        # 坐标轴标题字体大小
        title_size_row = QHBoxLayout()
        title_size_row.addWidget(QLabel("坐标轴标题字体大小:"))
        self.title_size = QSpinBox()
        self.title_size.setRange(8, 30)
        self.title_size.setValue(14)
        title_size_row.addWidget(self.title_size)
        title_size_row.addStretch()
        font_layout.addLayout(title_size_row)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)

        # 绘图对象设置组
        object_group = QGroupBox("绘图对象设置")
        object_layout = QVBoxLayout()
        
        # 线宽
        line_width_row = QHBoxLayout()
        line_width_row.addWidget(QLabel("线宽:"))
        self.line_width = QDoubleSpinBox()
        self.line_width.setRange(0.1, 10.0)
        self.line_width.setSingleStep(0.1)
        self.line_width.setValue(2.0)
        self.line_width.setDecimals(1)
        line_width_row.addWidget(self.line_width)
        line_width_row.addStretch()
        object_layout.addLayout(line_width_row)

        # 边框宽度
        border_width_row = QHBoxLayout()
        border_width_row.addWidget(QLabel("边框宽度:"))
        self.border_width = QDoubleSpinBox()
        self.border_width.setRange(0.1, 10.0)
        self.border_width.setSingleStep(0.1)
        self.border_width.setValue(1.0)
        self.border_width.setDecimals(1)
        border_width_row.addWidget(self.border_width)
        border_width_row.addStretch()
        object_layout.addLayout(border_width_row)   

        # 标记点大小
        marker_size_row = QHBoxLayout()
        marker_size_row.addWidget(QLabel("标记点大小:"))
        self.marker_size = QDoubleSpinBox()
        self.marker_size.setRange(0.1, 10.0)
        self.marker_size.setSingleStep(0.1)
        self.marker_size.setValue(5.0)
        self.marker_size.setDecimals(1)
        marker_size_row.addWidget(self.marker_size)
        marker_size_row.addStretch()
        object_layout.addLayout(marker_size_row)

        object_group.setLayout(object_layout)
        layout.addWidget(object_group)

        layout.addStretch()
        
    def is_chinese_font(self, font_name):
        """检查字体是否支持中文"""
        # 常见中文字体关键词
        chinese_keywords = ['sim', 'ms', 'pingfang', 'hiragino', 'noto', 'st', '华文', '宋体', '黑体', '楷体', '仿宋']
        return any(keyword.lower() in font_name.lower() for keyword in chinese_keywords)
        
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
            "font_family": self.font_family.currentText(),  # 获取当前选中的字体名称
            "label_size": self.label_size.value(),
            "tick_size": self.tick_size.value(),
            "title_size": self.title_size.value(),
            "line_width": self.line_width.value(),
            "border_width": self.border_width.value(),
            "marker_size": self.marker_size.value()
        }

    def load_settings(self, settings):
        """加载绘图设置"""
        # 设置默认图表类型
        default_chart_type = settings.get("default_chart_type", "折线图")
        index = self.default_chart_type.findText(default_chart_type)
        if index >= 0:
            self.default_chart_type.setCurrentIndex(index)
        
        # 设置默认颜色主题
        default_theme = settings.get("default_theme", "默认")
        index = self.default_theme.findText(default_theme)
        if index >= 0:
            self.default_theme.setCurrentIndex(index)
        
        # 设置默认尺寸
        self.default_width.setValue(settings.get("default_width", 800))
        self.default_height.setValue(settings.get("default_height", 600))
        
        # 设置颜色
        bg_color = settings.get("bg_color", "#ffffff")
        self.bg_color = QColor(bg_color)
        self.update_color_button(self.bg_color_btn, self.bg_color)
        
        grid_color = settings.get("grid_color", "#c8c8c8")
        self.grid_color = QColor(grid_color)
        self.update_color_button(self.grid_color_btn, self.grid_color)
        
        # 设置字体
        font_family = settings.get("font_family", "")
        if font_family:
            # 修复：使用 findText 和 setCurrentIndex 而不是 setCurrentFont
            index = self.font_family.findText(font_family)
            if index >= 0:
                self.font_family.setCurrentIndex(index)
        
        # 设置绘图对象参数
        self.label_size.setValue(settings.get("label_size", 12))
        self.tick_size.setValue(settings.get("tick_size", 10))
        self.title_size.setValue(settings.get("title_size", 14))
        
        # 设置浮点数参数
        self.line_width.setValue(float(settings.get("line_width", 2.0)))
        self.border_width.setValue(float(settings.get("border_width", 1.0)))
        self.marker_size.setValue(float(settings.get("marker_size", 5.0)))
