# main.py 
# 应用入口

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
import src.ui.main_window as main_window
from src.core.font_manager import setup_chinese_font

def main():
    # 启用高DPI缩放
    # QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    # QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = main_window.MainWindow()
    setup_chinese_font()
    sys.exit(app.exec())



if __name__ == '__main__':
    main()