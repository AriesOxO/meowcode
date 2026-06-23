"""
配置加载器
"""
import os
import yaml
from typing import Dict, Any


class Config:
    """配置管理器"""

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        # 如果配置文件不存在，使用示例配置
        if not os.path.exists(self.config_path):
            example_path = "config/config.example.yaml"
            if os.path.exists(example_path):
                print(f"⚠️  配置文件不存在，使用示例配置: {example_path}")
                self.config_path = example_path
            else:
                print("⚠️  配置文件不存在，使用默认配置")
                return self._default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config or {}
        except Exception as e:
            print(f"❌ 配置文件加载失败: {e}")
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            "llm": {
                "provider": "deepseek",
                "deepseek": {
                    "api_key": "",
                    "model": "deepseek-v4-flash",
                    "base_url": "https://api.deepseek.com"
                }
            },
            "agent": {
                "max_iterations": 20,
                "command_timeout": 30
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值（支持点号分隔的路径）"""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def get_llm_config(self) -> Dict[str, Any]:
        """获取 LLM 配置"""
        provider = self.get('llm.provider', 'deepseek')
        provider_config = self.get(f'llm.{provider}', {})

        # 优先从环境变量读取 API Key
        env_key = f"{provider.upper()}_API_KEY"
        if env_key in os.environ:
            provider_config['api_key'] = os.environ[env_key]

        return {
            "provider": provider,
            **provider_config
        }
