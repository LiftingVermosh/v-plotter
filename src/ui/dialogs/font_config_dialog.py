# src/ui/dialogs/font_config_dialog.py
# 字体配置对话框

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from PyQt6.QtGui import QFontDatabase
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt

class FontConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("字体配置")
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 获取所有可用字体
        available_fonts = set(f.name for f in fm.fontManager.ttflist)
        chinese_fonts = [f for f in available_fonts if self.is_chinese_font(f)]
        
        # 当前字体标签
        current_font_label = QLabel(f"当前字体: {plt.rcParams['font.sans-serif'][0]}")
        layout.addWidget(current_font_label)
        
        # 字体选择下拉框
        font_layout = QHBoxLayout()
        font_label = QLabel("选择中文字体:")
        self.font_combo = QComboBox()
        self.font_combo.addItems(chinese_fonts)
        
        # 设置当前选中的字体
        current_font = plt.rcParams['font.sans-serif'][0]
        if current_font in chinese_fonts:
            self.font_combo.setCurrentText(current_font)
        
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_combo)
        layout.addLayout(font_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        apply_button = QPushButton("应用")
        apply_button.clicked.connect(self.apply_font)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(apply_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
    
    def is_chinese_font(self, font_name):
        """检查字体是否支持中文"""
        # 常见中文字体关键词
        chinese_keywords = ['sim', 'ms', 'pingfang', 'hiragino', 'noto', 'st', '华文', '宋体', '黑体', '楷体', '仿宋']
        return any(keyword.lower() in font_name.lower() for keyword in chinese_keywords)
    
    def apply_font(self):
        """应用选中的字体"""
        selected_font = self.font_combo.currentText()
        try:
            plt.rcParams['font.sans-serif'] = [selected_font] + plt.rcParams['font.sans-serif']
            plt.rcParams['axes.unicode_minus'] = False
            QMessageBox.information(self, "成功", f"已设置字体为: {selected_font}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"设置字体失败: {str(e)}")
