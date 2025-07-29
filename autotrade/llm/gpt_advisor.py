import os
from openai import OpenAI

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


def ask_gpt(prompt: str) -> str:
    try:
        rsp = _client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return rsp.choices[0].message.content.strip()
    except Exception as exc:
        print("GPT error", exc)
        return ""
