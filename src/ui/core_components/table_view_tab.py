# src/ui/core_components/table_view_tab.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableView, QAbstractItemView, 
                             QPushButton, QHBoxLayout, QHeaderView, QMessageBox,
                             QInputDialog, QMenu, QLineEdit, QStyledItemDelegate,
                             QApplication, QStyleOptionViewItem, QStyle)
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QPoint
from PyQt6.QtGui import QKeySequence, QShortcut, QClipboard, QBrush, QColor
from src.core.signals import data_signals
import numpy as np
import re

class NumericDelegate(QStyledItemDelegate):
    """自定义委托，支持第一列字符串输入，其他列数值验证"""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        col = index.column()
        if col == 0:  # 第一列，左对齐 for string
            editor.setAlignment(Qt.AlignmentFlag.AlignLeft)
        else:  # 其他列，右对齐 for number
            editor.setAlignment(Qt.AlignmentFlag.AlignRight)
        return editor
    
    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        editor.setText(str(value))
    
    def setModelData(self, editor, model, index):
        text = editor.text().strip()
        col = index.column()
        if col == 0:  # 第一列，直接设置文本
            model.setData(index, text, Qt.ItemDataRole.EditRole)
        else:  # 其他列，尝试转换为float
            if text:
                try:
                    value = float(text)
                    model.setData(index, value, Qt.ItemDataRole.EditRole)
                except ValueError:
                    # 转换失败，保留原始值（不更新）
                    pass
            else:
                model.setData(index, 0.0, Qt.ItemDataRole.EditRole)  # 空文本设置为0.0

class TableModel(QAbstractTableModel):
    """自定义表格模型，第一列支持字符串，其他列支持数值"""
    def __init__(self, data=None, headers=None, parent=None):
        super().__init__(parent)
        self._headers = headers or ["列1", "列2"]
        
        # 使用对象类型数组支持混合类型
        if data is not None:
            if len(data.shape) == 1:
                data = data.reshape(-1, 1)
            self._data = data.astype(object)  # 改为对象类型
        else:
            # 创建默认空表格，第一列为空字符串，其他为0.0
            self._data = np.empty((5, len(self._headers)), dtype=object)
            for i in range(self._data.shape[0]):
                for j in range(self._data.shape[1]):
                    if j == 0:
                        self._data[i, j] = ''  # 第一列空字符串
                    else:
                        self._data[i, j] = 0.0  # 其他列0.0
        
        self.modified = False
    
    def rowCount(self, parent=QModelIndex()):
        return self._data.shape[0]
    
    def columnCount(self, parent=QModelIndex()):
        return self._data.shape[1]
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        row, col = index.row(), index.column()
        
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[row, col])
        elif role == Qt.ItemDataRole.EditRole:
            return self._data[row, col]
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if col == 0:  # 第一列，左对齐
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            else:  # 其他列，右对齐
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        elif role == Qt.ItemDataRole.BackgroundRole and self.modified:
            return QBrush(QColor(255, 255, 200))  # 修改过的单元格淡黄色背景
        
        return None
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole and index.isValid():
            row, col = index.row(), index.column()
            old_value = self._data[row, col]
            
            # 根据列索引处理值
            if col == 0:  # 第一列，存储字符串
                new_value = str(value) if value != "" else ""
            else:  # 其他列，尝试转换为float
                try:
                    new_value = float(value) if value != "" else 0.0
                except ValueError:
                    return False  # 转换失败，不更新
            
            if new_value != old_value:
                self._data[row, col] = new_value
                self.modified = True
                self.dataChanged.emit(index, index, [role])
                data_signals.data_modified.emit(self._data.copy(), self._headers.copy())   
                return True
        return False
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """ 表头数据 """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)  # 行号从1开始
        return None
    
    def setHeaderData(self, section, orientation, value, role=Qt.ItemDataRole.EditRole):
        """ 设置表头数据 """
        if role == Qt.ItemDataRole.EditRole and orientation == Qt.Orientation.Horizontal:
            if 0 <= section < len(self._headers):
                self._headers[section] = value
                self.headerDataChanged.emit(orientation, section, section)
                self.modified = True
                return True
        return False
    
    def flags(self, index):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable
    
    # 行列操作
    def insertRow(self, row):
        self.beginInsertRows(QModelIndex(), row, row)
        
        # 创建新行，第一列为空字符串，其他为0.0
        new_row = np.empty(self.columnCount(), dtype=object)
        for j in range(self.columnCount()):
            if j == 0:
                new_row[j] = ''
            else:
                new_row[j] = 0.0
        
        # 插入新行
        self._data = np.insert(self._data, row, new_row, axis=0)
        
        self.endInsertRows()
        self.modified = True
        data_signals.data_modified.emit(self._data.copy(), self._headers.copy())   
        return True
    
    def removeRow(self, row):
        if self.rowCount() <= 1:
            return False
            
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data = np.delete(self._data, row, axis=0)
        self.endRemoveRows()
        self.modified = True
        data_signals.data_modified.emit(self._data.copy(), self._headers.copy())   
        return True
    
    def insertColumn(self, col, header=None):
        if header is None:
            y_cols = [h for h in self._headers if h.startswith("列")]
            max_num = max([int(re.search(r'\d+', h).group()) for h in y_cols if re.search(r'\d+', h)] or [0])
            header = f"列{max_num + 1}"
        
        self.beginInsertColumns(QModelIndex(), col, col)
        
        # 创建新列，默认值: 如果插入位置是0（第一列），则为空字符串，否则0.0
        default_value = '' if col == 0 else 0.0
        new_column = np.full(self.rowCount(), default_value, dtype=object)
        
        self._data = np.insert(self._data, col, new_column, axis=1)
        self._headers.insert(col, header)
        self.endInsertColumns()
        self.modified = True
        data_signals.data_modified.emit(self._data.copy(), self._headers.copy())   
        return True
    
    def removeColumn(self, col):
        if self.columnCount() <= 1:
            return False
            
        self.beginRemoveColumns(QModelIndex(), col, col)
        self._data = np.delete(self._data, col, axis=1)
        self._headers.pop(col)
        self.endRemoveColumns()
        self.modified = True
        data_signals.data_modified.emit(self._data.copy(), self._headers.copy())   
        return True
    
    def get_data(self):
        """返回表格数据和列标题"""
        return self._data.copy(), self._headers.copy()
    
    def clear_modified(self):
        """清除修改状态"""
        self.modified = False


