from openai import OpenAI

def call_openai(prompt: str, api_key: str) -> str:
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content
