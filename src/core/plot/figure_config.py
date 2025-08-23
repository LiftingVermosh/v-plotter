# src/core/figure_config.py

import configparser
import os

class AppConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = "config.ini"
        self.default_settings = {
            'plot': {
                'dpi': '100',
                'figwidth': '10',
                'figheight': '6',
                'linewidth': '2',
                'markersize': '6',
                'fontsize': '10',
                'antialiasing': 'True'
            }
        }
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置文件"""
        self.config['DEFAULT'] = {}
        for section, options in self.default_settings.items():
            self.config[section] = options
        self.save_config()
    
    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
    
    def get_plot_setting(self, key):
        """获取绘图设置"""
        try:
            return self.config.getfloat('plot', key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return float(self.default_settings['plot'][key])

# 全局配置实例
app_config = AppConfig()
