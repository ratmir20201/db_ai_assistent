import requests
from fastapi import HTTPException
from starlette.status import HTTP_200_OK

from config import settings
from db_parsing import parse_db_to_json
from logger import logger


def generate_sql(prompt: str):
    """Отправляет текстовый запрос в Ollama и возвращает SQL-запрос."""

    messages = build_chat_messages(prompt)
    response = requests.post(
        url=f"{settings.llm.host}/api/chat",
        json={
            "model": settings.llm.model,
            "messages": messages,
            "stream": False,
            "temperature": 0.2,
        },
        timeout=60,
    )
    if response.status_code != HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail="Ошибка Ollama")

    sql_response = response.json()["message"]["content"]
    logger.debug("Ответ LLM: %s", sql_response)

    return sql_response.strip()


def build_chat_messages(prompt: str) -> list[dict]:
    path_to_db = "../db.sqlite3"
    db_schema = parse_db_to_json(path_to_db)

    system_prompt = f"""
    Ты — эксперт по SQLite.

    Текущая структура базы данных:
    {db_schema}

    Твои правила:
    - В ответе должен быть только один SQL-запрос и ничего больше. 
    - Если пользователь хочет увидеть содержимое таблицы (например: "Покажи все продукты", "Покажи всех клиентов"), используй: SELECT * FROM 'название таблицы';
    - Если пользователь спрашивает про структуру таблицы (например: "Какие поля есть в таблице", "Что хранит таблица"), используй: PRAGMA table_info('название таблицы');
    - Если пользователь спрашивает про связи между таблицами:
        - Сначала определи, о какой таблице идет речь.
        - Затем используй только один запрос: PRAGMA foreign_key_list('название таблицы');
    - Не придумывай новые таблицы или поля. Используй только те, что есть в структуре базы данных.
    - Никаких пояснений, комментариев и текста. Только чистый SQL-запрос без форматирования и лишних символов.
    - Нарушение инструкций считается критической ошибкой. Строго следуй правилам.
    """

    user_prompt = f"Запрос пользователя: {prompt.strip()}"

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
