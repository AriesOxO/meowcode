"""
LLM 提供商工厂
"""
from typing import Dict
from .base import BaseLLMProvider
from .deepseek import DeepSeekProvider

# 注册所有提供商
PROVIDERS: Dict[str, type] = {
    "deepseek": DeepSeekProvider,
    # 未来添加
    # "zhipu": ZhipuProvider,
    # "anthropic": AnthropicProvider,
}


def create_provider(provider_name: str, api_key: str, model: str = None, **kwargs) -> BaseLLMProvider:
    """
    创建 LLM 提供商实例

    Args:
        provider_name: 提供商名称 (deepseek, zhipu, anthropic)
        api_key: API Key
        model: 模型名称（可选，使用默认模型）
        **kwargs: 其他参数（如 base_url）

    Returns:
        BaseLLMProvider 实例

    Raises:
        ValueError: 如果提供商不存在
    """
    if provider_name not in PROVIDERS:
        available = ", ".join(PROVIDERS.keys())
        raise ValueError(f"未知的提供商: {provider_name}。可用: {available}")

    provider_class = PROVIDERS[provider_name]

    # 构建参数
    init_args = {"api_key": api_key}
    if model:
        init_args["model"] = model
    init_args.update(kwargs)

    return provider_class(**init_args)


def list_providers() -> list:
    """列出所有可用的提供商"""
    return list(PROVIDERS.keys())
