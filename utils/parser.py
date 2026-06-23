"""
Action 解析器 - 从 LLM 输出中提取结构化命令
"""
import re
from typing import Optional, Dict


class ActionParser:
    """解析 LLM 输出中的 action"""

    @staticmethod
    def parse_bash_action(text: str) -> Optional[str]:
        """
        解析 bash 命令

        格式: ```bash-action
              <command>
              ```
        """
        matches = re.findall(
            r"```bash-action\s*\n(.*?)\n```",
            text,
            re.DOTALL
        )
        return matches[0].strip() if matches else None

    @staticmethod
    def parse_read_file(text: str) -> Optional[str]:
        """
        解析读取文件命令

        格式: ```read-file
              <filepath>
              ```
        """
        matches = re.findall(
            r"```read-file\s*\n(.*?)\n```",
            text,
            re.DOTALL
        )
        return matches[0].strip() if matches else None

    @staticmethod
    def parse_write_file(text: str) -> Optional[Dict[str, str]]:
        """
        解析写入文件命令

        格式: ```write-file
              <filepath>
              ---
              <content>
              ```

        Returns:
            {"path": "filepath", "content": "content"} 或 None
        """
        matches = re.findall(
            r"```write-file\s*\n(.*?)\n---\n(.*?)\n```",
            text,
            re.DOTALL
        )
        if matches:
            filepath, content = matches[0]
            return {"path": filepath.strip(), "content": content}
        return None

    @staticmethod
    def parse_action(text: str) -> Optional[Dict]:
        """
        解析所有类型的 action

        Returns:
            {
                "type": "bash" | "read_file" | "write_file" | "exit",
                "data": ...  # 根据类型不同而不同
            }
        """
        # 检查是否是退出命令
        bash_cmd = ActionParser.parse_bash_action(text)
        if bash_cmd:
            if bash_cmd.strip().lower() == "exit":
                return {"type": "exit", "data": None}
            return {"type": "bash", "data": bash_cmd}

        # 检查读取文件
        read_path = ActionParser.parse_read_file(text)
        if read_path:
            return {"type": "read_file", "data": read_path}

        # 检查写入文件
        write_data = ActionParser.parse_write_file(text)
        if write_data:
            return {"type": "write_file", "data": write_data}

        return None
