# MeowCode 快速启动指南

## 🚀 5 分钟上手

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

只需要一个依赖：`openai` (用于 DeepSeek API)

### 2. 配置 API Key

**方式 A：环境变量（推荐）**

```bash
# Windows
set DEEPSEEK_API_KEY=sk-your-api-key-here

# Linux/macOS
export DEEPSEEK_API_KEY=sk-your-api-key-here
```

**方式 B：配置文件**

```bash
# 复制示例配置
cp config/config.example.yaml config/config.yaml

# 编辑 config/config.yaml
# 找到 llm.deepseek.api_key，填入你的 API Key
```

**获取 API Key：** https://platform.deepseek.com/api_keys

### 3. 运行测试

```bash
# 交互式输入任务
python agent.py

# 或直接指定任务
python agent.py "列出当前目录的文件"
```

### 4. 示例任务

```bash
# 文件操作
python agent.py "创建一个 hello.py 文件，内容是打印 Hello World"

# 代码搜索
python agent.py "找出所有 Python 文件"

# 命令执行
python agent.py "显示当前 Python 版本"
```

## 📁 项目结构

```
meowcode/
├── agent.py              # 🎯 主程序（从这里开始）
├── models/               # 🤖 LLM 提供商
│   ├── base.py          # 抽象基类
│   ├── deepseek.py      # DeepSeek 实现
│   └── factory.py       # 工厂函数
├── tools/                # 🔧 工具系统
│   ├── execute.py       # 命令执行器
│   └── file_ops.py      # 文件操作
├── utils/                # 🛠️ 工具函数
│   ├── parser.py        # Action 解析
│   └── config.py        # 配置加载
├── config/               # ⚙️ 配置
│   └── config.example.yaml
└── docs/                 # 📚 文档
    ├── blog/            # 开发博客
    ├── 设计/            # 设计文档
    └── 参考文档/        # 参考资料
```

## 🎮 支持的 Action

Agent 支持以下操作：

### 1. 执行命令

```markdown
\```bash-action
ls -la
\```
```

### 2. 读取文件

```markdown
\```read-file
path/to/file.py
\```
```

### 3. 写入文件

```markdown
\```write-file
path/to/file.py
---
print("Hello World")
\```
```

### 4. 退出

```markdown
\```bash-action
exit
\```
```

## ⚙️ 配置说明

编辑 `config/config.yaml`：

```yaml
# 选择 LLM 提供商
llm:
  provider: deepseek  # 当前只支持 deepseek

  deepseek:
    api_key: ""       # 或从环境变量读取
    model: deepseek-v4-flash  # 或 deepseek-v4-pro
    base_url: https://api.deepseek.com

# Agent 行为
agent:
  max_iterations: 20       # 最大循环次数
  command_timeout: 30      # 命令超时（秒）
```

## 🐛 常见问题

### 1. "未配置 API Key"

**解决**：设置环境变量 `DEEPSEEK_API_KEY` 或编辑 `config/config.yaml`

### 2. "DeepSeek API 调用失败"

**可能原因**：
- API Key 错误
- 网络问题（国内访问 DeepSeek 不需要代理）
- 账户余额不足

**检查**：
```bash
# 测试 API Key 是否有效
curl https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"hi"}]}'
```

### 3. "达到最大循环次数"

**原因**：任务过于复杂或 Agent 陷入循环

**解决**：
- 分解任务为更小的步骤
- 增加 `agent.max_iterations` 配置
- 检查任务描述是否明确

## 📊 成本估算

使用 DeepSeek v4-flash：
- 输入：¥0.1/M tokens
- 输出：¥0.2/M tokens

**典型任务成本**：
- 简单文件操作：<¥0.001
- 修复一个 Bug：~¥0.002
- 重构一个模块：~¥0.01

**100 元能做什么**：约 5000 个 Bug 修复或 10000 次文件操作！

## 🚧 开发状态

- [x] 核心循环
- [x] 基础文件操作
- [x] 命令执行
- [ ] 代码搜索
- [ ] 多模型支持（智谱、Claude）
- [ ] 错误重试机制
- [ ] 打包发布

## 📚 更多文档

- [架构设计](docs/设计/20260623-MeowCode架构设计.md) - 完整的技术方案
- [开发博客](docs/blog/) - 边做边写的开发日志
- [参考教程](docs/参考文档/20260623-Minimal-Agent设计教程.md) - Agent 设计原理

## 🤝 参与开发

欢迎 PR 和 Issue！

特别需要：
- 智谱 GLM 集成
- Anthropic Claude 集成
- 代码搜索优化
- 更好的错误处理

## 📝 License

MIT
