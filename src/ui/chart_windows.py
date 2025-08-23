# src/ui/chart_windows.py
# 这个文件是图表窗口的实现，主要是继承自QDialog，并使用matplotlib绘制图表。

from PyQt6.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import matplotlib

matplotlib.use('SVG')

class ChartWindow(QDialog):
    def __init__(self, container, chart_type, parent=None, options=None):
        super().__init__(parent)
        self.container = container
        self.chart_type = chart_type
        self.options = options or {}
        self.setWindowTitle(f"{chart_type} - {container.name}")
        self.resize(800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 创建图表
        self.figure = Figure(dpi=125)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        self.draw_chart()
        
    def draw_chart(self):
        # 从容器获取数据
        if self.container is None:
            return
        
        data_array = self.container.get_table_data_as_numpy()
        headers = self.container.column_headers
        
        # 确保数据是二维的
        if len(data_array.shape) == 1:
            data_array = data_array.reshape(-1, 1)
        
        # 清除旧图形
        self.figure.clear()
        
        ax = self.figure.add_subplot(111)
        
        # 根据图表类型调用不同的绘图方法
        if self.chart_type == 'bar':
            self.draw_bar_chart(ax, data_array, headers)
        elif self.chart_type == 'line':
            self.draw_line_chart(ax, data_array, headers)
        elif self.chart_type == 'pie':
            self.draw_pie_chart(ax, data_array, headers)
        elif self.chart_type == 'scatter':
            self.draw_scatter_chart(ax, data_array, headers)
        # 可以添加更多图表类型
        else:
            ax.text(0.5, 0.5, f'不支持的图表类型: {self.chart_type}', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax.transAxes)
        
        self.canvas.draw()
    
    def draw_bar_chart(self, ax, data_array, headers):
        # 绘制条形图
        if data_array.shape[1] < 2:
            ax.text(0.5, 0.5, '数据不足，至少需要两列（一列标签，一列数值）', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax.transAxes)
            return
        
        labels = data_array[:, 0]  # 第一列为标签
        values = data_array[:, 1]  # 第二列为数值
        
        try:
            values = values.astype(float)
        except ValueError:
            ax.text(0.5, 0.5, '数值列包含非数值数据', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax.transAxes)
            return
        
        x_pos = np.arange(len(labels))
        
        ax.bar(x_pos, values, antialiased=True)
        ax.plot(x_pos, values, antialiased=True)
        ax.set_xlabel(headers[0], antialiased=True)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels)
        ax.set_xlabel(headers[0] if headers else 'X')
        ax.set_ylabel(headers[1] if len(headers) > 1 else 'Y')
        ax.set_title(self.options.get('title', '条形图'))
    
    def draw_line_chart(self, ax, data_array, headers):
        # 绘制折线图
        if data_array.shape[1] < 2:
            ax.text(0.5, 0.5, '数据不足，至少需要两列（一列标签，一列数值）', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax.transAxes)
            return
        
        labels = data_array[:, 0]  # 第一列为标签
        values = data_array[:, 1]  # 第二列为数值
        
        try:
            values = values.astype(float)
        except ValueError:
            ax.text(0.5, 0.5, '数值列包含非数值数据', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax.transAxes)
            return
        
        x_pos = np.arange(len(labels))
        ax.plot(x_pos, values, marker='o')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels)
        ax.set_xlabel(headers[0] if headers else 'X')
        ax.set_ylabel(headers[1] if len(headers) > 1 else 'Y')
        ax.set_title(self.options.get('title', '折线图'))
    
    def draw_pie_chart(self, ax, data_array, headers):
        # 绘制饼图
        if data_array.shape[1] < 2:
            ax.text(0.5, 0.5, '数据不足，至少需要两列（一列标签，一列数值）', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax.transAxes)
            return
        
        labels = data_array[:, 0]  # 第一列为标签
        values = data_array[:, 1]  # 第二列为数值
        
        try:
            values = values.astype(float)
        except ValueError:
            ax.text(0.5, 0.5, '数值列包含非数值数据', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax.transAxes)
            return
        
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title(self.options.get('title', '饼图'))
    
    def draw_scatter_chart(self, ax, data_array, headers):
        # 绘制散点图
        if data_array.shape[1] < 3:
            ax.text(0.5, 0.5, '数据不足，至少需要三列（两列数值，一列标签）', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax.transAxes)
            return
        
        x_values = data_array[:, 1]  # 第二列为X值
        y_values = data_array[:, 2]  # 第三列为Y值
        labels = data_array[:, 0]   # 第一列为标签
        
        try:
            x_values = x_values.astype(float)
            y_values = y_values.astype(float)
        except ValueError:
            ax.text(0.5, 0.5, '数值列包含非数值数据', 
                    horizontalalignment='center', 
                    verticalalignment='center',
                    transform=ax.transAxes)
            return
        
        ax.scatter(x_values, y_values)
        ax.set_xlabel(headers[1] if len(headers) > 1 else 'X')
        ax.set_ylabel(headers[2] if len(headers) > 2 else 'Y')
        ax.set_title(self.options.get('title', '散点图'))
        
        # 添加标签（可选）
        for i, label in enumerate(labels):
            ax.annotate(label, (x_values[i], y_values[i]))
