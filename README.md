# MeowCode - AI 编码助手

一个轻量级、支持多模型的 AI 编码助手。

## 特性

- 🎯 基于 DeepSeek，性价比极高
- 🔧 命令行界面，简单高效
- 🔌 可扩展架构，支持多模型
- 📦 单文件打包，开箱即用

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置 API Key

```bash
# 方式 1: 环境变量
export DEEPSEEK_API_KEY="sk-your-api-key-here"

# 方式 2: 配置文件
cp config/config.example.yaml config/config.yaml
# 编辑 config.yaml 填入 API Key
```

### 运行

```bash
python agent.py
```

## 开发状态

- [x] 项目初始化
- [ ] 核心循环实现
- [ ] 文件操作工具
- [ ] 代码搜索功能
- [ ] 多模型支持
- [ ] 打包发布

## 技术栈

- Python 3.10+
- DeepSeek API (via OpenAI SDK)
- 标准库（最小依赖）

## 文档

- [架构设计](docs/设计/20260623-MeowCode架构设计.md)
- [开发博客](docs/blog/) - 边做边写

## License

MIT
