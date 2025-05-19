from typing import Type

from llms.base_llm import BaseLLM
from llms.deepseek_coder_1_3b.client import DeepseekCoderV1LLM
from llms.deepseek_coder_6_7b.client import DeepseekCoderV2LLM
from llms.deepseek_r1.client import DeepseekR1LLM
from llms.mistral.client import MistralLLM
from schemas import LLMType

llm_registry: dict[LLMType, Type[BaseLLM]] = {
    LLMType.mistral: MistralLLM,
    LLMType.deepseek_r1: DeepseekR1LLM,
    LLMType.deepseek_coder_v1: DeepseekCoderV1LLM,
    LLMType.deepseek_coder_v2: DeepseekCoderV2LLM,
}


def get_llm_by_type(llm_type: LLMType) -> Type[BaseLLM]:
    if llm_type in llm_registry.keys():
        return llm_registry[llm_type]
    raise TypeError(f"Неподдерживаемый тип LLM: {llm_type}")
