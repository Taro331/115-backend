import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "minimaxai/minimax-m3.1-flash"

HTTP_GET_TOOL = {
    "type": "function",
    "function": {
        "name": "http_get",
        "description": "Fetch a URL with HTTP GET. Return status code and a short body summary.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Absolute http(s) URL to fetch.",
                }
            },
            "required": ["url"],
        },
    },
}


def call_model(messages, tools=None):
    api_key = os.environ["NVIDIA_API_KEY"]
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 1,
        "top_p": 0.95,
    }
    if tools is not None:
        payload["tools"] = tools

    for attempt in range(1, 4):
        resp = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        print("status:", resp.status_code)
        if resp.status_code not in (429, 503, 529):
            break
        print(f"伺服器忙碌，{attempt * 5} 秒後重試...")
        time.sleep(attempt * 5)

    try:
        data = resp.json()
    except ValueError:
        print("error:", resp.text)
        raise SystemExit(1)

    if not resp.ok:
        print("error:", data.get("error", data))
        raise SystemExit(1)
    return data["choices"][0]["message"]


def http_get(url):
    resp = requests.get(url, timeout=10)
    return {
        "status_code": resp.status_code,
        "body_summary": resp.text[:120],
    }


def dispatch(name, arguments):
    if name != "http_get":
        raise ValueError(f"unknown tool: {name}")
    args = json.loads(arguments)
    return http_get(args["url"])


if __name__ == "__main__":
    messages = [
        {
            "role": "user",
            "content": "用 http_get 抓取 https://example.com，然後用一句話說明你看到什麼。",
        }
    ]

    print("===== 第一次 API 呼叫 =====")
    first = call_model(messages, tools=[HTTP_GET_TOOL])
    print("tool_calls:", json.dumps(first.get("tool_calls"), ensure_ascii=False, indent=2))
    if not first.get("tool_calls"):
        raise SystemExit("沒有拿到 tool_calls；先檢查工具描述與 user message。")

    messages.append(first)
    for call in first["tool_calls"]:
        print("===== 程式執行工具 =====")
        print("tool_call id:", call["id"])
        print("模型建議:", call["function"]["arguments"])
        result = dispatch(call["function"]["name"], call["function"]["arguments"])
        print("程式執行:", json.dumps(result, ensure_ascii=False))
        messages.append({
            "role": "tool",
            "tool_call_id": call["id"],
            "content": json.dumps(result, ensure_ascii=False),
        })

    print("===== 第二次 API 呼叫（不帶 tools）=====")
    final = call_model(messages)
    print("reply:", final.get("content"))