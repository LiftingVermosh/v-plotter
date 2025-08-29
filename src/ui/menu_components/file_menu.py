# src/ui/menu_component/file_menu.py
# 这个文件是用来实现文件菜单的，包括新建、打开、保存、另存为、打印、退出等功能。

import os
import json
import pandas as pd
import numpy as np
from typing import Optional, List, Any
from PyQt6.QtWidgets import QMenu, QFileDialog, QMessageBox, QWidget
from PyQt6.QtGui import QKeySequence
from src.core.data_container import DataContainer
from src.core.signals import container_signals, tab_signals

class FileMenu(QMenu):
    def __init__(self, parent=None, main_window=None):
        super().__init__("&文件", parent)
        self.main_window = main_window
        
        # 文件操作
        self.new_action = self.addAction("&新建...", QKeySequence("Ctrl+N"))
        self.open_action = self.addAction("&打开...", QKeySequence("Ctrl+O"))
        self.save_action = self.addAction("&保存", QKeySequence("Ctrl+S"))
        self.save_as_action = self.addAction("另存为")
        self.addSeparator()
        
        # 打印操作
        self.print_action = self.addAction("&打印...", QKeySequence("Ctrl+P"))
        self.addSeparator()
        
        # 退出操作
        self.exit_action = self.addAction("&退出", QKeySequence("Alt+F4"))
        
        # 连接信号
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action.triggered.connect(self.save_as)
        self.print_action.triggered.connect(self.print_file)
        self.exit_action.triggered.connect(self.exit_app)

    def new_file(self):
        if self.main_window:
            # 新建数据容器
            container_signals.container_created.emit()
        else:
            QMessageBox.warning(self.main_window, "错误", "无法访问主窗口")

    def open_file(self):
        """打开文件并进行操作"""
        try:
            file_dialog = QFileDialog(self, "打开文件")
            file_path, _ = file_dialog.getOpenFileName(
                parent=self, 
                caption="打开文件", 
                directory="", 
                filter="所有支持的文件(*.csv *.xlsx *.xls *.json);;csv文件(*.csv);;xlsx文件(*.xlsx, *.xls);;json文件(*.json)"
            )
            if not file_path:
                return  # 用户取消操作
            # 加载文件拓展名，并根据拓展名调用相应的加载函数
            extension = os.path.splitext(file_path)[1].lower()
            # 创建数据容器
            container = DataContainer()
            container.name = os.path.splitext(os.path.basename(file_path))[0]
            container.source = file_path
            container.data_type = extension.replace(".", "")
            # 加载数据
            if extension == ".csv":
                self.load_csv(file_path, container)
            elif extension in [".xlsx", ".xls"]:
                self.load_excel(file_path, container)
            elif extension == ".json":
                self.load_json(file_path, container)
            else:
                QMessageBox.warning(self.main_window, "错误", "不支持的文件类型")
                return
            
            # 检查数据有效性
            if container.dataframe is None or container.dataframe.empty:
                QMessageBox.warning(self.main_window, "警告", "文件内容为空或格式不正确")
                return
            
            # 通知主窗口更新数据容器
            container_signals.container_ready.emit(container)
        except Exception as e:
            QMessageBox.warning(self.main_window, "错误", f"打开文件失败：{str(e)}")

    ## open选项下函数
    def load_csv(self, file_path, container):
        """加载CSV文件"""
        try:
            # 尝试读取第一行来判断是否为表头
            first_row = pd.read_csv(file_path, nrows=1, header=None)
            
            # 检查第一行是否主要为数值
            if is_numeric_row(first_row.iloc[0]):
                # 数值无表头
                df = pd.read_csv(file_path, header=None)
                headers = [f"列{i+1}" for i in range(df.shape[1])]  # 生成默认列名
            else:
                # 非数值，作为表头
                df = pd.read_csv(file_path)
                headers = df.columns.tolist()
            
            # 获取数据数组
            data_array = df.to_numpy()
            
            # 获取数据
            container.set_table_data(data_array, headers)
            
        except Exception as e:
            QMessageBox.warning(self.main_window, "错误", f"加载CSV文件时出错: {str(e)}")
            return
    def load_excel(self, file_path, container):
        """加载Excel文件，智能识别第一行是否为表头"""
        try:
            # 首先尝试读取第一行来判断是否为表头
            first_row = pd.read_excel(file_path, nrows=1, header=None)
            
            # 检查第一行是否主要为数值
            if is_numeric_row(first_row.iloc[0]):
                # 第一行是数值，没有表头
                df = pd.read_excel(file_path, header=None)
                headers = [f"列{i+1}" for i in range(df.shape[1])]  # 生成默认列名
            else:
                # 第一行不是数值，作为表头
                df = pd.read_excel(file_path)
                headers = df.columns.tolist()
            
            # 获取数据数组
            data_array = df.to_numpy()
            
            # 获取数据
            container.set_table_data(data_array, headers)
            
        except Exception as e:
            QMessageBox.warning(self.main_window, "错误", f"加载Excel文件时出错: {str(e)}")
            return

    def load_json(self, file_path, container):
        """ 加载json文件 """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list) and all(isinstance(row, dict) for row in data):
            # 列表中每个元素都是字典
            headers = list(data[0].keys()) if data else []
            rows = []
            for row in data:
                row.append([row.get(header, "") for header in headers])
            data_array = np.array(rows)
        elif isinstance(data, dict) and 'data' in data and 'columns' in data:
            # 字典中包含data和columns两个键
            headers = data.get('columns', [])
            data_array = np.array(data.get('data', []))
        else:
            QMessageBox.warning(self.main_window, "错误", "不支持的json格式\t")
            return

        container.set_table_data(data_array, headers)
    
    """ save选项下函数 """
    # 保存当前文件
    def save_file(self):
        # 获取当前活动视图
        if not hasattr(self.main_window, 'plot_area'):
            QMessageBox.warning(self.main_window, "错误", "\n无法访问绘图区域\t")
            return
        
        # 获取当前数据容器
        cur_tab = self.main_window.plot_area.get_current_table_tab()
        if cur_tab is None:
            QMessageBox.warning(self.main_window, "错误", "\n当前没有活动的表格视图\t")
            return
        
        # 获取数据容器
        container = cur_tab.container
        
        # 如果数据容器没有保存过，则调用另存为
        if container.source == "新建":
            # 无原始路径，调用另存为
            self.save_as()
            return
        
        try:
            # 获取当前数据
            data = container.get_table_data_as_numpy()
            headers = container.column_headers
            # 根据文件拓展名调用相应的保存函数
            extensions = os.path.splitext(container.source)[1].lower()
            if extensions == ".csv":
                self.save_csv(container.source, data, headers)
            elif extensions == ".xlsx":
                self.save_excel(container.source, data, headers)
            elif extensions == ".json":
                self.save_json(container.source, data, headers)
            else:
                QMessageBox.warning(self.main_window, "错误", "不支持的文件类型\t")
                return
        except Exception as e:
            QMessageBox.warning(self.main_window, "错误", f"保存文件失败：{str(e)}\t")
            
    # 另存为
    def save_as(self):
        # 获取当前活动视图
        if not hasattr(self.main_window, 'plot_area'):
            QMessageBox.warning(self.main_window, "错误", "\n无法访问绘图区域\t")
            return
        
        # 使用正确的方法名
        cur_tab = self.main_window.plot_area.get_current_table_tab()
        if cur_tab is None:
            QMessageBox.warning(self.main_window, "错误", "当前没有活动的表格视图\t")
            return
        
        # 获取数据容器
        container = cur_tab.container
        
        file_dialog = QFileDialog(self, "另存为")
        file_path, selected_filter = file_dialog.getSaveFileName(
            parent = self, 
            caption = "另存为", 
            directory = container.source if container.source else "", 
            filter = "csv文件(*.csv);;xlsx文件(*.xlsx);;json文件(*.json)"
        )
        if not file_path:
            return  # 用户取消操作
        
        try:
            # 获取当前数据
            data = container.get_table_data_as_numpy()
            headers = container.column_headers
            # 根据文件拓展名调用相应的保存函数
            extensions = os.path.splitext(file_path)[1].lower()
            if file_path.endswith('.csv') or selected_filter == "CSV文件(*.csv)":
                self.save_csv(file_path, data, headers)
            elif file_path.endswith('.xlsx') or selected_filter == "Excel文件(*.xlsx)":
                self.save_excel(file_path, data, headers)
            elif file_path.endswith('.json') or selected_filter == "JSON文件(*.json)":
                self.save_json(file_path, data, headers)
            # 更新容器信息
            container.source = file_path
            container.name = os.path.split(file_path)[1]
            # 通知主窗口更新数据容器
            if self.main_window and hasattr(self.main_window, "plot_area"):
                table_tab = self.main_window.plot_area.parent_table_tab
                if table_tab:
                    for uuid, info in table_tab.tab_map.items():
                        if info['container'] == container:
                            self.set_tab_name(table_tab, info['index'], container.name)
            QMessageBox.information(self.main_window, "提示", "保存成功\t")
        except Exception as e:
            QMessageBox.warning(self.main_window, "错误", f"保存文件失败：{str(e)}\t")

    # 保存csv文件
    def save_csv(self, file_path, data, headers):
        """ 保存csv文件 """
        df = pd.DataFrame(data, columns=headers)
        df.to_csv(file_path, index=False)

    # 保存excel文件
    def save_excel(self, file_path, data, headers):
        """ 保存excel文件 """
        df = pd.DataFrame(data, columns=headers)
        df.to_excel(file_path, index=False)

    # 保存json文件
    def save_json(self, file_path, data, headers):
        """ 保存json文件 """
        data_dict = {
            "columns": headers,
            "data": data.tolist()
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

    # 获取当前活动的表格视图
    def get_current_table_tab(self):
        """获取当前活动的表格视图"""
        if not self.main_window or not hasattr(self.main_window, "plot_area"):
            return None
        
        plot_area = self.main_window.plot_area
        return plot_area.get_current_table_tab()  # 返回当前活动的表格视图
    
    def set_tab_name(self, tab_widget, index, name):
        """ 设置表格视图的标签名 """
        tab_widget.setTabText(index, name)

        # 更新映射名称
        for uuid, info in tab_widget.tab_map.items():
            if info['index'] == index:
                tab_signals.table_tab_created.emit(uuid, name)
    
    def print_file(self):
        """ 打印文件 """
        pass
    
    def exit_app(self):
        """ 退出程序 """
        if self.main_window:
            self.main_window.close()
        else:
            QMessageBox.warning(self.main_window, "错误", "无法访问主窗口\t")

def is_numeric_row(row):
    """
    判断一行数据是否主要为数值类型
    
    参数:
        row: 一行数据，可以是列表、Series或其他可迭代对象
        
    返回:
        bool: 如果该行 >50% 的元素可以转换为数值，则返回True
    """
    numeric_count = 0
    total_count = 0
    
    for item in row:
        # 跳过空值
        if pd.isna(item) or item == "":
            continue
            
        total_count += 1
        
        # 尝试转换为数值
        try:
            float(item)
            numeric_count += 1
        except (ValueError, TypeError):
            pass
    
    # 如果没有有效数据，默认返回False
    if total_count == 0:
        return False
    
    # 如果数值比例超过50%，则认为这是数值行
    return (numeric_count / total_count) > 0.5