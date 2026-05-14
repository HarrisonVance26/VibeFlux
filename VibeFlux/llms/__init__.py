# VibeFlux, AGPL-3.0 license
# File: llms/__init__.py | Created: 2026-05-13
"""
Unified LLM tools for VibeFlux.

This subpackage provides provider/model registry management, API key configuration, message construction, preset output
templates, a unified OpenAI-compatible client, and optional PySide6 worker helpers.
"""
from .Client import LLMAPIError, LLMClient, LLMResponse
from .Config import APIKeyManager, DEFAULT_API_CONFIG, default_config_path, package_example_config_path
from .Message import build_message, build_user_content, file_to_data_url, image_to_part, normalize_messages
from .Registry import ModelInfo, ModelRegistry, ProviderInfo, PRESET_MODELS, PRESET_PROVIDERS
from .Templates import OutputTemplate, get_template, list_templates, render_template_prompt, template_names
from .Updater import ModelPresetUpdateResult, ModelPresetUpdater

try:
    from .QtBridge import LLMQtRunner, LLMWorker
except Exception:
    LLMQtRunner = None
    LLMWorker = None

__all__ = (
    "APIKeyManager",
    "DEFAULT_API_CONFIG",
    "LLMAPIError",
    "LLMClient",
    "LLMQtRunner",
    "LLMResponse",
    "LLMWorker",
    "ModelInfo",
    "ModelPresetUpdateResult",
    "ModelPresetUpdater",
    "ModelRegistry",
    "OutputTemplate",
    "PRESET_MODELS",
    "PRESET_PROVIDERS",
    "ProviderInfo",
    "build_message",
    "build_user_content",
    "default_config_path",
    "file_to_data_url",
    "get_template",
    "image_to_part",
    "list_templates",
    "normalize_messages",
    "package_example_config_path",
    "render_template_prompt",
    "template_names",
)
