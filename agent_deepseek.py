"""
极简 AI Agent - DeepSeek 版本
只依赖: openai
"""
import re
import subprocess
import os
from openai import OpenAI

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),  # 或直接写 "sk-xxx"
    base_url="https://api.deepseek.com"
)

def query_lm(messages: list[dict]) -> str:
    """查询 DeepSeek 模型"""
    response = client.chat.completions.create(
        model="deepseek-v4-flash",  # 便宜快速，适合 Agent
        messages=messages
    )
    return response.choices[0].message.content

def parse_action(lm_output: str) -> str:
    """从 LM 输出中提取 action"""
    matches = re.findall(
        r"```bash-action\s*\n(.*?)\n```",
        lm_output,
        re.DOTALL
    )
    return matches[0].strip() if matches else ""

def execute_action(command: str) -> str:
    """执行 action，返回输出"""
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        env=os.environ,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
    )
    return result.stdout

# 主循环
if __name__ == "__main__":
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant. When you want to run a command, wrap it in ```bash-action\n<command>\n```. To finish, run the exit command."
    }, {
        "role": "user",
        "content": "List the files in the current directory"
    }]

    while True:
        print("\n" + "="*50)
        lm_output = query_lm(messages)
        print(f"🤖 Agent: {lm_output}")
        messages.append({"role": "assistant", "content": lm_output})

        action = parse_action(lm_output)
        if not action:
            print("⚠️  No action found")
            break

        print(f"⚡ Action: {action}")
        if action == "exit":
            print("👋 Bye!")
            break

        output = execute_action(action)
        print(f"📤 Output:\n{output}")
        messages.append({"role": "user", "content": output})
