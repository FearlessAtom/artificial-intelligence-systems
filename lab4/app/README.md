A terminal chat with a local language model. It talks to any OpenAI-compatible server, streams the answer as it is generated, keeps the conversation history, and prints TTFT and tokens/s after every reply.

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com)
- The `openai` Python package

## Setup

```bash
pip install openai
ollama serve
ollama pull qwen3:4b-instruct-2507-q4_K_M
```

## Run

```bash
python main.py
```

Chat commands:

| Command  | What it does                     |
| -------- | -------------------------------- |
| `/clear` | Clear the conversation history   |
| `/exit`  | Quit (Ctrl+C also works)         |

## Options

```bash
python chatbot.py --model qwen3:8b                  # use another model
python chatbot.py --system "You turn lecture notes into flashcards."   # give it a role
python chatbot.py --temperature 0 --max-tokens 300  # deterministic, shorter answers
```
