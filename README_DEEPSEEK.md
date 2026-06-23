# DeepSeek Agent 快速开始

## 安装依赖

```bash
pip install openai
```

## 配置 API Key

```bash
# 方式 1: 环境变量
export DEEPSEEK_API_KEY="sk-your-api-key-here"

# 方式 2: 或者直接在代码中修改
client = OpenAI(
    api_key="sk-your-api-key-here",
    base_url="https://api.deepseek.com"
)
```

## 运行

```bash
python agent_deepseek.py
```

## DeepSeek 模型选择

| 模型 | 用途 | 价格 |
|------|------|------|
| `deepseek-v4-flash` | Agent、快速响应 | 便宜 |
| `deepseek-v4-pro` | 复杂推理、代码生成 | 较贵 |

**Agent 推荐用 `deepseek-v4-flash`**：
- 速度快（降低循环延迟）
- 价格低（Agent 会多次调用）
- 能力够用（命令生成不需要最强推理）

## 参考资源

- [DeepSeek API 文档](https://api-docs.deepseek.com)
- [DeepSeek 价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)
- [获取 API Key](https://platform.deepseek.com/api_keys)
