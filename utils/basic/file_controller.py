# -*- coding: utf-8 -*-
"""
@file:      file_controller
@time:      2025/9/28 02:33
@author:    sMythicalBird
"""
# file_controller.py
import os
import json
import csv
import pickle
from pathlib import Path
from typing import Any, Dict, List, Union, Optional
from threading import Lock

# 类型别名（现代 Python 风格）
FilePath = str | Path
Data = Dict[str, Any] | List[Any] | Any


class FileOperationError(Exception):
    """自定义文件操作异常"""
    pass


class FileController:
    """
    单例文件操作控制器
    提供统一的文件读写接口
    """

    _instance = None
    _lock = Lock()  # 线程安全

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(FileController, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._operation_history: list[str] = []  # 可选：记录操作历史

    # —————————————————— 工具方法 ——————————————————

    def _ensure_dir(self, file_path: FilePath) -> Path:
        """确保目录存在"""
        path = Path(file_path)
        directory = path.parent
        if directory and not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        return path

    def _log_operation(self, operation: str) -> None:
        """记录操作（可选功能）"""
        self._operation_history.append(operation)

    # —————————————————— 基础操作 ——————————————————

    def exists(self, file_path: FilePath) -> bool:
        """检查文件是否存在"""
        return Path(file_path).exists()

    def is_file(self, file_path: FilePath) -> bool:
        """检查是否为文件"""
        return Path(file_path).is_file()

    def get_size(self, file_path: FilePath) -> int:
        """获取文件大小（字节）"""
        if not self.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        return Path(file_path).stat().st_size

    def get_ext(self, file_path: FilePath) -> str:
        """获取扩展名（小写）"""
        return Path(file_path).suffix.lower()

    def delete(self, file_path: FilePath) -> bool:
        """删除文件"""
        try:
            Path(file_path).unlink(missing_ok=True)
            self._log_operation(f"DELETE: {file_path}")
            return True
        except Exception as e:
            raise FileOperationError(f"删除文件失败: {file_path}") from e

    # —————————————————— 读写操作 ——————————————————

    def read_text(self, file_path: FilePath, encoding: str = 'utf-8') -> str:
        """读取文本"""
        try:
            path = Path(file_path)
            content = path.read_text(encoding=encoding)
            self._log_operation(f"READ TEXT: {file_path}")
            return content
        except Exception as e:
            raise FileOperationError(f"读取文本失败: {file_path}") from e

    def write_text(self, content: str, file_path: FilePath, encoding: str = 'utf-8') -> None:
        """写入文本"""
        try:
            path = self._ensure_dir(file_path)
            path.write_text(content, encoding=encoding)
            self._log_operation(f"WRITE TEXT: {file_path}")
        except Exception as e:
            raise FileOperationError(f"写入文本失败: {file_path}") from e

    def append_text(self, content: str, file_path: FilePath, encoding: str = 'utf-8') -> None:
        """追加文本"""
        try:
            path = Path(file_path)
            with path.open('a', encoding=encoding) as f:
                f.write(content + '\n')
            self._log_operation(f"APPEND TEXT: {file_path}")
        except Exception as e:
            raise FileOperationError(f"追加文本失败: {file_path}") from e

    # —————————————————— JSON ——————————————————

    def read_json(self, file_path: FilePath, encoding: str = 'utf-8') -> dict | list:
        """读取 JSON"""
        try:
            content = self.read_text(file_path, encoding)
            data = json.loads(content)
            self._log_operation(f"READ JSON: {file_path}")
            return data
        except Exception as e:
            raise FileOperationError(f"读取 JSON 失败: {file_path}") from e

    def write_json(
        self,
        data: dict | list,
        file_path: FilePath,
        encoding: str = 'utf-8',
        indent: int = 2
    ) -> None:
        """写入 JSON"""
        try:
            content = json.dumps(data, ensure_ascii=False, indent=indent)
            self.write_text(content, file_path, encoding)
            self._log_operation(f"WRITE JSON: {file_path}")
        except Exception as e:
            raise FileOperationError(f"写入 JSON 失败: {file_path}") from e

    # —————————————————— CSV ——————————————————

    def read_csv(
        self,
        file_path: FilePath,
        encoding: str = 'utf-8',
        delimiter: str = ','
    ) -> list[dict[str, str]]:
        """读取 CSV"""
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                data = list(reader)
            self._log_operation(f"READ CSV: {file_path}")
            return data
        except Exception as e:
            raise FileOperationError(f"读取 CSV 失败: {file_path}") from e

    def write_csv(
        self,
        data: list[dict],
        file_path: FilePath,
        fieldnames: Optional[list[str]] = None,
        encoding: str = 'utf-8',
        delimiter: str = ','
    ) -> None:
        """写入 CSV"""
        if not data:
            raise FileOperationError("CSV 数据为空")

        try:
            path = self._ensure_dir(file_path)
            fieldnames = fieldnames or list(data[0].keys())
            with path.open('w', encoding=encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            self._log_operation(f"WRITE CSV: {file_path}")
        except Exception as e:
            raise FileOperationError(f"写入 CSV 失败: {file_path}") from e

    # —————————————————— Pickle ——————————————————

    def read_pickle(self, file_path: FilePath) -> Any:
        """读取 Pickle"""
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            self._log_operation(f"READ PICKLE: {file_path}")
            return data
        except Exception as e:
            raise FileOperationError(f"读取 Pickle 失败: {file_path}") from e

    def write_pickle(self, obj: Any, file_path: FilePath) -> None:
        """写入 Pickle"""
        try:
            path = self._ensure_dir(file_path)
            with path.open('wb') as f:
                pickle.dump(obj, f)
            self._log_operation(f"WRITE PICKLE: {file_path}")
        except Exception as e:
            raise FileOperationError(f"写入 Pickle 失败: {file_path}") from e

    # —————————————————— 辅助方法 ——————————————————

    def get_history(self) -> list[str]:
        """获取操作历史（调试用）"""
        return self._operation_history.copy()

    def clear_history(self) -> None:
        """清空操作历史"""
        self._operation_history.clear()

    def __repr__(self) -> str:
        return f"<FileController instance, history={len(self._operation_history)} ops>"

