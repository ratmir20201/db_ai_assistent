from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


class Translator:
    llm = OllamaLLM(model="llama3.1:latest", temperature=0.0)

    @classmethod
    def translate_from_russian_into_english(cls, user_input: str):
        system_prompt = ChatPromptTemplate.from_template(
            """
            Translate the following Russian text into fluent English.
            Respond with the translation only. No explanations, no comments.

            Text: {user_input}
            """
        )
        return cls._make_chain(system_prompt, user_input)

    @classmethod
    def translate_from_english_into_russian(cls, user_input: str):
        system_prompt = ChatPromptTemplate.from_template(
            """
            Translate the text provided below into Russian. However, do not change the names of tables and columns. 
            Table names start with STAGE_DO, DWH, DM, or SANDBOX. The names of both tables and columns are written in uppercase letters.
            Respond with the translation only. No explanations, no comments. 
            
            Text: {user_input}
            """
        )
        return cls._make_chain(system_prompt, user_input)

    @classmethod
    def language_detect(cls, user_input: str):
        system_prompt = ChatPromptTemplate.from_template(
            """
            Detect the language of the following text and respond with only one of the two language codes: "ru" for Russian or "en" for English. 
            Do not include any explanations, comments, or additional text.

            Text: {user_input}
            """
        )
        return cls._make_chain(system_prompt, user_input)

    @classmethod
    def _make_chain(cls, prompt: ChatPromptTemplate, user_input: str) -> str:
        """Создает цепь, и делает запрос в llm передавая неполную схему бд."""

        chain = prompt | cls.llm
        return chain.invoke({"user_input": user_input})
