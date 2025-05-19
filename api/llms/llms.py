from typing import Type

from llms.base_llm import BaseLLM
from llms.mistral.mistral_client import MistralLLM
from schemas import LLMType

llm_registry: dict[LLMType, Type[BaseLLM]] = {
    LLMType.mistral: MistralLLM,
}


def get_llm_by_type(llm_type: LLMType) -> Type[BaseLLM]:
    if llm_type in llm_registry.keys():
        return llm_registry[llm_type]
    raise TypeError(f"Неподдерживаемый тип LLM: {llm_type}")
