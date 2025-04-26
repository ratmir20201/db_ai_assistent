from openai import OpenAI

from config import settings

# openai.api_key = settings.open_ai.api_key
client = OpenAI(api_key=settings.open_ai.api_key)


def generate_sql(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Ты SQL-ассистент. Отвечай только SQL-запросам.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    print(response)
    return response
