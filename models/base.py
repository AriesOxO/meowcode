"""
MeowCode LLM 提供商基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class BaseLLMProvider(ABC):
    """LLM 提供商抽象基类"""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def query(self, messages: List[Dict[str, str]]) -> str:
        """
        查询 LLM

        Args:
            messages: 对话消息列表，格式 [{"role": "user/assistant/system", "content": "..."}]

        Returns:
            模型响应文本
        """
        pass

    @abstractmethod
    def get_model_info(self) -> Dict:
        """
        获取模型信息

        Returns:
            {
                "name": "模型名称",
                "provider": "提供商",
                "context_length": 上下文长度,
                "pricing": {"input": 输入价格, "output": 输出价格, "unit": "单位"}
            }
        """
        pass

    def validate_api_key(self) -> bool:
        """
        验证 API Key 是否有效

        Returns:
            True 如果有效，False 否则
        """
        try:
            # 发送一个简单的测试请求
            test_messages = [{"role": "user", "content": "hi"}]
            self.query(test_messages)
            return True
        except Exception as e:
            print(f"❌ API Key 验证失败: {e}")
            return False
