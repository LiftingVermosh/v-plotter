# src/core/theme_manager.py
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget
from PyQt6.QtCore import QObject
from pathlib import Path
import importlib
import importlib.util
from .base_theme import BaseTheme
from .signals import theme_signals
from .settings_manager import SettingsManager

class ThemeManager(QObject):
    """主题管理器，负责加载、切换和管理主题"""
    
    theme_changed = theme_signals.theme_changed  # 主题更改信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.themes = {}
        self.current_theme = None
        self.settings_manager = SettingsManager()
        self._discover_themes()
        # 自动加载保存的主题
        self.load_saved_theme()
        
        theme_signals.success_changed.connect(self.on_theme_applied)
    
    # 发现并加载所有可用主题
    def _discover_themes(self):
        """发现并加载所有可用主题"""
        themes_dir = Path("src/core/themes")
        
        if not themes_dir.exists():
            QMessageBox.warning(None, "主题管理器", "主题目录不存在！")
            return
        
        # 加载内置主题
        for theme_file in themes_dir.glob("*.py"):
            if theme_file.name != "__init__.py" and not theme_file.name.startswith("_"):
                module_name = f"src.core.themes.{theme_file.stem}"
                # 根据文件名生成类名（例如：light_theme -> LightTheme）
                class_name = f"{theme_file.stem.split('_')[0].capitalize()}Theme"
                
                try:
                    # 动态导入模块
                    spec = importlib.util.spec_from_file_location(module_name, theme_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 获取主题类并实例化
                    theme_class = getattr(module, class_name)
                    theme_instance = theme_class()
                    self.themes[theme_instance.name] = theme_instance
                except (ImportError, AttributeError, FileNotFoundError) as e:
                    QMessageBox.warning(None, "主题管理器", f"加载主题 {theme_file.stem} 失败: {e}")
        
        # 如果没有找到主题，创建默认主题
        if not self.themes:
            QMessageBox.warning(None, "主题管理器", "未找到主题，创建默认主题")
            from .themes.light_theme import LightTheme
            light_theme = LightTheme()
            self.themes[light_theme.name] = light_theme
    
    # 获取可用主题列表
    def get_available_themes(self) -> list:
        """获取可用主题列表"""
        return list(self.themes.keys())
    
    # 获取当前主题名称
    def get_current_theme_name(self):
        """获取当前主题名称"""
        if self.current_theme:
            return self.current_theme.name
        return None

    # 获取指定名称的主题
    def get_theme(self, name: str) -> BaseTheme:
        """获取指定名称的主题"""
        return self.themes.get(name)
    
    # 设置当前主题
    def set_theme(self, name: str, user_initiated=False):
        """设置当前主题，可选是否用户主动触发"""
        if name in self.themes and self.themes[name] != self.current_theme:
            self.current_theme = self.themes[name]
            self.settings_manager.save_theme_setting(name)
            # 应用主题到整个应用和当前活动窗口
            app = QApplication.instance()
            main_window = self.get_main_window()
            success = self.apply_theme(app=app, widget=main_window)
            # 发射主题改变信号，通知其他组件
            self.theme_changed.emit(name)
            return True
        return False
    
    # 应用当前主题
    def apply_theme(self, app=None, widget=None):
        """应用当前主题到应用或部件"""
        if self.current_theme:
            if app:
                self.current_theme.apply_to_app(app)
            if widget:
                # 应用主题
                self.current_theme.apply_to_widget(widget)
            
                # 强制更新菜单栏
                if hasattr(widget, 'menuBar') and widget.menuBar():
                    self.current_theme.apply_to_menu_bar(widget.menuBar())
                
                # 强制更新所有子部件
                self.update_all_children(widget)
            return True
        return False

    
    def update_all_children(self, widget):
        """递归更新所有子部件的样式"""
        for child in widget.findChildren(QWidget):
            try:
                child.style().unpolish(child)
                child.style().polish(child)
                child.update()
            except:
                pass

    def on_theme_applied(self, user_initiated, success):
        """主题应用成功/失败的回调"""
        if success and user_initiated:
            # 成功应用主题，处理额外逻辑
            QMessageBox.information(None, "主题管理器", f"成功应用主题 {self.current_theme.name}")
        elif not success:
            # 应用主题失败，处理额外逻辑
            QMessageBox.warning(None, "主题管理器", f"应用主题 {self.current_theme.name} 失败")

    # 加载保存的主题
    def load_saved_theme(self):
        """从设置中加载保存的主题"""
        saved_theme = self.settings_manager.get_theme_setting()
        available_themes = self.get_available_themes()
        if saved_theme in available_themes:
            self.set_theme(saved_theme, user_initiated=False)
        elif available_themes:
            default_theme = available_themes[0]
            self.set_theme(default_theme, user_initiated=False)
            self.settings_manager.save_theme_setting(default_theme)
    
    # 创建自定义主题
    def create_custom_theme(self, name, stylesheet_path, icon_dir=None):
        """创建自定义主题"""
        # 实现自定义主题创建逻辑
        pass

    def get_main_window(self):
        """获取主窗口实例"""
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                return widget
        return None