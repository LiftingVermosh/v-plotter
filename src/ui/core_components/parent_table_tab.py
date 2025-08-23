# src/ui/core_components/parent_table_tab.py
from PyQt6.QtWidgets import QTabWidget, QWidget, QMessageBox
from .table_view_tab import TableViewTab
from src.core.signals import tab_signals, container_signals
from src.core.data_container import DataContainer
import uuid

class ParentTableTab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tab_map = {}  # {container_uuid: {"widget": TableViewTab, "container": dict}}
        self.name = "表格父标签页"

        # 初始欢迎页
        self.welcome_tab = QWidget()
        self.addTab(self.welcome_tab, "默认表格页")
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.handle_tab_close_by_index)
        
        # 信号连接
        container_signals.container_ready.connect(self.create_sub_tab)      # 数据容器准备就绪信号
        tab_signals.table_tab_created.connect(self.activate_tab)             # 表格子标签页创建信号 
        tab_signals.activate_table_tab.connect(self.activate_tab)            # 激活表格子标签页信号
        container_signals.container_created.connect(self.on_container_created)  # 数据容器创建信号
        tab_signals.table_tab_closed.connect(self.handle_tab_close_by_uuid)           # 表格子标签页关闭信号

    
    def on_container_created(self):
        cur_container = DataContainer()
        cur_container.name = f"数据组{len(self.tab_map) + 1}"
        if not cur_container:
            # print("当前容器为空")
            fail_to_create = QMessageBox.warning(self, "错误", "创建数据容器失败")
            return
        container_signals.container_ready.emit(cur_container)
        # print("容器已创建")
    
    def create_sub_tab(self, container):
        """创建或激活表格子标签页"""
        # 确保容器有UUID
        container_uuid = container.uuid
        
        # 检查是否已存在
        if container_uuid in self.tab_map:
            self.activate_tab(container_uuid)
            return
        
        # 创建新的表格视图
        table_view = TableViewTab(container)
        tab_name = container.name if container.name else f"数据表 {len(self.tab_map) + 1}"
        
        # 添加到标签页
        index = self.addTab(table_view, tab_name)
        self.setCurrentIndex(index)
        
        # 存储到映射
        self.tab_map[container_uuid] = {
            "widget": table_view,
            "container": container,
            "index": index
        }
        
        # 加载数据
        table_view.load_data()
        
        # 发射创建信号
        tab_signals.table_tab_created.emit(container_uuid, tab_name)
        # print(f"创建表格子标签页: {tab_name}")
    
    def activate_tab(self, container_uuid):
        """通过UUID激活标签页"""
        if container_uuid in self.tab_map:
            tab_info = self.tab_map[container_uuid]
            self.setCurrentIndex(tab_info["index"])
    
    def activate_tab_by_container(self, container):
        """通过容器对象激活标签页"""
        container_uuid = container.get('uuid')
        if container_uuid in self.tab_map:
            self.activate_tab(container_uuid)
    
    def update_current_tab_properties(self, properties):
        """更新当前活动标签页的属性"""
        current_widget = self.currentWidget()
        if current_widget and hasattr(current_widget, 'update_properties'):
            current_widget.update_properties(properties)
    
    def handle_tab_close_by_uuid(self, uuid):
        """通过UUID关闭标签页"""
        closed_widget_uuid = uuid
        # 查找对应的Index
        container_index = None
        for uuid_str, info in self.tab_map.items():
            if uuid_str == closed_widget_uuid:
                container_index = info["index"]
                break
        if container_index:
            # 从映射中移除
            del self.tab_map[closed_widget_uuid]
        
            # 移除标签页
            self.removeTab(container_index)
        else:
            print(f"未找到UUID为{closed_widget_uuid}的标签页")
        
        # 更新剩余标签页的索引
        for info in self.tab_map.values():
            if info["index"] > container_index:
                info["index"] -= 1
    
    def handle_tab_close_by_index(self, index):
        """通过索引关闭标签页"""
        close_widget = self.widget(index)

        if close_widget == self.welcome_tab:
            self.removeTab(index)
            return
        
        # 查找对应uuid
        container_uuid = None
        for uuid_str, info in self.tab_map.items():
            if info["widget"] == close_widget:
                container_uuid = uuid_str
                break
        if container_uuid:
            # 移除标签页
            self.removeTab(index)
            
            # 从映射中移除
            del self.tab_map[container_uuid]
            
            # 更新剩余标签页的索引
            for info in self.tab_map.values():
                if info["index"] > index:
                    info["index"] -= 1
            
            # 通知其他组件
            tab_signals.thumbnnail_closed.emit(container_uuid)
            
        else:
            print(f"未找到索引为{index}的标签页")
    
    def handle_tab_close_by_container(self, container):
        """通过容器对象关闭标签页"""
        container_uuid = container.get('uuid')
        if container_uuid in self.tab_map:
            tab_signals.table_tab_closed.emit(container_uuid)
