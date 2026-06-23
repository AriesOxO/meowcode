"""
工具系统 - 文件操作
"""
import os
from typing import Optional


class FileOperations:
    """文件操作工具"""

    @staticmethod
    def read_file(filepath: str) -> Optional[str]:
        """
        读取文件内容

        Args:
            filepath: 文件路径

        Returns:
            文件内容，失败返回 None
        """
        try:
            if not os.path.exists(filepath):
                return f"❌ 文件不存在: {filepath}"

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # 添加行号（方便后续编辑）
            lines = content.split('\n')
            numbered = '\n'.join([f"{i+1:4d} | {line}" for i, line in enumerate(lines)])

            return f"📄 {filepath}\n{'='*60}\n{numbered}"

        except Exception as e:
            return f"❌ 读取失败: {str(e)}"

    @staticmethod
    def write_file(filepath: str, content: str) -> str:
        """
        写入文件（覆盖）

        Args:
            filepath: 文件路径
            content: 文件内容

        Returns:
            执行结果消息
        """
        try:
            # 确保目录存在
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            lines = len(content.split('\n'))
            return f"✅ 已写入 {filepath} ({lines} 行)"

        except Exception as e:
            return f"❌ 写入失败: {str(e)}"

    @staticmethod
    def append_file(filepath: str, content: str) -> str:
        """
        追加内容到文件

        Args:
            filepath: 文件路径
            content: 要追加的内容

        Returns:
            执行结果消息
        """
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content)

            return f"✅ 已追加到 {filepath}"

        except Exception as e:
            return f"❌ 追加失败: {str(e)}"

    @staticmethod
    def list_files(directory: str = ".", pattern: str = "*") -> str:
        """
        列出目录下的文件

        Args:
            directory: 目录路径
            pattern: 文件模式（暂不实现通配符）

        Returns:
            文件列表
        """
        try:
            if not os.path.exists(directory):
                return f"❌ 目录不存在: {directory}"

            files = []
            for item in os.listdir(directory):
                full_path = os.path.join(directory, item)
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    files.append(f"  📄 {item} ({size} bytes)")
                else:
                    files.append(f"  📁 {item}/")

            if not files:
                return f"📂 {directory} (空目录)"

            return f"📂 {directory}\n" + "\n".join(sorted(files))

        except Exception as e:
            return f"❌ 列出文件失败: {str(e)}"
