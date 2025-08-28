# src/core/core_manager.py

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import Qt

class Command:
    """命令基类"""
    def execute(self):
        raise NotImplementedError()
    def undo(self):
        raise NotImplementedError()
    
class CommandManager(QObject):
    """命令管理器"""
    command_executed = pyqtSignal()  # 命令执行信号
    command_undone = pyqtSignal()    # 命令撤销信号
    command_redone = pyqtSignal()    # 命令重做信号

    def __init__(self):
        super().__init__()
        self.undo_stack = []        # 撤销栈
        self.redo_stack = []        # 重做栈

    def execute(self, command):
        """执行命令"""
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()
        self.command_executed.emit()

    def undo(self):
        """撤销命令"""
        if not self.undo_stack:
            return
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)
        self.command_undone.emit()

    def redo(self):
        """重做命令"""
        if not self.redo_stack:
            return
        command = self.redo_stack.pop()
        command.execute()
        self.undo_stack.append(command)
        self.command_redone.emit()

    @property
    def can_undo(self):
        """是否可以撤销"""
        return len(self.undo_stack) > 0
    
    @property
    def can_redo(self):
        """是否可以重做"""
        return len(self.redo_stack) > 0

class EditCellCommand(Command):
    """编辑单元格命令"""
    def __init__(self, model, index, old_value, new_value):
        super().__init__()
        self.model = model
        self.index = index  # QModelIndex
        self.old_value = old_value
        self.new_value = new_value

    def execute(self):
        self.model.setData(self.index, self.new_value, Qt.ItemDataRole.EditRole)

    def undo(self):
        self.model.setData(self.index, self.old_value, Qt.ItemDataRole.EditRole)


class AddRowCommand(Command):
    """添加行命令"""
    def __init__(self, model, row):
        super().__init__()
        self.model = model
        self.row = row  # 插入的行索引

    def execute(self):
        self.model.insertRow(self.row)

    def undo(self):
        self.model.removeRow(self.row)


class RemoveRowCommand(Command):
    """删除行命令"""
    def __init__(self, model, row):
        super().__init__()
        self.model = model
        self.row = row
        # 存储被删除行的数据，用于撤销
        self.old_data = self.model._data[row].copy()  # 假设模型有 _data 属性
        self.old_headers = self.model._headers.copy()  # 存储头信息

    def execute(self):
        self.model.removeRow(self.row)

    def undo(self):
        # 重新插入行并恢复数据
        self.model.insertRow(self.row)
        for col in range(self.model.columnCount()):
            index = self.model.index(self.row, col)
            self.model.setData(index, self.old_data[col], Qt.ItemDataRole.EditRole)
        self.model._headers = self.old_headers  # 恢复头信息（如果需要）


class AddColumnCommand(Command):
    """添加列命令"""
    def __init__(self, model, col, header=None):
        super().__init__()
        self.model = model
        self.col = col  # 插入的列索引
        self.header = header

    def execute(self):
        self.model.insertColumn(self.col, self.header)

    def undo(self):
        self.model.removeColumn(self.col)


class RemoveColumnCommand(Command):
    """删除列命令"""
    def __init__(self, model, col):
        super().__init__()
        self.model = model
        self.col = col
        # 存储被删除列的数据和头信息
        self.old_data = self.model._data[:, col].copy()  # 存储列数据
        self.old_header = self.model._headers[col]  # 存储头

    def execute(self):
        self.model.removeColumn(self.col)

    def undo(self):
        # 重新插入列并恢复数据
        self.model.insertColumn(self.col, self.old_header)
        for row in range(self.model.rowCount()):
            index = self.model.index(row, self.col)
            self.model.setData(index, self.old_data[row], Qt.ItemDataRole.EditRole)
