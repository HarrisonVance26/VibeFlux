# VibeFlux, AGPL-3.0 license
# File: examples/llm_usage.py | Created: 2026-05-13
"""
Minimal LLM usage example.

Before running this file, copy config/api_keys.example.json to api_keys.json and fill in one provider API key.
"""
from VibeFlux.llms import APIKeyManager, LLMClient


def main() -> None:
    """
    Run text, multi-turn, image, and file-assisted examples.
    """
    keys = APIKeyManager("api_keys.json")
    # Replace YOUR_API_KEY with a real key or set the provider environment variable.
    # keys.set_api_key("qwen", "YOUR_API_KEY")
    keys.set_active(provider="qwen", model="qwen-plus")

    client = LLMClient(config_path="api_keys.json")

    text_reply = client.single_chat("用三句话介绍 VibeFlux。")
    print(text_reply.content)

    client.reset_history(system="你是一个严谨的桌面视觉应用助手。")
    print(client.send("先记住：当前项目使用 PySide6。").content)
    print(client.send("上一句里我说项目使用什么 UI 框架？").content)

    # Vision-capable model example. Use qwen-vl-plus, glm-4.6v, or a Doubao vision model.
    # keys.set_active(provider="qwen", model="qwen-vl-plus")
    # image_reply = client.ask_image("sample.jpg", task="image_detection", response_format="json")
    # print(image_reply.content)

    # File-assisted example. Text files and PDFs with optional pypdf are supported.
    # file_reply = client.analyze_file("notes.md", task="file_summary", response_format="json")
    # print(file_reply.content)


if __name__ == "__main__":
    main()
