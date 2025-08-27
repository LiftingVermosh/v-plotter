# src/core/core_manager.py

from PyQt6.QtCore import QObject, pyqtSignal

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