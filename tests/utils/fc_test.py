# -*- coding: utf-8 -*-
"""
@file:      fc_test
@time:      2025/9/28 03:41
@author:    sMythicalBird
"""
from utils import FileController
from pathlib import Path
from config import PATHS

file_path = PATHS["tests"] / "logs"

# 获取唯一实例
fc = FileController()

# 1. 写入 JSON
fc.write_json({"name": "Alice", "age": 25}, file_path/"user.json")

# 2. 读取 JSON
user = fc.read_json(file_path/"user.json")
print(user)

# 3. 写入 CSV
fc.write_csv(
    [{"name": "Alice", "score": 95}, {"name": "Bob", "score": 87}],
    file_path/"scores.csv"
)

# 4. 读取 CSV
scores = fc.read_csv(file_path/"scores.csv")
print(scores)

# 5. 文本操作
fc.write_text("Hello, world！", file_path/"app.log")
fc.append_text("原神启动", file_path/"app.log")

# 6. 检查文件
if fc.exists(file_path/"user.json"):
    print("文件大小:", fc.get_size(file_path/"user.json"), "bytes")

# 7. 查看操作历史
print("操作历史:", fc.get_history())