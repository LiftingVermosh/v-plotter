# src/ui/core_components/right_down_zone_property_panel.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, 
    QLineEdit, QComboBox, QPushButton, QStackedWidget,
    QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from src.core.signals import component_signals

class PropertyPanel(QWidget):
    def __init__(self, parent=None, plot_area=None):
        super().__init__(parent)
        self.main_window = parent
        self.plot_area = plot_area  # 引用PlotArea
        self.current_container = None
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 使用堆叠窗口管理不同视图的属性面板
        self.stacked_widget = QStackedWidget()
        
        # 1. 表格视图属性面板
        self.table_properties_panel = self.create_table_properties_panel()
        self.stacked_widget.addWidget(self.table_properties_panel)
        
        # 2. 绘图视图属性面板
        self.plot_properties_panel = self.create_plot_properties_panel()
        self.stacked_widget.addWidget(self.plot_properties_panel)
        
        layout.addWidget(self.stacked_widget)
        layout.addStretch()
        
        # 初始显示表格视图属性
        self.show_table_properties()

    """创建表格视图下的属性面板"""
    def create_table_properties_panel(self):
        """创建表格视图下的属性面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # # 数据集属性组
        # dataset_group = QGroupBox("数据集属性")
        # dataset_layout = QFormLayout()
        
        # self.dataset_name = QLineEdit()
        # self.dataset_name.textEdited.connect(self.on_table_property_changed)
        # dataset_layout.addRow("名称:", self.dataset_name)
        
        # self.dataset_source = QLineEdit()
        # self.dataset_source.setReadOnly(True)
        # dataset_layout.addRow("来源:", self.dataset_source)
        
        # self.row_count_label = QLabel("0")
        # dataset_layout.addRow("行数:", self.row_count_label)
        
        # self.column_count_label = QLabel("0")
        # dataset_layout.addRow("列数:", self.column_count_label)
        
        # dataset_group.setLayout(dataset_layout)
        
        # # 数据列属性组
        # column_group = QGroupBox("列属性")
        # column_layout = QFormLayout()
        
        # self.column_name = QLineEdit()
        # self.column_name.textEdited.connect(self.on_table_property_changed)
        # column_layout.addRow("列名:", self.column_name)
        
        # self.column_type = QComboBox()
        # self.column_type.addItems(["数值", "文本", "日期", "布尔"])
        # self.column_type.currentIndexChanged.connect(self.on_table_property_changed)
        # column_layout.addRow("类型:", self.column_type)
        
        # column_group.setLayout(column_layout)
        
        # layout.addWidget(dataset_group)
        # layout.addWidget(column_group)
        return panel
    
    """创建绘图视图下的属性面板"""
    def create_plot_properties_panel(self):
        """创建绘图视图下的属性面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # # 图表整体属性
        # chart_group = QGroupBox("图表属性")
        # chart_layout = QFormLayout()
        
        # self.chart_title = QLineEdit()
        # self.chart_title.textEdited.connect(self.on_plot_property_changed)
        # chart_layout.addRow("标题:", self.chart_title)
        
        # self.chart_type = QComboBox()
        # self.chart_type.addItems(["折线图", "柱状图", "散点图", "饼图"])
        # self.chart_type.currentIndexChanged.connect(self.on_plot_property_changed)
        # chart_layout.addRow("类型:", self.chart_type)
        
        # self.x_axis_label = QLineEdit()
        # self.x_axis_label.textEdited.connect(self.on_plot_property_changed)
        # chart_layout.addRow("X轴标签:", self.x_axis_label)
        
        # self.y_axis_label = QLineEdit()
        # self.y_axis_label.textEdited.connect(self.on_plot_property_changed)
        # chart_layout.addRow("Y轴标签:", self.y_axis_label)
        
        # chart_group.setLayout(chart_layout)
        
        # # 数据系列属性
        # series_group = QGroupBox("数据系列属性")
        # series_layout = QFormLayout()
        
        # self.series_name = QComboBox()
        # self.series_name.currentIndexChanged.connect(self.on_series_selected)
        # series_layout.addRow("系列:", self.series_name)
        
        # self.series_color = QPushButton("选择颜色")
        # self.series_color.clicked.connect(self.on_series_color_changed)
        # series_layout.addRow("颜色:", self.series_color)
        
        # self.series_style = QComboBox()
        # self.series_style.addItems(["实线", "虚线", "点线", "点划线"])
        # self.series_style.currentIndexChanged.connect(self.on_plot_property_changed)
        # series_layout.addRow("线型:", self.series_style)
        
        # self.marker_style = QComboBox()
        # self.marker_style.addItems(["无", "圆形", "方形", "三角形"])
        # self.marker_style.currentIndexChanged.connect(self.on_plot_property_changed)
        # series_layout.addRow("标记:", self.marker_style)
        
        # series_group.setLayout(series_layout)
        
        # layout.addWidget(chart_group)
        # layout.addWidget(series_group)
        return panel
    
    def connect_signals(self):
        """连接信号"""
        # 全局信号
        # component_signals.container_updated.connect(self.on_container_updated)
        # component_signals.properties_updated.connect(self.on_properties_updated)

    
    def on_container_updated(self, container):
        """更新属性面板显示"""
        self.current_container = container
        if container:
            # 根据当前视图更新属性
            if self.stacked_widget.currentIndex() == 0:  # 表格视图
                self.update_table_properties(container)
            else:  # 绘图视图
                self.update_plot_properties(container)
    
    def on_plot_view_changed(self, view_type):
        """当绘图区域视图切换时更新属性面板"""
        if view_type == "表格视图":
            self.show_table_properties()
            if self.current_container:
                self.update_table_properties(self.current_container)
        elif view_type == "绘图视图":
            self.show_plot_properties()
            if self.current_container:
                self.update_plot_properties(self.current_container)
    
    def show_table_properties(self):
        """显示表格视图属性"""
        self.stacked_widget.setCurrentIndex(0)
    
    def show_plot_properties(self):
        """显示绘图视图属性"""
        self.stacked_widget.setCurrentIndex(1)
    
    def update_table_properties(self, container):
        """更新表格视图属性"""
        # 数据集属性
        self.dataset_name.setText(container.get('name', '未命名'))
        self.dataset_source.setText(container.get('source', '未知'))
        
        # 数据统计
        data = container.get('data', [])
        self.row_count_label.setText(str(len(data)))
        if data:
            self.column_count_label.setText(str(len(data[0])))
        else:
            self.column_count_label.setText("0")
        
        # 默认显示第一列的属性
        if data and len(data) > 0:
            headers = list(data[0].keys())
            if headers:
                self.column_name.setText(headers[0])
                # TODO: 根据实际数据类型设置
                self.column_type.setCurrentText("数值")
    
    def update_plot_properties(self, container):
        """更新绘图视图属性"""
        # 图表整体属性
        plot_config = container.get('plot_config', {})
        self.chart_title.setText(plot_config.get('title', '图表'))
        self.chart_type.setCurrentText(plot_config.get('type', '折线图'))
        self.x_axis_label.setText(plot_config.get('x_label', 'X轴'))
        self.y_axis_label.setText(plot_config.get('y_label', 'Y轴'))
        
        # 数据系列属性
        series = container.get('series', [])
        self.series_name.clear()
        for s in series:
            self.series_name.addItem(s.get('name', '未命名'))
        
        if series:
            self.series_name.setCurrentIndex(0)
            self.on_series_selected(0)
    
    def on_series_selected(self, index):
        """当选择不同数据系列时更新属性"""
        if not self.current_container:
            return
            
        series = self.current_container.get('series', [])
        if 0 <= index < len(series):
            series_data = series[index]
            # 更新系列样式属性
            self.series_style.setCurrentText(series_data.get('line_style', '实线'))
            self.marker_style.setCurrentText(series_data.get('marker', '无'))
            # TODO: 更新颜色按钮显示
    
    def on_series_color_changed(self):
        """选择系列颜色"""
        # TODO: 实现颜色选择对话框
        pass
    
    def on_table_property_changed(self):
        """表格属性变化时发出信号"""
        if self.current_container:
            properties = {
                'type': 'table',
                'name': self.dataset_name.text(),
                # 其他表格属性...
            }
            component_signals.properties_updated.emit(properties)
    
    def on_plot_property_changed(self):
        """绘图属性变化时发出信号"""
        if self.current_container:
            properties = {
                'type': 'plot',
                'title': self.chart_title.text(),
                'chart_type': self.chart_type.currentText(),
                'x_label': self.x_axis_label.text(),
                'y_label': self.y_axis_label.text(),
                'line_style': self.series_style.currentText(),
                'marker': self.marker_style.currentText(),
            }
            component_signals.properties_updated.emit(properties)
