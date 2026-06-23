# -*- coding: utf-8 -*-
"""
简化测试 - 测试 Agent 核心循环
"""
import sys
import io

# Windows 编码fix
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from models import create_provider
from utils import ActionParser

# 初始化
print("初始化 DeepSeek 提供商...")
provider = create_provider(
    provider_name="deepseek",
    api_key="sk-ilsfrqticbgjmsldxljxdbhnvcuhfmloanmcjepyewvwxnhu",
    model="deepseek-ai/DeepSeek-V3.2",
    base_url="https://api.siliconflow.cn/v1"
)

print("测试查询...")
messages = [
    {"role": "system", "content": "你是一个编码助手。当你想列出文件时，用```bash-action\nls\n```格式。"},
    {"role": "user", "content": "列出当前目录的文件"}
]

response = provider.query(messages)
print("\nLLM 响应:")
print("-" * 60)
print(response)
print("-" * 60)

# 解析 action
parser = ActionParser()
action = parser.parse_action(response)

if action:
    print(f"\n解析到的 Action:")
    print(f"  类型: {action['type']}")
    print(f"  数据: {action['data']}")
else:
    print("\n未解析到 Action")

print("\n测试完成!")
