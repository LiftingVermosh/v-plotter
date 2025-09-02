# src/core/data_container.py

import numpy as np
import pandas as pd
import uuid
from PyQt6.QtWidgets import QMessageBox
from src.core.signals import container_signals, data_signals
from typing import Optional, List, Dict, Any, Union

class DataContainer:
    def __init__(self, data_type="data", data_value=None, data_unit=""):
        self.data_type = data_type
        self.data_value = data_value    
        self.uuid = uuid.uuid4().hex
        self.data_unit = data_unit
        self.source = "新建"
        self.name = "数据组"
        self.metadata = {}  # 添加元数据存储

        # 使用DataFrame作为主要数据存储
        self.dataframe: Optional[pd.DataFrame] = None
        self.row_count = 0
        self.column_count = 0
    
    def set_table_data(self, data, headers=None):
        """设置表格数据，支持多种输入格式"""
        if data is None:
            self._clear_data()
            return
            
        try:
            # 处理不同的输入类型
            if isinstance(data, pd.DataFrame):
                # 如果已经是DataFrame，直接使用
                self.dataframe = data.copy()
            elif isinstance(data, np.ndarray):
                # 如果是numpy数组，转换为DataFrame
                if headers is None:
                    headers = [f"Column_{i}" for i in range(data.shape[1])]
                self.dataframe = pd.DataFrame(data, columns=headers)
            elif isinstance(data, list):
                # 如果是列表，转换为DataFrame
                if not data or len(data) == 0:
                    self._clear_data()
                    return
                    
                if headers is None:
                    headers = [f"Column_{i}" for i in range(len(data[0]))]
                self.dataframe = pd.DataFrame(data, columns=headers)
            else:
                # 其他类型，尝试转换为DataFrame
                self.dataframe = pd.DataFrame(data)
                if headers is not None:
                    self.dataframe.columns = headers
            
            # 确保列名是字符串
            self.dataframe.columns = self.dataframe.columns.astype(str)
            
            # 更新统计信息
            self.update_stats()
            
        except Exception as e:
            self._clear_data()
            raise ValueError(f"无法将数据转换为DataFrame: {e}")
    
    def sort_data(self, column: str, ascending: bool = True) -> bool:
        """对数据进行排序"""
        if self.dataframe is None:
            return False
        
        try:
            # 排序
            self.dataframe = self.dataframe.sort_values(by=column, ascending=ascending)
            self.update_stats()
            return True
        except Exception as e:
            QMessageBox.warning(f"排序失败: {e}")
            return False

    def clean_data(self, column: str, sensitive: bool = False, target: str = '0') -> bool:
        """清洗异常值"""
        if self.dataframe is None:
            QMessageBox.warning(None, "错误", "数据为空，无法清洗")
            return False
        
        if column not in self.dataframe.columns:
            QMessageBox.warning(None, "错误", f"列 '{column}' 不存在")
            return False
        
        try:
            # 保存原始数据类型
            origin_dtype = self.dataframe[column].dtype
            
            # 处理数值列和字符串列的不同情况
            if pd.api.types.is_numeric_dtype(origin_dtype):
                # 数值列处理
                try:
                    target_value = float(target)
                except ValueError:
                    QMessageBox.warning(None, "错误", f"对于数值列 '{column}'，替换值 '{target}' 不是有效的数字")
                    return False
                    
                if sensitive:
                    # 严格清洗：替换NaN和无限值
                    self.dataframe[column] = self.dataframe[column].replace(
                        [np.nan, np.inf, -np.inf], target_value
                    )
                else:
                    # 宽松清洗：只替换NaN
                    self.dataframe[column] = self.dataframe[column].fillna(target_value)
            else:
                # 字符串列处理
                # 先将列转换为字符串
                self.dataframe[column] = self.dataframe[column].astype(str)
                
                # 定义要替换的值列表
                if sensitive:
                    to_replace = ['', 'nan', 'None', 'null', 'NaN', 'NA', 'N/A']
                else:
                    to_replace = ['', 'None', 'null']
                
                # 执行替换
                self.dataframe[column] = self.dataframe[column].replace(to_replace, target)
                
                # 尝试转换回原始数据类型（如果是其他非字符串类型）
                try:
                    self.dataframe[column] = self.dataframe[column].astype(origin_dtype)
                except (ValueError, TypeError):
                    # 如果转换失败，保持为字符串类型
                    pass
            
            self.update_stats()
            
            # 发出数据修改信号
            data_signals.data_modified.emit(
                self.dataframe.to_numpy().copy(), 
                self.get_table_headers().copy()
            )
            
            return True
        except Exception as e:
            QMessageBox.warning(None, "错误", f"清洗失败: {e}")
            return False



    def _clear_data(self):
        """清除数据"""
        self.dataframe = None
        self.row_count = 0
        self.column_count = 0
    
    def update_stats(self):
        """更新数据统计信息"""
        if self.dataframe is not None:
            self.row_count = len(self.dataframe)
            self.column_count = len(self.dataframe.columns)
        else:
            self.row_count = 0
            self.column_count = 0
    
    def get_table_data_as_numpy(self) -> Optional[np.ndarray]:
        """获取Numpy数组形式的表格数据"""
        if self.dataframe is None:
            return None
        return self.dataframe.to_numpy()
    
    def get_table_data_as_pandas(self) -> Optional[pd.DataFrame]:
        """获取Pandas DataFrame形式的表格数据"""
        return self.dataframe.copy() if self.dataframe is not None else None
    
    def get_table_headers(self) -> List[str]:
        """获取表格的列名"""
        if self.dataframe is None:
            return []
        return list(self.dataframe.columns)
    
    def get_column_type(self, column_name: str) -> Optional[str]:
        """获取指定列的数据类型"""
        if self.dataframe is None:
            return None
        
        # 确保列名是字符串
        str_column_name = str(column_name)
        
        if str_column_name not in self.dataframe.columns:
            return None
        
        # 获取列的dtype
        dtype = self.dataframe.dtypes[str_column_name]
        
        # 将pandas/numpy类型转换为字符串表示
        if dtype in [np.int64, np.int32, np.int16, np.int8, 'int64', 'int32', 'int16', 'int8']:
            return "int"
        elif dtype in [np.float64, np.float32, np.float16, 'float64', 'float32', 'float16']:
            return "float"
        elif dtype == np.bool_ or dtype == 'bool':
            return "bool"
        elif np.issubdtype(dtype, np.datetime64) or 'datetime' in str(dtype):
            return "date"
        elif dtype == np.object_ or dtype == 'object' or dtype == 'string':
            # 检查是否可能是字符串类型
            return "str"
        else:
            return str(dtype)
    
    def apply_filter(self, filter_condition: Dict[str, Any]) -> bool:
        """应用过滤条件"""
        if self.dataframe is None:
            return False
        
        try:
            # 创建过滤掩码
            mask = self.create_filter_mask(filter_condition)
            
            # 应用过滤
            filtered_data = self.dataframe[mask]
            
            # 创建一个新的DataContainer来存储过滤后的数据
            filtered_container = DataContainer()
            filtered_container.set_table_data(filtered_data)
            filtered_container.name = f"{self.name} (已过滤)"
            
            # 发出信号通知过滤完成
            container_signals.filter_applied.emit(self.uuid, filtered_container.uuid)
            
            return True
        except Exception as e:
            QMessageBox.warning(f"过滤应用失败: {e}")
            return False
    
    def create_filter_mask(self, filter_condition: Dict[str, Any]) -> pd.Series:
        """根据过滤条件创建布尔掩码"""
        column = filter_condition["column"]
        operator = filter_condition["operator"]
        value = filter_condition["value"]
        case_sensitive = filter_condition.get("case_sensitive", False)
        
        # 获取列数据
        column_data = self.dataframe[column]
        
        # 对于数值比较，确保值的类型正确
        if operator in ["大于", "小于", "大于等于", "小于等于"]:
            # 尝试将值转换为数值类型
            try:
                if column_data.dtype in [np.int64, np.int32, np.int16, np.int8, 'int64', 'int32', 'int16', 'int8']:
                    value = int(value)
                elif column_data.dtype in [np.float64, np.float32, np.float16, 'float64', 'float32', 'float16']:
                    value = float(value)
            except (ValueError, TypeError):
                raise ValueError(f"无法将值 '{value}' 转换为数值类型")
        
        # 根据运算符创建掩码
        if operator == "等于":
            if column_data.dtype == 'object' and not case_sensitive:
                # 对于字符串且不区分大小写的情况
                return column_data.str.lower() == str(value).lower()
            else:
                return column_data == value
        elif operator == "不等于":
            if column_data.dtype == 'object' and not case_sensitive:
                return column_data.str.lower() != str(value).lower()
            else:
                return column_data != value
        elif operator == "大于":
            return column_data > value
        elif operator == "小于":
            return column_data < value
        elif operator == "大于等于":
            return column_data >= value
        elif operator == "小于等于":
            return column_data <= value
        elif operator == "包含":
            if case_sensitive:
                return column_data.str.contains(str(value), na=False)
            else:
                return column_data.str.contains(str(value), case=False, na=False)
        elif operator == "不包含":
            if case_sensitive:
                return ~column_data.str.contains(str(value), na=False)
            else:
                return ~column_data.str.contains(str(value), case=False, na=False)
        elif operator == "开头为":
            if case_sensitive:
                return column_data.str.startswith(str(value))
            else:
                return column_data.str.lower().str.startswith(str(value).lower())
        elif operator == "结尾为":
            if case_sensitive:
                return column_data.str.endswith(str(value))
            else:
                return column_data.str.lower().str.endswith(str(value).lower())
        elif operator == "为空":
            return column_data.isna()
        elif operator == "不为空":
            return ~column_data.isna()
        else:
            raise ValueError(f"不支持的运算符: {operator}")

    
    def add_column(self, name: str, data=None, dtype=None):
        """添加新列"""
        if self.dataframe is None:
            self.dataframe = pd.DataFrame()
        
        if data is None:
            # 如果没有提供数据，创建一个默认值的列
            if dtype == 'int':
                data = 0
            elif dtype == 'float':
                data = 0.0
            elif dtype == 'str':
                data = ""
            elif dtype == 'bool':
                data = False
            else:
                data = None
        
        self.dataframe[name] = data
        self.update_stats()
    
    def remove_column(self, name: str):
        """移除列"""
        if self.dataframe is not None and name in self.dataframe.columns:
            self.dataframe.drop(columns=[name], inplace=True)
            self.update_stats()
    
    def get_unique_values(self, column_name: str) -> List[Any]:
        """获取指定列的唯一值"""
        if self.dataframe is None or column_name not in self.dataframe.columns:
            return []
        
        return self.dataframe[column_name].dropna().unique().tolist()
    
    def get_column_stats(self, column_name: str) -> Dict[str, Any]:
        """获取列的统计信息"""
        if self.dataframe is None or column_name not in self.dataframe.columns:
            return {}
        
        column_data = self.dataframe[column_name]
        dtype = self.get_column_type(column_name)
        
        stats = {
            "dtype": dtype,
            "count": column_data.count(),
            "null_count": column_data.isna().sum(),
            "unique_count": column_data.nunique()
        }
        
        # 数值型列的额外统计
        if dtype in ["int", "float"]:
            stats.update({
                "min": column_data.min(),
                "max": column_data.max(),
                "mean": column_data.mean(),
                "std": column_data.std()
            })
        
        return stats
    
    def to_dict(self) -> Dict[str, Any]:
        """将数据转换为字典格式（用于序列化）"""
        if self.dataframe is None:
            return {
                "data": None,
                "headers": []
            }
        
        return {
            "data": self.dataframe.to_dict('list'),
            "headers": list(self.dataframe.columns),
            "metadata": self.metadata,
            "name": self.name,
            "source": self.source,
            "data_type": self.data_type,
            "data_unit": self.data_unit
        }
    
    def from_dict(self, data_dict: Dict[str, Any]):
        """从字典加载数据"""
        if data_dict.get("data") is None:
            self.dataframe = None
        else:
            self.dataframe = pd.DataFrame(data_dict["data"])
            if "headers" in data_dict and data_dict["headers"]:
                self.dataframe.columns = data_dict["headers"]
        
        # 加载元数据
        self.metadata = data_dict.get("metadata", {})
        self.name = data_dict.get("name", "数据组")
        self.source = data_dict.get("source", "新建")
        self.data_type = data_dict.get("data_type", "data")
        self.data_unit = data_dict.get("data_unit", "")
        
        self.update_stats()
    
    def __repr__(self):
        return f"DataContainer(name={self.name}, shape=({self.row_count}, {self.column_count}), source={self.source})"
