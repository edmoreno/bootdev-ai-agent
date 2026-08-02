import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("OpenRouter API key could not be found!")


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    model = "nvidia/nemotron-3-ultra-550b-a55b:free"

    messages = [
        {"role": "user", "content": f"{args.user_prompt}"},
    ]

    response = client.chat.completions.create(messages=messages, model=model)

    if response.usage is not None:
        if args.verbose is True:
            print(f"User prompt: {messages[0]['content']}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        print(f"Response: {response.choices[0].message.content}")
    else:
        raise RuntimeError("API response incomplete, try again!")


if __name__ == "__main__":
    main()
