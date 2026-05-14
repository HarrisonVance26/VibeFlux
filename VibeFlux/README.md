# VibeFlux Package README

This package is part of the VibeFlux project.

For the full GitHub and PyPI documentation, see the project-level `README.md`:

- GitHub: <https://github.com/HarrisonVance26/VibeFlux>
- PyPI: <https://pypi.org/project/VibeFlux/>

VibeFlux is a pre-alpha Python toolkit for building computer-vision desktop applications with PySide6 / Qt, OpenCV, Pillow, reusable UI widgets, visualization utilities, SQLite helpers, and a lightweight OpenAI-compatible LLM client layer.

Version `0.8.0` adds:

- `VibeFlux.llms.LLMClient`
- `VibeFlux.llms.APIKeyManager`
- `VibeFlux.llms.ModelRegistry`
- JSON output templates
- image and file-assisted LLM helpers
- PySide6-friendly LLM workers
- compatibility import paths `VibeFlux.frames` and `VibeFlux.managers`

Keep API keys in a local `api_keys.json` file or environment variables. Do not commit real API keys.
