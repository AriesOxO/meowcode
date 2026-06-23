"""
DeepSeek LLM 提供商
"""
from typing import List, Dict
from openai import OpenAI
from .base import BaseLLMProvider


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek LLM 提供商实现"""

    def __init__(self, api_key: str, model: str = "deepseek-v4-flash",
                 base_url: str = "https://api.deepseek.com"):
        super().__init__(api_key, model)
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def query(self, messages: List[Dict[str, str]]) -> str:
        """查询 DeepSeek 模型"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"DeepSeek API 调用失败: {e}")

    def get_model_info(self) -> Dict:
        """获取 DeepSeek 模型信息"""
        models_info = {
            "deepseek-v4-flash": {
                "name": "DeepSeek V4 Flash",
                "context_length": 64000,
                "pricing": {"input": 0.1, "output": 0.2, "unit": "¥/M tokens"}
            },
            "deepseek-v4-pro": {
                "name": "DeepSeek V4 Pro",
                "context_length": 64000,
                "pricing": {"input": 1.0, "output": 2.0, "unit": "¥/M tokens"}
            }
        }

        info = models_info.get(self.model, models_info["deepseek-v4-flash"])
        info["provider"] = "DeepSeek"
        return info
