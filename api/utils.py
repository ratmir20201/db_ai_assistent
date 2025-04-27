import re


def extract_sql_query(text: str) -> str:
    """Извлекает SQL-запрос из текста."""

    match = re.search(r"```(?:sql)?\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        sql_query = match.group(1)
        return sql_query.strip()
    raise Exception(f"SQL-запрос не найден в тексте. {text}")
