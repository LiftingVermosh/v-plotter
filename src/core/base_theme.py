# src/core/base_theme.py
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QColor, QFont, QIcon
from pathlib import Path
import json
from src.core.settings_manager import SettingsManager

# 创建兼容的元类
class QObjectABCMeta(type(QObject), type(ABC)):
    pass

class BaseTheme(QObject, ABC, metaclass=QObjectABCMeta):
    """抽象主题基类，包括所有主题必须实现的接口"""
    
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.resources_path = Path("src/resources/themes") / name.lower().replace(" ", "_")
        self.stylesheet = ""
        self.config = {}
        self.settings_manager = SettingsManager()
        self._load_resources()  
    
    def _load_resources(self):
        """加载主题资源（样式表、图标等）"""
        # 加载样式表
        stylesheet_path = self.resources_path / "styles.qss"
        if stylesheet_path.exists():
            try:
                with open(stylesheet_path, 'r', encoding='utf-8') as f:
                    self.stylesheet = f.read()
                    # 确保样式表不为空
                    if not self.stylesheet.strip():
                        QMessageBox.warning(f"警告: {self.name} 主题的样式表为空，使用默认样式表")
                        self.stylesheet = self._get_default_stylesheet()
            except Exception as e:
                print(f"加载样式表失败: {e}")
                self.stylesheet = self._get_default_stylesheet()
        else:
            print(f"警告: {stylesheet_path} 不存在，使用默认样式表")
            self.stylesheet = self._get_default_stylesheet()
        
        # 加载主题配置（如果有）
        config_path = self.resources_path / "theme.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"加载主题配置失败: {e}")
                self.config = {}

    
    def _get_default_stylesheet(self):
        """获取默认样式表（当QSS文件不存在时使用）"""
        return f"""
            /* 默认样式表 - {self.name} 主题 */
            QMainWindow {{
                background-color: #f0f0f0;
                color: #333333;
            }}
            QPushButton {{
                background-color: #007acc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            /* 更多默认样式... */
        """
    
    def get_color(self, role: str) -> QColor:
        """根据角色获取颜色"""
        # 首先尝试从主题配置中获取颜色
        if "colors" in self.config and role in self.config["colors"]:
            return QColor(self.config["colors"][role])
        
        # 如果主题配置中没有，使用默认颜色映射
        default_colors = {
            "primary": QColor("#007acc"),
            "secondary": QColor("#6c757d"),
            "success": QColor("#28a745"),
            "danger": QColor("#dc3545"),
            "warning": QColor("#ffc107"),
            "info": QColor("#17a2b8"),
            "background": QColor("#ffffff"),
            "foreground": QColor("#212529"),
            "border": QColor("#dee2e6"),
        }
        
        return default_colors.get(role, QColor("#000000"))
    
    def get_font(self, role: str) -> QFont:
        """根据角色获取字体"""
        # 获取设置中的字体配置
        settings = self.settings_manager.get_ui_settings()
        font_family = settings.get("font_family", "Microsoft YaHei")
        font_size = settings.get("font_size", 10)
        
        # 根据角色调整字体属性
        if role == "title":
            font = QFont(font_family, font_size + 2, QFont.Weight.Bold)
        elif role == "monospace":
            font = QFont("Consolas", font_size)
        else:
            font = QFont(font_family, font_size)
        
        return font
    
    @abstractmethod
    def get_stylesheet(self) -> str:
        """获取主题的QSS样式表 - 抽象方法，子类必须实现"""
        pass
    
    @abstractmethod
    def get_icon(self, name: str) -> QIcon:
        """根据名称获取图标 - 抽象方法，子类必须实现"""
        pass
    
    @abstractmethod
    def apply_to_app(self, app):
        """将主题应用到整个应用程序 - 抽象方法，子类必须实现"""
        pass
    
    @abstractmethod
    def apply_to_widget(self, widget):
        """将主题应用到特定部件 - 抽象方法，子类必须实现"""
        pass
