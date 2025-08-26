# src/core/settings_manager.py
import json
import os
import base64
from pathlib import Path
import matplotlib.pyplot as plt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import QByteArray
from PyQt6.QtWidgets import QApplication, QWidget

class SettingsManager:
    def __init__(self):
        self.config_dir = Path.home() / ".vplotter"
        self.config_file = self.config_dir / "config.json"
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
            # 在保存前转换 QByteArray 为 Base64 字符串
            serializable_settings = self._make_settings_serializable(settings)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_settings, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"保存设置失败: {e}")
            return False
    
    def _make_settings_serializable(self, settings):
        """将设置转换为可序列化的格式"""
        if isinstance(settings, dict):
            return {k: self._make_settings_serializable(v) for k, v in settings.items()}
        elif isinstance(settings, list):
            return [self._make_settings_serializable(item) for item in settings]
        elif isinstance(settings, QByteArray):
            # 将 QByteArray 转换为 Base64 字符串
            return base64.b64encode(settings.data()).decode('utf-8')
        else:
            return settings
    
    def _restore_from_serializable(self, settings):
        """从可序列化的格式恢复设置"""
        if isinstance(settings, dict):
            return {k: self._restore_from_serializable(v) for k, v in settings.items()}
        elif isinstance(settings, list):
            return [self._restore_from_serializable(item) for item in settings]
        elif isinstance(settings, str):
            # 尝试将 Base64 字符串转换回 QByteArray
            try:
                return QByteArray(base64.b64decode(settings))
            except:
                # 如果不是有效的 Base64 字符串，保持原样
                return settings
        else:
            return settings
    
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
        
        # 先恢复可序列化的数据
        restored_settings = self._restore_from_serializable(loaded_settings)
        return deep_merge(restored_settings, defaults.copy())
    
    def get_default_settings(self):
        """获取默认设置"""
        # 获取当前Matplotlib默认字体
        default_font = plt.rcParams['font.sans-serif'][0] if plt.rcParams['font.sans-serif'] else "SimHei"
        
        return {
            "ui": {
                "theme": "Light",  # 默认主题
                "language": "zh_CN",
                "font_family": "Microsoft YaHei",
                "font_size": 10,
                "dpi_scaling": 1.0,
                "toolbar_visible": True,
                "statusbar_visible": True,
                "window_state": None,  # 保存窗口状态（最大化/最小化/正常）
                "window_geometry": None  # 保存窗口几何信息
            },
            "data_interface": {
                "show_row_numbers": True,           # 显示行号
                "show_grid": True,                  # 显示网格  
                "auto_resize_columns": True,        # 自动调整列宽
                "default_row_count": 10,            # 默认行数
                "default_column_count": 3,          # 默认列数
                "column_naming": "列1, 列2, ...",   # 列名模板
                "default_width": 1200,  
                "default_height": 800
            },
            "plot_settings": {
                "default_chart_type": "折线图",
                "default_theme": "默认",
                "default_width": 800,
                "default_height": 600,
                "bg_color": "#ffffff",
                "grid_color": "#c8c8c8",
                "font_family": default_font,
                "label_size": 12,
                "tick_size": 10,
                "title_size": 14,
                "line_width": 2.0,
                "border_width": 1.0,
                "marker_size": 5.0
            },
            "recent_files": [],  # 最近打开的文件列表
            "user_preferences": {
                "auto_save": False,
                "auto_save_interval": 5,  # 分钟
                "backup_enabled": True,
                "backup_count": 3
            }
        }
    
    def get_ui_settings(self):
        """获取UI相关设置"""
        settings = self.load_settings()
        return settings.get("ui", {})
    
    def save_ui_settings(self, ui_settings):
        """保存UI相关设置"""
        settings = self.load_settings()
        settings["ui"] = ui_settings
        return self.save_settings(settings)
    
    def get_theme_setting(self):
        """获取主题设置"""
        ui_settings = self.get_ui_settings()
        return ui_settings.get("theme", "Light")
    
    def save_theme_setting(self, theme_name):
        """保存主题设置"""
        ui_settings = self.get_ui_settings()
        ui_settings["theme"] = theme_name
        return self.save_ui_settings(ui_settings)
    
    def get_window_geometry(self):
        """获取窗口几何设置"""
        ui_settings = self.get_ui_settings()
        geometry_data = ui_settings.get("window_geometry")
        
        # 如果是从 Base64 恢复的 QByteArray，直接返回
        if isinstance(geometry_data, QByteArray):
            return geometry_data
        
        # 如果是 Base64 字符串，转换为 QByteArray
        if isinstance(geometry_data, str):
            try:
                return QByteArray(base64.b64decode(geometry_data))
            except:
                pass
        
        return None
    
    def save_window_geometry(self, geometry):
        """保存窗口几何设置"""
        ui_settings = self.get_ui_settings()
        ui_settings["window_geometry"] = geometry
        return self.save_ui_settings(ui_settings)
    
    def get_window_state(self):
        """获取窗口状态"""
        ui_settings = self.get_ui_settings()
        state_data = ui_settings.get("window_state")
        
        # 如果是从 Base64 恢复的 QByteArray，直接返回
        if isinstance(state_data, QByteArray):
            return state_data
        
        # 如果是 Base64 字符串，转换为 QByteArray
        if isinstance(state_data, str):
            try:
                return QByteArray(base64.b64decode(state_data))
            except:
                pass
        
        return None
    
    def save_window_state(self, state):
        """保存窗口状态"""
        ui_settings = self.get_ui_settings()
        ui_settings["window_state"] = state
        return self.save_ui_settings(ui_settings)

    def save_window_state_and_geometry(self, window):
        """从QMainWindow保存窗口状态和几何信息"""
        geometry = window.saveGeometry()
        state = window.saveState()
        if geometry and not geometry.isEmpty():
            self.save_window_geometry(geometry)
        if state and not state.isEmpty():
            self.save_window_state(state)
    
    # 恢复窗口状态和几何信息到QMainWindow
    def restore_window_state_and_geometry(self, window, default_size=(1200, 800)):
        """恢复窗口状态和几何信息到QMainWindow"""
        geometry = self.get_window_geometry()
        state = self.get_window_state()
        if geometry and not geometry.isEmpty():
            window.restoreGeometry(geometry)
        else:
            window.resize(*default_size)
        if state and not state.isEmpty():
            window.restoreState(state)
    
    # 应用UI设置（例如字体、DPI缩放）
    def apply_ui_settings(self, settings=None):
        """应用UI相关设置，如字体和DPI缩放"""
        if settings is None:
            settings = self.load_settings()
        ui_settings = settings.get("ui", {})
        # 应用字体设置
        font_family = ui_settings.get("font_family", "Microsoft YaHei")
        font_size = ui_settings.get("font_size", 10)
        app = QApplication.instance()
        if app:
            font = QFont(font_family, font_size)
            app.setFont(font)
        # 应用DPI缩放（如果需要）
        dpi_scaling = ui_settings.get("dpi_scaling", 1.0)
        if app and hasattr(app, 'setHighDpiScaleFactorRoundingPolicy'):
            from PyQt6.QtCore import Qt
            app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            app.setAttribute(Qt.AA_EnableHighDpiScaling)
        # 可以添加其他UI设置的应用逻辑