# src/core/font_manager.py
from PyQt6.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import os
import platform
from src.core.settings_manager import SettingsManager

def setup_chinese_font(settings=None):
    """
    设置Matplotlib支持中文显示
    参数: settings - 可选的设置字典，如果提供则使用其中的字体设置
    返回: 成功设置的字体系列名称
    """
    # 如果提供了设置，优先使用设置中的字体
    if settings and 'plot_settings' in settings:
        font_family = settings['plot_settings'].get('font_family')
        if font_family and font_family in [f.name for f in fm.fontManager.ttflist]:
            plt.rcParams['font.sans-serif'] = [font_family] + plt.rcParams['font.sans-serif']
            plt.rcParams['axes.unicode_minus'] = False
            return font_family
    
    # 如果没有提供设置或设置中的字体不可用，则使用原来的逻辑
    # 确定操作系统
    system = platform.system()
    
    # 常见的中文字体名称
    chinese_fonts = []
    
    if system == "Windows":
        # Windows系统常见中文字体
        chinese_fonts = [
            "Microsoft YaHei",       # 微软雅黑
            "SimHei",                # 黑体
            "KaiTi",                 # 楷体
            "FangSong",              # 仿宋
            "SimSun",                # 宋体
            "NSimSun",               # 新宋体
        ]
    elif system == "Darwin":  # macOS
        # macOS系统常见中文字体
        chinese_fonts = [
            "PingFang SC",           # 苹方
            "Hiragino Sans GB",      # 冬青黑体
            "STHeiti",               # 华文黑体
            "STKaiti",               # 华文楷体
            "STSong",                # 华文宋体
        ]
    else:  # Linux和其他系统
        # Linux系统常见中文字体
        chinese_fonts = [
            "WenQuanYi Micro Hei",   # 文泉驿微米黑
            "WenQuanYi Zen Hei",     # 文泉驿正黑
            "Noto Sans CJK SC",      # 思源黑体
            "Noto Serif CJK SC",     # 思源宋体
        ]
    
    # 检查系统中可用的中文字体
    available_fonts = set(f.name for f in fm.fontManager.ttflist)
    
    # 尝试设置第一个可用的中文字体
    for font_name in chinese_fonts:
        if font_name in available_fonts:
            plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            return font_name
    
    # 如果没有找到中文字体，尝试使用字体文件
    QMessageBox.warning(None, "警告", "未找到系统中文字体，尝试使用内置字体文件...")
    return setup_chinese_font_with_file()

def setup_chinese_font_with_file():
    """
    通过字体文件设置中文字体
    返回: 成功设置的字体系列名称
    """
    # 常见中文字体文件路径
    font_paths = []
    
    # 根据操作系统确定可能的字体文件路径
    system = platform.system()
    if system == "Windows":
        # Windows字体目录
        font_dir = os.path.join(os.environ['WINDIR'], 'Fonts')
        font_paths = [
            os.path.join(font_dir, 'msyh.ttc'),      # 微软雅黑
            os.path.join(font_dir, 'simhei.ttf'),    # 黑体
            os.path.join(font_dir, 'simkai.ttf'),    # 楷体
            os.path.join(font_dir, 'simfang.ttf'),   # 仿宋
            os.path.join(font_dir, 'simsun.ttc'),    # 宋体
        ]
    elif system == "Darwin":  # macOS
        # macOS字体目录
        font_dir = '/System/Library/Fonts'
        font_paths = [
            os.path.join(font_dir, 'PingFang.ttc'),      # 苹方
            os.path.join(font_dir, 'Hiragino Sans GB.ttc'),  # 冬青黑体
            os.path.join(font_dir, 'STHeiti Light.ttc'), # 华文黑体
            os.path.join(font_dir, 'STKaiti.ttf'),       # 华文楷体
            os.path.join(font_dir, 'STSong.ttf'),        # 华文宋体
        ]
    else:  # Linux和其他系统
        # Linux字体目录
        font_dirs = [
            '/usr/share/fonts',
            '/usr/local/share/fonts',
            os.path.expanduser('~/.fonts'),
        ]
        
        # 在Linux中搜索中文字体文件
        for font_dir in font_dirs:
            if os.path.exists(font_dir):
                for root, dirs, files in os.walk(font_dir):
                    for file in files:
                        if file.lower().endswith(('.ttf', '.ttc', '.otf')):
                            # 检查文件名是否包含中文字体相关关键词
                            if any(keyword in file.lower() for keyword in ['chinese', 'china', 'sim', 'msyh', 'pingfang', 'hiragino', 'noto']):
                                font_paths.append(os.path.join(root, file))
    
    # 尝试加载第一个可用的字体文件
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                # 添加字体到Matplotlib字体管理器
                font_prop = fm.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                
                # 设置默认字体
                plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
                plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
                
                print(f"已通过字体文件设置中文字体: {font_name} ({font_path})")
                return font_name
            except Exception as e:
                print(f"加载字体文件失败: {font_path}, 错误: {e}")
                continue
    
    # 如果所有方法都失败，使用默认字体并打印警告
    print("警告: 无法找到合适的中文字体，中文显示可能不正常")
    return None

# 在模块导入时自动设置中文字体
chinese_font = setup_chinese_font()

# 在模块导入时自动设置中文字体
settings_manager = SettingsManager()
settings = settings_manager.load_settings()
chinese_font = setup_chinese_font(settings)
