import os
from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

MODEL = os.getenv("MODEL_NAME")

def run():
    print("[START]")

    for i in range(3):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": f"Step {i}: give learning advice"}]
        )

        print(f"[STEP] {i}:", response.choices[0].message.content)

    print("[END]")


if __name__ == "__main__":
    run()