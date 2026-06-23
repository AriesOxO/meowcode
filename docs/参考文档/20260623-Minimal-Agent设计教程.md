---
title: Minimal AI Agent 设计教程
type: reference
author: Claude
created: 2026-06-23
updated: 2026-06-23
status: active
tags: [agent, 架构, 教程, AI]
source: https://minimal-agent.com/
---

# Minimal AI Agent 设计教程

## 概述

本教程展示如何用约 50-60 行代码从零构建一个 AI Agent，用于软件工程任务。

### 核心循环模式

```
1. 向语言模型发送消息
2. 解析模型输出中的 action
3. 执行 action
4. 将执行结果反馈给模型
5. 重复循环
```

---

## 一、查询语言模型（Query LM）

### OpenAI 实现

安装：
```bash
pip install openai
```

代码：
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key-here"
)  # 或设置 OPENAI_API_KEY 环境变量

def query_lm(messages):
    response = client.responses.create(
        model="gpt-5.1",
        input=messages
    )
    return response.output_text
```

### LiteLLM 实现

支持 100+ 语言模型提供商。

安装：
```bash
pip install litellm
```

代码：
```python
from litellm import completion

def query_lm(messages: list[dict[str, str]]) -> str:
    response = completion(
        model="openai/gpt-5.1",
        messages=messages
    )
    return response.choices[0].message.content
```

### Anthropic 实现

安装：
```bash
pip install anthropic
```

代码：
```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key-here")

def query_lm(messages):
    response = client.messages.create(
        model="claude-sonnet-4.5",
        max_tokens=4096,
        messages=messages
    )
    return response.content[0].text
```

### OpenRouter 实现

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-api-key-here"
)

def query_lm(messages):
    response = client.chat.completions.create(
        model="anthropic/claude-3.5-sonnet",
        messages=messages
    )
    return response.choices[0].message.content
```

### GLM (Zhipu AI) 实现

安装：
```bash
pip install zhipuai
```

代码：
```python
from zhipuai import ZhipuAI

client = ZhipuAI(
    api_key="your-api-key-here"
)  # 或设置 ZHIPUAI_API_KEY 环境变量

def query_lm(messages):
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=messages
    )
    return response.choices[0].message.content
```

---

## 二、解析 Action

### 方案 A：Triple Backticks（Markdown 代码块）

格式示例：
```
\```bash-action
ls -la
\```
```

解析代码：
```python
import re

def parse_action(lm_output: str) -> str:
    matches = re.findall(
        r"```bash-action\s*\n(.*?)\n```",
        lm_output,
        re.DOTALL
    )
    return matches[0].strip() if matches else ""
```

### 方案 B：XML 风格标签

格式示例：
```
<bash_action>
cat file.txt
</bash_action>
```

解析代码：
```python
import re

def parse_action(lm_output: str) -> str:
    matches = re.findall(
        r"<bash_action>(.*?)</bash_action>",
        lm_output,
        re.DOTALL
    )
    return matches[0].strip() if matches else ""
```

---

## 三、执行 Action

```python
import subprocess
import os

def execute_action(command: str) -> str:
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
```

关键参数说明：
- `shell=True`：允许执行 shell 命令
- `stdout=subprocess.PIPE`：捕获标准输出
- `timeout=30`：防止命令挂起

---

## 四、系统提示词（System Prompt）

```python
messages = [{
    "role": "system",
    "content": "You are a helpful assistant. When you want to run a command, wrap it in ```bash-action\n<command>\n```. To finish, run the exit command."
}]
```

简洁清晰，指定：
- 身份定位
- Action 格式规范
- 终止条件

---

## 四点五、完整的 56 行 Agent 代码

将上述所有组件整合在一起：

```python
import re
import subprocess
import os
from litellm import completion

def query_lm(messages: list[dict[str, str]]) -> str:
    response = completion(
        model="openai/gpt-5.1",
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

# 主 agent 循环
messages = [{
    "role": "system",
    "content": "You are a helpful assistant. When you want to run a command, wrap it in ```bash-action\n<command>\n```. To finish, run the exit command."
}, {
    "role": "user",
    "content": "List the files in the current directory"
}]

while True:
    lm_output = query_lm(messages)
    print("LM output", lm_output)
    messages.append({"role": "assistant", "content": lm_output})
    
    action = parse_action(lm_output)
    print("Action", action)
    if action == "exit":
        break
    
    output = execute_action(action)
    print("Output", output)
    messages.append({"role": "user", "content": output})
```

**这就是基础架构**：查询 LM → 解析 action → 执行 → 将输出反馈回去，循环往复。

---

## 五、增强特性 - 让 Agent 更健壮

### 1. 异常处理

```python
class NonterminatingException(RuntimeError): ...
class TerminatingException(RuntimeError): ...

while True:
    try:
        # 主循环内容
    except NonterminatingException as e:
        messages.append({"role": "user", "content": str(e)})
    except TerminatingException as e:
        print("Stopping because of ", str(e))
        break
```

**设计思路**：
- 可恢复错误 → 将异常信息发回给模型，让其调整策略
- 致命错误 → 直接终止循环

### 2. 格式验证

当模型输出格式不正确时，追加提醒消息：

```python
if not action:
    messages.append({
        "role": "user",
        "content": "Please wrap your command in the correct format."
    })
    continue
```

### 3. 环境变量配置

禁用交互式工具，确保命令在非交互环境中正常执行：

```python
env_vars = {
    "PAGER": "cat",
    "MANPAGER": "cat",
    "LESS": "-R",
    "PIP_PROGRESS_BAR": "off",
    "TQDM_DISABLE": "1",
}

# 在 execute_action 中使用：
env=os.environ | env_vars
```

---

## 六、Mini-SWE-Agent 架构参考

教程提到一个生产级实现，采用模块化架构：

- **Agent 类**：主循环控制
- **Model 类**：多 LM 提供商适配
- **Environment 类**：执行环境（本地 / Docker）

源码地址：GitHub（教程中有链接）

核心理念：在上述蓝图基础上添加最小必要复杂度。

---

## 核心设计哲学

1. **简洁性优先**：50-60 行即可实现核心功能
2. **循环驱动**：持续反馈，让模型自我纠正
3. **格式约束**：明确的 action 格式，简化解析
4. **渐进增强**：核心逻辑稳定后再添加异常处理、验证等特性

---

## 适用场景

- 自动化代码分析与修复
- 文件系统操作任务
- 命令行工具编排
- DevOps 自动化脚本

---

## 参考资源

- 原始教程：https://minimal-agent.com/
- 生产实现：参见教程中 GitHub 链接
- 相关技术：LangChain、AutoGPT 等更复杂的框架

---

## 启发

这个极简设计揭示了 AI Agent 的本质：
- 不需要复杂框架
- 核心是「思考-行动-观察」循环
- 清晰的接口比复杂的抽象更重要

