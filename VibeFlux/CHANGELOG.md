# Changelog

## 0.8.0 - 2026-05-13

- Added `VibeFlux.llms`, a unified OpenAI-compatible LLM calling layer.
- Added API key configuration through `api_keys.json` and `config/api_keys.example.json`.
- Added preset provider support for DeepSeek, Qwen / Alibaba Cloud Bailian, Doubao / Volcengine Ark, and ZhipuAI / GLM.
- Added preset and custom model management through `ModelRegistry`.
- Added single-turn, multi-turn, streaming, image, and file-assisted chat helpers.
- Added preset structured JSON output templates for detection, segmentation, image understanding, text extraction, file summaries, and structured reports.
- Added PySide6-friendly LLM workers through `LLMWorker` and `LLMQtRunner`.
