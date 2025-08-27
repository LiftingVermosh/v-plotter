# src/ui/chart_windows.py
# 这个文件是图表窗口的实现，主要是继承自QDialog，并使用matplotlib绘制图表。

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

from src.core.settings_manager import SettingsManager

matplotlib.use('SVG')

class ChartWindow(QDialog):
    def __init__(self, container, chart_type, parent=None, options=None):
        super().__init__(parent)
        self.container = container
        self.chart_type = chart_type
        self.options = options or {}
        self.setting_manager = SettingsManager()
        self.settings = self.setting_manager.load_settings()
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
        
    def apply_draw_config(self, ax):
        """应用绘图配置设置"""
        plot_settings = self.settings.get("plot_settings", {})
        
        # 应用字体设置
        font_family = plot_settings.get("font_family", "SimHei")
        label_size = plot_settings.get("label_size", 12)
        tick_size = plot_settings.get("tick_size", 10)
        title_size = plot_settings.get("title_size", 14)
        
        # 设置全局字体
        plt.rcParams['font.sans-serif'] = [font_family] + plt.rcParams['font.sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置坐标轴标签字体
        ax.xaxis.label.set_fontfamily(font_family)
        ax.yaxis.label.set_fontfamily(font_family)
        ax.xaxis.label.set_size(label_size)
        ax.yaxis.label.set_size(label_size)
        
        # 设置刻度字体
        for tick in ax.get_xticklabels():
            tick.set_fontfamily(font_family)
            tick.set_fontsize(tick_size)
        
        for tick in ax.get_yticklabels():
            tick.set_fontfamily(font_family)
            tick.set_fontsize(tick_size)
        
        # 设置标题字体
        ax.title.set_fontfamily(font_family)
        ax.title.set_fontsize(title_size)
        
        # 应用背景颜色
        bg_color = plot_settings.get("bg_color", "#ffffff")
        self.figure.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        
        # 应用网格颜色和显示
        grid_color = plot_settings.get("grid_color", "#c8c8c8")
        ax.grid(True, color=grid_color, linestyle='--', alpha=0.7)
        
        # 应用线宽设置
        line_width = plot_settings.get("line_width", 2.0)
        # 在绘图方法中应用线宽
        
        # 应用边框宽度设置
        border_width = plot_settings.get("border_width", 1.0)
        for spine in ax.spines.values():
            spine.set_linewidth(border_width)
        
        # 应用标记点大小设置
        self.marker_size = plot_settings.get("marker_size", 5.0)
        # 在绘图方法中应用标记点大小
        
    def draw_chart(self):
        # 从容器获取数据
        if self.container is None:
            return
        
        data_array = self.container.get_table_data_as_numpy()
        headers = self.container.column_headers
        
        # 确保数据是二维的
        if not data_array.any():
            QMessageBox.warning(self, "错误", "数据为空！")
            return

        if len(data_array.shape) == 1:
            data_array = data_array.reshape(-1, 1)
        
        # 清除旧图形
        self.figure.clear()
        
        ax = self.figure.add_subplot(111)
        
        # 应用绘图配置
        self.apply_draw_config(ax)
        
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
        
        # 设置标题
        title = self.options.get('title', f'{self.chart_type} Chart')
        ax.set_title(title)
        
        self.canvas.draw()
    
    def draw_line_chart(self, ax, data_array, headers):
        """绘制折线图，应用线宽和标记点大小设置"""
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
        
        # 应用线宽和标记点大小设置
        line_width = self.settings.get("plot_settings", {}).get("line_width", 2)
        marker_size = self.settings.get("plot_settings", {}).get("marker_size", 5)
        
        ax.plot(x_pos, values, marker='o', linewidth=line_width, markersize=marker_size)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels)
        ax.set_xlabel(headers[0] if headers else 'X')
        ax.set_ylabel(headers[1] if len(headers) > 1 else 'Y')
    
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
