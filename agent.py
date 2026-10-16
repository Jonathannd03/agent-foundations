from tools import SEARCH_SCHEMA, TOOL_FUNCTIONS
from tool_calls import extract_tool_call
from error import LLMAPIError
from dotenv import load_dotenv
from datetime import date
import os
import httpx

load_dotenv()

API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.environ["OPENAI_MODEL"]

today = date.today().isoformat()


prompt = f"What are some news from the apoBank lately?"

tools = [SEARCH_SCHEMA]

messages = [
    {
        "role": "system",
        "content": f"Today is {today}.",
    },
    {
        "role": "user",
        "content": prompt,
    },
]


def call_llm(messages: list, tools: list) -> dict:
    response = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": MODEL,
            "messages": messages,
            "tools": tools,
        },
        timeout=30,
    )
    if response.status_code != 200:
        raise LLMAPIError(
            f"Request failed with status code {response.status_code}: {response.text}"
        )
    return response.json()


MAX_STEPS = 3
reached_max = True

for step in range(MAX_STEPS):
    print(f"Step number: {step + 1}")
    data = call_llm(messages, tools)
    call = extract_tool_call(data)

    if call is None:
        print("Final Answer:")
        print(data["choices"][0]["message"]["content"])
        reached_max = False
        break

    func = TOOL_FUNCTIONS[call["tool"]]
    tool_result = func(**call["args"])

    messages.append(data["choices"][0]["message"])
    messages.append(
        {
            "role": "tool",
            "tool_call_id": call["id"],
            "content": tool_result,
        }
    )
    print(f"Response: {data}")


if reached_max:
    print("Stopped: reached max steps without a final answer")
