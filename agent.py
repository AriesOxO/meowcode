#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeowCode - AI 编码助手
主程序入口
"""
import os
import sys
import io
from typing import List, Dict

# 设置 Windows 控制台编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from models import create_provider
from tools import CommandExecutor, FileOperations
from utils import ActionParser, Config


class MeowCodeAgent:
    """MeowCode Agent 主类"""

    def __init__(self, config: Config):
        self.config = config

        # 初始化 LLM
        llm_config = config.get_llm_config()
        self.provider = create_provider(
            provider_name=llm_config["provider"],
            api_key=llm_config["api_key"],
            model=llm_config.get("model"),
            base_url=llm_config.get("base_url")
        )

        # 初始化工具
        self.executor = CommandExecutor(
            timeout=config.get('agent.command_timeout', 30)
        )
        self.file_ops = FileOperations()
        self.parser = ActionParser()

        # Agent 状态
        self.messages: List[Dict] = []
        self.max_iterations = config.get('agent.max_iterations', 20)

    def initialize(self, user_task: str):
        """初始化对话"""
        system_prompt = self.config.get('agent.system_prompt', '')

        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_task}
        ]

    def run(self, user_task: str):
        """运行 Agent 主循环"""
        print("🐱 MeowCode Agent 启动")
        print(f"📋 任务: {user_task}")
        print("=" * 60)

        self.initialize(user_task)

        for iteration in range(self.max_iterations):
            print(f"\n📍 第 {iteration + 1} 轮")
            print("-" * 60)

            # 查询 LLM
            try:
                lm_output = self.provider.query(self.messages)
                print(f"🤖 Agent:\n{lm_output}\n")
                self.messages.append({"role": "assistant", "content": lm_output})
            except Exception as e:
                print(f"❌ LLM 查询失败: {e}")
                break

            # 解析 action
            action = self.parser.parse_action(lm_output)

            if not action:
                print("⚠️  未检测到 action，继续对话...")
                continue

            # 执行 action
            action_type = action["type"]
            print(f"⚡ Action: {action_type}")

            if action_type == "exit":
                print("✅ 任务完成，退出")
                break

            result = self.execute_action(action)
            print(f"📤 输出:\n{result}\n")

            # 将结果反馈给 LLM
            self.messages.append({"role": "user", "content": result})

        else:
            print(f"⚠️  达到最大循环次数 ({self.max_iterations})")

        print("\n" + "=" * 60)
        print("👋 MeowCode Agent 结束")

    def execute_action(self, action: Dict) -> str:
        """执行 action"""
        action_type = action["type"]
        data = action["data"]

        if action_type == "bash":
            result = self.executor.execute(data)
            return self.executor.format_result(result)

        elif action_type == "read_file":
            return self.file_ops.read_file(data)

        elif action_type == "write_file":
            return self.file_ops.write_file(data["path"], data["content"])

        else:
            return f"❌ 未知的 action 类型: {action_type}"


def main():
    """主函数"""
    # 加载配置
    config = Config()

    # 检查 API Key
    llm_config = config.get_llm_config()
    if not llm_config.get("api_key"):
        print("❌ 未配置 API Key")
        print(f"请设置环境变量 {llm_config['provider'].upper()}_API_KEY")
        print("或编辑配置文件 config/config.yaml")
        sys.exit(1)

    # 获取任务
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = input("🐱 请输入任务: ").strip()
        if not task:
            print("❌ 任务不能为空")
            sys.exit(1)

    # 创建并运行 Agent
    agent = MeowCodeAgent(config)
    agent.run(task)


if __name__ == "__main__":
    main()
