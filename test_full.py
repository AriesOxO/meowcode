# -*- coding: utf-8 -*-
"""
快速测试脚本 - 测试完整 Agent 流程
"""
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from models import create_provider
from tools import CommandExecutor, FileOperations
from utils import ActionParser, Config

print("="*60)
print("MeowCode Agent 快速测试")
print("="*60)

# 加载配置
config = Config()
llm_config = config.get_llm_config()

print(f"\nLLM 配置:")
print(f"  提供商: {llm_config['provider']}")
print(f"  模型: {llm_config['model']}")
print(f"  Base URL: {llm_config['base_url']}")

# 初始化
provider = create_provider(
    provider_name=llm_config['provider'],
    api_key=llm_config['api_key'],
    model=llm_config['model'],
    base_url=llm_config['base_url']
)
executor = CommandExecutor()
file_ops = FileOperations()
parser = ActionParser()

# 测试任务
print("\n任务: 列出当前目录文件\n")

messages = [
    {"role": "system", "content": config.get('agent.system_prompt')},
    {"role": "user", "content": "列出当前目录的文件"}
]

# 第一轮
print("[第 1 轮]")
print("-"*60)
lm_output = provider.query(messages)
print(f"Agent: {lm_output[:200]}...")
messages.append({"role": "assistant", "content": lm_output})

action = parser.parse_action(lm_output)
if action and action["type"] == "bash":
    print(f"\nAction: {action['data']}")
    result = executor.execute(action['data'])
    output = executor.format_result(result)
    print(f"Output:\n{output[:300]}")

    messages.append({"role": "user", "content": output})

    # 第二轮
    print("\n[第 2 轮]")
    print("-"*60)
    lm_output = provider.query(messages)
    print(f"Agent: {lm_output}")

    # 检查是否有 exit
    action2 = parser.parse_action(lm_output)
    if action2 and action2["type"] == "exit":
        print("\n任务完成!")

print("\n" + "="*60)
print("测试完成!")
