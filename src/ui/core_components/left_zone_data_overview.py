# src/ui/core_components/left_zone_data_overview.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QTreeWidget, QTreeWidgetItem,
    QHeaderView, QHBoxLayout, QAbstractItemView, QMenu, QStyledItemDelegate, QStyle
)
from PyQt6.QtGui import QIcon, QFont, QPixmap, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QRect
from src.core.signals import container_signals, tab_signals

class DataListItemDelegate(QStyledItemDelegate):
    """自定义委托用于美化列表项"""
    def paint(self, painter, option, index):
        # 设置背景色
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, QColor(200, 230, 255))  # 选中项背景色
        else:
            painter.fillRect(option.rect, QColor(240, 240, 240))  # 默认背景色
        
        # 绘制边框
        painter.setPen(QColor(200, 200, 200))
        painter.drawRect(option.rect)
        
        # 绘制文本
        super().paint(painter, option, index)

class LeftZoneDataOverview(QWidget):
    """左侧数据概览区 - 详细信息视图风格"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_map = {}  # {container_uuid: QTreeWidgetItem}
        self.init_ui()
        self.connect_signals()
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
    
    
    def init_ui(self):
        """初始化UI - 详细信息视图风格"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # 添加分隔线
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        
        # 创建列表视图
        self.list_widget = QTreeWidget(self)
        self.list_widget.setHeaderHidden(True)  # 隐藏表头
        self.list_widget.setRootIsDecorated(False)  # 隐藏根装饰
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.list_widget.setIndentation(0)  # 无缩进
        
        # 设置自定义委托
        delegate = DataListItemDelegate(self.list_widget)
        self.list_widget.setItemDelegate(delegate)
        
        main_layout.addWidget(self.list_widget)
    
    def connect_signals(self):
        """连接信号"""
        # 容器就绪信号 - 添加新项
        container_signals.container_ready.connect(self.add_data_item)
        
        # 标签页创建信号 - 更新项名称
        tab_signals.table_tab_created.connect(self.update_item_name)
        
        # 标签页关闭信号 - 移除项
        tab_signals.table_tab_closed.connect(self.remove_data_item)

        tab_signals.thumbnnail_closed.connect(self.remove_data_item)
        
        # 列表项选择信号
        self.list_widget.itemSelectionChanged.connect(self.handle_selection_change)
    
    def create_thumbnail_pixmap(self):
        """创建缩略图预览（占位符）"""
        pixmap = QPixmap(40, 40)
        pixmap.fill(QColor(200, 230, 255))  # 浅蓝色背景
        return pixmap
    
    def add_data_item(self, container):
        """添加新的数据项"""
        # 检查是否已存在
        if container.uuid in self.data_map:
            return
        
        # 创建列表项
        item = QTreeWidgetItem(self.list_widget)
        item.setData(0, Qt.ItemDataRole.UserRole, container.uuid)
        
        # 设置自定义控件
        item_widget = QWidget()
        layout = QHBoxLayout(item_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # 缩略图
        icon_label = QLabel()
        icon_label.setPixmap(self.create_thumbnail_pixmap())
        icon_label.setFixedSize(40, 40)
        icon_label.setScaledContents(True)
        layout.addWidget(icon_label)
        
        # 详细信息
        details_layout = QVBoxLayout()
        details_layout.setSpacing(3)
        
        # 名称
        name_label = QLabel(container.name)
        name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        details_layout.addWidget(name_label)
        
        # 类型和大小
        type_label = QLabel(f"类型: {container.data_type}")
        type_label.setFont(QFont("Arial", 8))
        type_label.setStyleSheet("color: #666666;")
        details_layout.addWidget(type_label)
        
        layout.addLayout(details_layout)
        layout.addStretch()  # 添加弹性空间
        
        # 设置自定义控件
        self.list_widget.setItemWidget(item, 0, item_widget)
        
        # 添加到列表
        self.list_widget.addTopLevelItem(item)
        
        # 存储映射关系
        self.data_map[container.uuid] = item
    
    def update_item_name(self, container_uuid, new_name):
        """更新项显示的名称"""
        if container_uuid in self.data_map:
            item = self.data_map[container_uuid]
            widget = self.list_widget.itemWidget(item, 0)
            if widget:
                # 找到名称标签并更新
                name_label = widget.findChild(QLabel)
                if name_label:
                    name_label.setText(new_name)
    
    def remove_data_item(self, container_uuid):
        """移除数据项"""
        try:
            if container_uuid in self.data_map:
                item = self.data_map.pop(container_uuid)
                index = self.list_widget.indexOfTopLevelItem(item)
                if index >= 0:
                    # 先移除自定义控件，避免内存泄漏
                    widget = self.list_widget.itemWidget(item, 0)
                    if widget:
                        widget.deleteLater()
                    
                    # 移除项
                    self.list_widget.takeTopLevelItem(index)
                    
                # 删除项
                del item
        except Exception as e:
            print(f"移除数据项时出错: {e}")

    def handle_selection_change(self):
        """处理列表项选择变化"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        container_uuid = item.data(0, Qt.ItemDataRole.UserRole)
        
        # 激活对应的表格标签页
        tab_signals.activate_table_tab.emit(container_uuid)

    ## 右键菜单
    def show_context_menu(self, pos):
        """显示右键菜单"""
        item = self.list_widget.itemAt(pos)
        if not item:
            return
        
        menu = QMenu(self)
        
        # 重命名操作
        rename_action = menu.addAction("重命名")
        rename_action.triggered.connect(lambda: self.rename_data_item(item))
        
        # 关闭操作
        close_action = menu.addAction("关闭")
        close_action.triggered.connect(lambda: self.close_data_item(item))
        
        menu.addSeparator()
        
        # 复制操作
        copy_action = menu.addAction("复制数据")
        copy_action.triggered.connect(lambda: self.copy_data_item(item))
        
        menu.exec(self.list_widget.mapToGlobal(pos))
    
    def rename_data_item(self, item):
        """重命名数据项"""
        container_uuid = item.data(0, Qt.ItemDataRole.UserRole)
        # 实现重命名逻辑...
        pass
    
    def close_data_item(self, item):
        """关闭数据项"""
        container_uuid = item.data(0, Qt.ItemDataRole.UserRole)
        tab_signals.table_tab_closed.emit(container_uuid)
    
    def copy_data_item(self, item):
        """复制数据项"""
        container_uuid = item.data(0, Qt.ItemDataRole.UserRole)
        # 实现复制逻辑...
        pass