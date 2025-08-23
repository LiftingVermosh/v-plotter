# src/core/data_container.py
# 这个文件主要是用来存储数据的，包括数据类型、数据值、数据单位等。

import numpy as np
import pandas as pd
import uuid
from src.core.signals import container_signals

class DataContainer:
    def __init__(self, data_type="data", data_value=None, data_unit=""):
        self.data_type : str = data_type
        self.data_value = data_value    
        self.uuid : str = uuid.uuid4().hex
        self.data_unit : str = data_unit
        self.source : str = "新建"
        self.name : str = "数据组"

        self.table_data = None #
        self.column_headers = []
        self.row_count = 0
        self.column_count = 0
    
    def set_table_data(self, data, headers):
        """ 设置表格数据 """
        self.table_data = data
        self.column_headers = headers

        if len(headers) > 0:
            self.row_count = len(data)
            self.column_count = len(headers)
        else:
            self.row_count = 0
            self.column_count = 0
    
    def get_table_data_as_numpy(self):
        """获取Numpy数组形式的表格数据"""
        if self.table_data is None:
            return None
        
        # 确保返回的是二维数组
        data = np.array(self.table_data)
        if len(data.shape) == 1:
            return data.reshape(-1, 1)
        return data

    
    def get_table_data_as_pandas(self):
        """ 获取Pandas DataFrame形式的表格数据 """
        if self.table_data is None:
            return None
        
        # 确保列名是字符串，避免后续处理问题
        str_headers = [str(header) for header in self.column_headers]
        return pd.DataFrame(self.table_data, columns=str_headers)
