"""
工具系统 - 命令执行
"""
import subprocess
import os
from typing import Dict


class CommandExecutor:
    """命令执行器"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

        # 环境变量配置（禁用交互式工具）
        self.env = os.environ.copy()
        self.env.update({
            "PAGER": "cat",
            "MANPAGER": "cat",
            "LESS": "-R",
            "PIP_PROGRESS_BAR": "off",
            "TQDM_DISABLE": "1",
        })

    def execute(self, command: str) -> Dict[str, any]:
        """
        执行命令

        Args:
            command: 要执行的 shell 命令

        Returns:
            {
                "stdout": 标准输出,
                "stderr": 标准错误,
                "returncode": 返回码,
                "success": 是否成功
            }
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                env=self.env,
                encoding="utf-8",
                errors="replace",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout,
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"命令超时（>{self.timeout}秒）",
                "returncode": -1,
                "success": False
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"执行失败: {str(e)}",
                "returncode": -1,
                "success": False
            }

    def format_result(self, result: Dict) -> str:
        """格式化执行结果为文本"""
        output = []

        if result["stdout"]:
            output.append(result["stdout"])

        if result["stderr"]:
            output.append(f"[STDERR]\n{result['stderr']}")

        if not result["success"]:
            output.append(f"[返回码: {result['returncode']}]")

        return "\n".join(output) if output else "(无输出)"
