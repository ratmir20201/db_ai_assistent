import requests
from fastapi import HTTPException
from starlette.status import HTTP_200_OK

from config import settings
from logger import logger


def generate_sql(user_prompt: str):
    """Отправляет текстовый запрос в Ollama и возвращает SQL-запрос."""

    db_schema = ""
    base_prompt = f"""
    Ты — эксперт по базам данных и генерации SQL-запросов.
    Твоя задача: по запросу пользователя возвращать только рабочий SQL-запрос без дополнительных пояснений или текста.

    Текущая структура базы данных:
    {db_schema}

    Условия работы:
    - Ты знаешь структуру базы данных: таблицы, их поля и связи между ними.
    - Ты понимаешь связи между таблицами и используешь их корректно в запросах.
    - Ты никогда не обращаешься к несуществующим таблицам или полям.
    - Ты умеешь строить запросы на основе естественного языка:
        - Например: “Покажи топ 5 клиентов по выручке за 2024 год”, “Какие таблицы связаны с клиентами?”.
    - Ты умеешь использовать SQL-конструкции: WHERE, ORDER BY, GROUP BY, LIMIT, а также агрегатные функции (SUM, AVG, COUNT и др.).
    - Всегда возвращай только чистый SQL-код, без пояснений, комментариев или форматирования в стиле Markdown.
    - Если запрос предполагает выборку — используй SELECT.
    - Если требуется фильтрация или сортировка — добавляй соответствующие условия.
    - Если в запросе просят "показать" — используй SELECT.

    Очень важно: не пиши ничего, кроме одного SQL-запроса.

    Запрос пользователя: '{user_prompt}'
    """

    response = requests.post(
        url=f"{settings.llm.host}/api/generate",
        json={
            "model": settings.llm.model,
            "prompt": base_prompt,
            "stream": False,
            "temperature": 0.2,
        },
        timeout=30,
    )
    if response.status_code != HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail="Ошибка Ollama")

    sql_response = response.json()["response"]
    logger.debug("Ответ LLM: %s", sql_response)
    # sql_query = extract_sql_query(sql_response)

    return sql_response