class TableViewTab(QWidget):
    """ 单个表格视图标签页 """
    def __init__(self, container, parent=None):
        super().__init__(parent)
        self.container = container
        self.model = None
        self.init_ui()
        self.setup_shortcuts()
        data_signals.data_modified.connect(self.update_container_data)

    def update_container_data(self, data, headers):
        """更新容器数据"""
        self.container.set_table_data(data, headers)

        # 调试行为
        # print(f"数据已更新至容器: {self.container.uuid}\n内容:\n{headers}\n{data} ")

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)

        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 行列操作按钮
        self.add_row_btn = QPushButton("添加行 (Ctrl+Shift+R)")
        self.add_row_btn.clicked.connect(self.add_row)
        
        self.remove_row_btn = QPushButton("删除行 (Ctrl+Shift+D)")
        self.remove_row_btn.clicked.connect(self.remove_row)

        self.add_col_btn = QPushButton("添加列(Ctrl+Shift+C)")
        self.add_col_btn.clicked.connect(self.add_column)

        self.remove_col_btn = QPushButton("删除列(Ctrl+Shift+X)")
        self.remove_col_btn.clicked.connect(self.remove_column)

        button_layout.addWidget(self.add_row_btn)
        button_layout.addWidget(self.remove_row_btn)
        button_layout.addWidget(self.add_col_btn)
        button_layout.addWidget(self.remove_col_btn)

        # 表格视图
        self.tableView = QTableView()
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.tableView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # 启用表头编辑
        self.tableView.horizontalHeader().setSectionsClickable(True)
        self.tableView.horizontalHeader().sectionDoubleClicked.connect(self.edit_header)
        
        # 设置右键菜单
        self.tableView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.show_context_menu)
        
        # 初始化模型
        self.model = TableModel()
        self.tableView.setModel(self.model)
        
        # 设置自定义委托
        self.delegate = NumericDelegate()
        self.tableView.setItemDelegate(self.delegate)
        
        layout.addLayout(button_layout)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
    
    def setup_shortcuts(self):
        """设置键盘快捷键"""
        # 添加行: Ctrl+Shift+R
        QShortcut(QKeySequence("Ctrl+Shift+R"), self).activated.connect(self.add_row)
        
        # 删除行: Ctrl+Shift+D
        QShortcut(QKeySequence("Ctrl+Shift+D"), self).activated.connect(self.remove_row)
        
        # 添加列: Ctrl+Shift+C
        QShortcut(QKeySequence("Ctrl+Shift+C"), self).activated.connect(self.add_column)
        
        # 删除列: Ctrl+Shift+X
        QShortcut(QKeySequence("Ctrl+Shift+X"), self).activated.connect(self.remove_column)

        # 全选: Ctrl+A
        QShortcut(QKeySequence("Ctrl+A"), self).activated.connect(self.select_all)
        
        # 清除选择: Esc
        QShortcut(QKeySequence("Esc"), self).activated.connect(self.clear_selection)

        # 清除内容: Del
        QShortcut(QKeySequence("Del"), self).activated.connect(self.clear_insertion)
        
        # 复制: Ctrl+C
        QShortcut(QKeySequence("Ctrl+C"), self).activated.connect(self.copy_selection)

        # 粘贴: Ctrl+V
        QShortcut(QKeySequence("Ctrl+V"), self).activated.connect(self.paste_to_selection)
    
    def load_data(self):
        """从容器加载数据，支持混合类型"""
        if self.container and self.container.table_data is not None:
            data_array = self.container.get_table_data_as_numpy()
            headers = self.container.column_headers
            
            if len(data_array.shape) == 1:
                data_array = data_array.reshape(-1, 1)
            
            # 不再强制转换为float，直接使用对象类型
            self.model.beginResetModel()
            self.model._data = data_array.astype(object)  # 确保对象类型
            self.model._headers = headers
            self.model.endResetModel()
            
            self.model.clear_modified()
            
    
    def update_properties(self, properties):
        """更新属性并刷新视图"""
        # 这里可以根据properties更新表格显示
        pass
    
    # 表头编辑方法
    def edit_header(self, section):
        """编辑指定列的表头"""
        current_header = self.model.headerData(section, Qt.Orientation.Horizontal)
        new_header, ok = QInputDialog.getText(
            self, 
            "编辑列标题", 
            "请输入新的列标题:", 
            text=current_header
        )
        
        if ok and new_header and new_header != current_header:
            self.model.setHeaderData(section, Qt.Orientation.Horizontal, new_header)
    
    def edit_selected_header(self):
        """编辑选中列的表头"""
        selected_indexes = self.tableView.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "操作错误", "请先选择要编辑的列")
            return
        
        # 获取所有选中列的索引（去重）
        cols_to_edit = set(index.column() for index in selected_indexes)
        
        for col in cols_to_edit:
            self.edit_header(col)
    
    # 行列操作方法
    def add_row(self):
        """在选中区域下方添加新行"""
        selected_indexes = self.tableView.selectedIndexes()
        row = max(index.row() for index in selected_indexes) + 1 if selected_indexes else self.model.rowCount()
        self.model.insertRow(row)
    
    def remove_row(self):
        """删除所有选中行"""
        selected_indexes = self.tableView.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "操作错误", "请先选择要删除的行")
            return
        
        # 获取所有选中行的索引（去重）
        rows_to_remove = sorted(set(index.row() for index in selected_indexes), reverse=True)
        
        if self.model.rowCount() <= len(rows_to_remove):
            QMessageBox.warning(self, "操作错误", "至少需要保留一行")
            return
        
        # 从大到小删除，避免索引变化导致错误
        for row in rows_to_remove:
            self.model.removeRow(row)
    
    def add_column(self):
        """在选中区域右侧添加新列"""
        selected_indexes = self.tableView.selectedIndexes()
        col = max(index.column() for index in selected_indexes) + 1 if selected_indexes else self.model.columnCount()
        self.model.insertColumn(col)
    
    def remove_column(self):
        """删除所有选中列"""
        selected_indexes = self.tableView.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "操作错误", "请先选择要删除的列")
            return
        
        # 获取所有选中列的索引（去重）
        cols_to_remove = sorted(set(index.column() for index in selected_indexes), reverse=True)
        
        if self.model.columnCount() <= len(cols_to_remove):
            QMessageBox.warning(self, "操作错误", "至少需要保留一列")
            return
        
        # 从大到小删除，避免索引变化导致错误
        for col in cols_to_remove:
            self.model.removeColumn(col)
    
    def select_rows(self):
        """选择所有选中单元格所在的行"""
        selected_indexes = self.tableView.selectedIndexes()
        if not selected_indexes:
            return
        
        rows = set(index.row() for index in selected_indexes)
        self.tableView.clearSelection()
        
        for row in rows:
            self.tableView.selectRow(row)
    
    def select_columns(self):
        """选择所有选中单元格所在的列"""
        selected_indexes = self.tableView.selectedIndexes()
        if not selected_indexes:
            return
        
        cols = set(index.column() for index in selected_indexes)
        self.tableView.clearSelection()
        
        for col in cols:
            self.tableView.selectColumn(col)
    
    def select_all(self):
        """选择所有单元格"""
        self.tableView.selectAll()
    
    def clear_selection(self):
        """清除选择"""
        self.tableView.clearSelection()
    
    def clear_insertion(self):
        """清除选中单元格的输入内容"""
        selected_indexes = self.tableView.selectedIndexes()
        if not selected_indexes:
            return
        
        for index in selected_indexes:
            self.model.setData(index, "", Qt.ItemDataRole.EditRole)
    
    # 复制/粘贴功能
    def copy_selection(self):
        """复制选中内容到剪贴板"""
        selected_indexes = self.tableView.selectedIndexes()
        if not selected_indexes:
            return
        
        # 确定选区范围
        rows = sorted(set(index.row() for index in selected_indexes))
        cols = sorted(set(index.column() for index in selected_indexes))
        
        # 构建表格数据字符串
        clipboard_data = ""
        for r in rows:
            row_data = []
            for c in cols:
                if self.tableView.model().index(r, c) in selected_indexes:
                    value = self.tableView.model().data(self.tableView.model().index(r, c), Qt.ItemDataRole.DisplayRole)
                    row_data.append(str(value))
                else:
                    row_data.append("")
            clipboard_data += "\t".join(row_data) + "\n"
        
        # 复制到剪贴板
        QApplication.clipboard().setText(clipboard_data.strip())
    
    def paste_to_selection(self):
        """从剪贴板粘贴数据到选中区域"""
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text().strip()
        if not clipboard_text:
            return
        
        # 获取选中区域的起始位置
        selected_indexes = self.tableView.selectedIndexes()
        if not selected_indexes:
            return
        
        start_row = min(index.row() for index in selected_indexes)
        start_col = min(index.column() for index in selected_indexes)
        
        # 解析剪贴板数据
        rows = clipboard_text.split('\n')
        data = [row.split('\t') for row in rows]
        
        # 粘贴数据
        model = self.tableView.model()
        for r, row in enumerate(data):
            for c, value in enumerate(row):
                target_row = start_row + r
                target_col = start_col + c
                
                # 确保目标位置有效
                if target_row < model.rowCount() and target_col < model.columnCount():
                    model.setData(model.index(target_row, target_col), value, Qt.ItemDataRole.EditRole)
    
    # 右键菜单功能
    def show_context_menu(self, pos):
        """显示右键菜单"""
        menu = QMenu(self)
        
        # 添加编辑操作
        edit_action = menu.addAction("编辑单元格")
        edit_action.triggered.connect(self.edit_current_cell)
        
        edit_header_action = menu.addAction("编辑列标题")
        edit_header_action.triggered.connect(self.edit_current_header)
        
        menu.addSeparator()
        
        # 添加复制粘贴操作
        copy_action = menu.addAction("复制")
        copy_action.triggered.connect(self.copy_selection)
        
        paste_action = menu.addAction("粘贴")
        paste_action.triggered.connect(self.paste_to_selection)
        
        menu.addSeparator()
        
        # 添加行列操作
        add_row_action = menu.addAction("添加行")
        add_row_action.triggered.connect(self.add_row)
        
        remove_row_action = menu.addAction("删除行")
        remove_row_action.triggered.connect(self.remove_row)
        
        add_col_action = menu.addAction("添加列")
        add_col_action.triggered.connect(self.add_column)
        
        remove_col_action = menu.addAction("删除列")
        remove_col_action.triggered.connect(self.remove_column)
        
        # 显示菜单
        global_pos = self.tableView.viewport().mapToGlobal(pos)
        menu.exec(global_pos)
    
    def edit_current_cell(self):
        """编辑当前选中单元格"""
        selected_indexes = self.tableView.selectedIndexes()
        if selected_indexes:
            self.tableView.edit(selected_indexes[0])
    
    def edit_current_header(self):
        """编辑当前选中列的标题"""
        selected_indexes = self.tableView.selectedIndexes()
        if selected_indexes:
            col = selected_indexes[0].column()
            self.edit_header(col)
    
    def get_table_data(self):
        """获取表格数据"""
        return self.model.get_data()
