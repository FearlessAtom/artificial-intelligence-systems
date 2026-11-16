import argparse
import time

from openai import OpenAI

DEFAULT_SYSTEM = ("You are a helpful assistant for students. "
                  "Answer briefly and to the point, "
                  "unless the user asks otherwise.")

def parse_args():
    parser = argparse.ArgumentParser(description="Terminal chat with a local model.")
    parser.add_argument("--base-url", default="http://localhost:11434/v1")
    parser.add_argument("--model", default="qwen3:4b-instruct-2507-q4_K_M")
    parser.add_argument("--api-key", default="local")
    parser.add_argument("--system", default=DEFAULT_SYSTEM)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max-tokens", type=int, default=800)
    parser.add_argument("--max-history", type=int, default=20)

    return parser.parse_args()

def main():
    args = parse_args()
    client = OpenAI(base_url=args.base_url, api_key=args.api_key)
    extra = {"reasoning_effort": "none"}
    history = []

    print(f"Chat with {args.model}. Commands: /clear to reset the history, /exit to quit.")

    while True:
        try:
            text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not text:
            continue

        if text == "/exit":
            break

        if text == "/clear":
            history.clear()
            print("History cleared.")
            continue

        history.append({"role": "user", "content": text})
        messages = [{"role": "system", "content": args.system}] + history[-args.max_history:]

        start = time.perf_counter()
        first = usage = None
        answer = ""

        try:
            stream = client.chat.completions.create(
                model=args.model,
                messages=messages,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                stream=True,
                stream_options={"include_usage": True},
                extra_body=extra,
            )

            print("Assistant: ", end="", flush=True)

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    if first is None:
                        first = time.perf_counter()
                    piece = chunk.choices[0].delta.content
                    answer += piece
                    print(piece, end="", flush=True)
                if chunk.usage:
                    usage = chunk.usage

        except Exception as error:
            print(f"\nError: {error}. Check that the server is running and the model name is correct.")
            history.pop()
            continue
        end = time.perf_counter()
        print()

        history.append({"role": "assistant", "content": answer})

        if first is not None:
            stats = f"TTFT {first - start:.2f} s · total latency {end - start:.2f} s"
            if usage and usage.completion_tokens > 1 and end > first:
                stats += f" · {usage.completion_tokens} tokens · {(usage.completion_tokens - 1) / (end - first):.0f} tokens/s"
            print(f"[{stats}]")

if __name__ == "__main__":
    main()
