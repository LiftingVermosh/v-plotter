# src/core/settings_manager.py
import json
import os
from PyQt6.QtCore import QSettings

class SettingsManager:
    def __init__(self):
        self.settings = QSettings("YourCompany", "V-Plotter")
        # 或者使用JSON文件
        # self.config_file = os.path.expanduser("~/.vplotter/config.json")
        # self.load_settings()
    
    def load_settings(self):
        """加载设置"""
        # 使用QSettings
        return {
            "data_interface": {
                "show_row_numbers": self.settings.value("data_interface/show_row_numbers", True, type=bool),
                "show_grid": self.settings.value("data_interface/show_grid", True, type=bool),
                # ... 其他设置
            },
            "plot_settings": {
                "default_chart_type": self.settings.value("plot_settings/default_chart_type", "折线图"),
                # ... 其他设置
            }
        }
    
    def save_settings(self, settings):
        """保存设置"""
        # 使用QSettings
        data_interface = settings.get("data_interface", {})
        plot_settings = settings.get("plot_settings", {})
        
        self.settings.setValue("data_interface/show_row_numbers", data_interface.get("show_row_numbers", True))
        self.settings.setValue("data_interface/show_grid", data_interface.get("show_grid", True))
        
        self.settings.setValue("plot_settings/default_chart_type", plot_settings.get("default_chart_type", "折线图"))
        
        # 同步设置
        self.settings.sync()
    
    # 使用JSON文件的替代方案
    def load_settings_json(self):
        """从JSON文件加载设置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_settings()
        return self.get_default_settings()
    
    def save_settings_json(self, settings):
        """保存设置到JSON文件"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(settings, f, indent=4)
    
    def get_default_settings(self):
        """获取默认设置"""
        return {
            "data_interface": {
                "show_row_numbers": True,
                "show_grid": True,
                "auto_resize_columns": True,
                "default_row_count": 10,
                "default_column_count": 3,
                "column_naming": "列1, 列2, ..."
            },
            "plot_settings": {
                "default_chart_type": "折线图",
                "default_theme": "默认",
                "default_width": 800,
                "default_height": 600,
                "bg_color": "#ffffff",
                "grid_color": "#c8c8c8"
            }
        }
