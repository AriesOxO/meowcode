#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试硅基流动 API 连接
"""
import sys
import io
from openai import OpenAI

# 设置 Windows 控制台编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 硅基流动配置
API_KEY = "sk-ilsfrqticbgjmsldxljxdbhnvcuhfmloanmcjepyewvwxnhu"
BASE_URL = "https://api.siliconflow.cn/v1"
MODEL = "deepseek-ai/DeepSeek-V3.2"

print("测试硅基流动 API 连接")
print("=" * 60)
print(f"Base URL: {BASE_URL}")
print(f"Model: {MODEL}")
print("=" * 60)

try:
    # 创建客户端
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )

    print("\n发送测试请求...")

    # 测试请求
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": "你好，请用一句话介绍你自己。"}
        ]
    )

    print("API 调用成功！\n")
    print("模型响应:")
    print("-" * 60)
    print(response.choices[0].message.content)
    print("-" * 60)

    print(f"\n使用情况:")
    print(f"   输入 tokens: {response.usage.prompt_tokens}")
    print(f"   输出 tokens: {response.usage.completion_tokens}")
    print(f"   总计 tokens: {response.usage.total_tokens}")

    print("\n测试通过！可以继续使用 MeowCode Agent")

except Exception as e:
    print(f"\n测试失败: {e}")
    print("\n可能的原因:")
    print("  1. API Key 无效或已过期")
    print("  2. 网络连接问题")
    print("  3. 模型名称错误")
    print("  4. 账户余额不足")
