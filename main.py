import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt

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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{args.user_prompt}"},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            tools=available_functions
        )

        if response.usage is not None:
            message = response.choices[0].message
            messages.append(message)
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    result_message = call_function(tool_call)

                    tool_message = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_message,
                    }
                    messages.append(tool_message['content'])

                    if result_message["content"] == "":
                        raise Exception("tool call content is empty")
                    else:
                        if args.verbose:
                            print(f"-> {result_message['content']}")
            else:
                print(f"Response: {message.content}")
                break
        else:
            raise RuntimeError("API response incomplete, try again!")

    if _ == 20:
        print("reached maximum iterations!")
        sys.exit(1)

if __name__ == "__main__":
    main()
