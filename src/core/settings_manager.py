# src/core/settings_manager.py
import json
import os
from pathlib import Path
import matplotlib.pyplot as plt

class SettingsManager:
    def __init__(self):
        # 设置配置文件路径
        self.config_dir = Path.home() / ".vplotter"
        self.config_file = self.config_dir / "config.json"
        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def load_settings(self):
        """从JSON文件加载设置，提供默认值"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # 合并加载的设置和默认设置，确保所有设置项都存在
                    return self._merge_with_defaults(loaded_settings)
            except (json.JSONDecodeError, IOError):
                return self.get_default_settings()
        return self.get_default_settings()
    
    def save_settings(self, settings):
        """保存设置到JSON文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def _merge_with_defaults(self, loaded_settings):
        """将加载的设置与默认设置合并"""
        defaults = self.get_default_settings()
        
        # 深度合并字典
        def deep_merge(source, destination):
            for key, value in source.items():
                if key in destination:
                    if isinstance(value, dict) and isinstance(destination[key], dict):
                        deep_merge(value, destination[key])
                    else:
                        destination[key] = value
                else:
                    destination[key] = value
            return destination
        
        return deep_merge(loaded_settings, defaults.copy())
    
    def get_default_settings(self):
        """获取默认设置"""
        # 获取当前Matplotlib默认字体
        default_font = plt.rcParams['font.sans-serif'][0] if plt.rcParams['font.sans-serif'] else "SimHei"
        
        return {
            "data_interface": {
                "show_row_numbers": True,           # 是否显示行号
                "show_grid": True,                  # 是否显示网格
                "auto_resize_columns": True,        # 是否自动调整列宽
                "default_row_count": 10,            # 默认行数
                "default_column_count": 3,          # 默认列数
                "column_naming": "列1, 列2, ..."    # 列命名格式
            },
            "plot_settings": {
                "default_chart_type": "折线图",     # 默认图表类型
                "default_theme": "默认",            # 默认主题
                "default_width": 800,               # 默认宽度  
                "default_height": 600,              # 默认高度
                "bg_color": "#ffffff",              # 背景颜色
                "grid_color": "#c8c8c8",            # 网格颜色
                "font_family": default_font,        # 字体族
                "label_size": 12,                   # 标签字号
                "tick_size": 10,                    # 刻度字号
                "title_size": 14,                   # 标题字号
                "line_width": 2.0,                  # 线条宽度
                "border_width": 1.0,                # 边框宽度
                "marker_size": 5.0                  # 标记大小
            }
        }
