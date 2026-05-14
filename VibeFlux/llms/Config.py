# VibeFlux, AGPL-3.0 license
# File: llms/Config.py | Created: 2026-05-13
"""
API key and LLM configuration manager.

The manager reads and writes an api_keys.json file. It keeps API keys outside source code and exposes simple methods
that PySide6 settings dialogs can call after a user enters a provider key or selects a model.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List, Optional

from .Registry import ModelInfo, ModelRegistry, PRESET_PROVIDERS


DEFAULT_API_CONFIG: Dict[str, Any] = {
    "active_provider": "qwen",
    "active_model": "qwen-plus",
    "providers": {
        "deepseek": {
            "api_key": "",
            "base_url": PRESET_PROVIDERS["deepseek"].base_url,
            "api_key_env": PRESET_PROVIDERS["deepseek"].api_key_env,
        },
        "qwen": {
            "api_key": "",
            "base_url": PRESET_PROVIDERS["qwen"].base_url,
            "api_key_env": PRESET_PROVIDERS["qwen"].api_key_env,
        },
        "doubao": {
            "api_key": "",
            "base_url": PRESET_PROVIDERS["doubao"].base_url,
            "api_key_env": PRESET_PROVIDERS["doubao"].api_key_env,
        },
        "zhipu": {
            "api_key": "",
            "base_url": PRESET_PROVIDERS["zhipu"].base_url,
            "api_key_env": PRESET_PROVIDERS["zhipu"].api_key_env,
        },
        "custom": {
            "api_key": "",
            "base_url": "",
            "api_key_env": "",
        },
    },
    "models": {
        "custom": []
    },
    "runtime": {
        "timeout": 60,
        "max_retries": 2,
        "temperature": 0.2,
        "max_file_chars": 20000,
        "thinking_mode": "auto",
        "return_reasoning": True,
    },
}


def default_config_path(filename: str = "api_keys.json") -> str:
    """
    Return the default runtime configuration path in the current working directory.
    """
    return os.path.abspath(os.path.join(os.getcwd(), filename))


def package_example_config_path() -> str:
    """
    Return the path of the packaged api_keys example file.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(base_dir, "config", "api_keys.example.json")


def _deep_merge(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries and return a new dictionary.
    """
    result = dict(base)
    for key, value in update.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class APIKeyManager:
    """
    Manage the api_keys.json file used by LLM clients.
    """

    def __init__(self, config_path: Optional[str] = None, auto_create: bool = True) -> None:
        """
        Initialize the key manager.

        Args:
            config_path (Optional[str]): Path to api_keys.json. Defaults to the current working directory.
            auto_create (bool): Create a default file when it does not exist.
        """
        self.config_path = os.path.abspath(config_path or default_config_path())
        self.data: Dict[str, Any] = json.loads(json.dumps(DEFAULT_API_CONFIG))
        if os.path.exists(self.config_path):
            self.load()
        elif auto_create:
            self.save()

    def load(self) -> Dict[str, Any]:
        """
        Load api_keys.json and merge it with default values.
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                user_data = json.load(file)
            self.data = _deep_merge(DEFAULT_API_CONFIG, user_data)
        except FileNotFoundError:
            self.data = json.loads(json.dumps(DEFAULT_API_CONFIG))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON configuration file: {self.config_path}. {e}")
        return self.data

    def save(self) -> None:
        """
        Save api_keys.json to disk.
        """
        folder = os.path.dirname(self.config_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)

    def ensure_provider(self, provider: str) -> Dict[str, Any]:
        """
        Ensure a provider block exists in api_keys.json.
        """
        key = provider.strip().lower()
        providers = self.data.setdefault("providers", {})
        if key not in providers:
            preset = PRESET_PROVIDERS.get(key)
            providers[key] = {
                "api_key": "",
                "base_url": preset.base_url if preset else "",
                "api_key_env": preset.api_key_env if preset else "",
            }
        return providers[key]

    def set_api_key(self, provider: str, api_key: str, save: bool = True) -> None:
        """
        Store an API key for a provider.
        """
        provider_data = self.ensure_provider(provider)
        provider_data["api_key"] = api_key or ""
        if save:
            self.save()

    def get_api_key(self, provider: str, env_fallback: bool = True) -> str:
        """
        Get the API key for a provider, optionally falling back to environment variables.
        """
        provider_data = self.ensure_provider(provider)
        api_key = provider_data.get("api_key", "")
        if api_key:
            return api_key
        if env_fallback:
            env_name = provider_data.get("api_key_env") or PRESET_PROVIDERS.get(provider, PRESET_PROVIDERS["custom"]).api_key_env
            if env_name:
                return os.environ.get(env_name, "")
        return ""

    def set_base_url(self, provider: str, base_url: str, save: bool = True) -> None:
        """
        Store the base URL for a provider.
        """
        provider_data = self.ensure_provider(provider)
        provider_data["base_url"] = base_url or ""
        if save:
            self.save()

    def get_base_url(self, provider: str) -> str:
        """
        Get a provider base URL from api_keys.json or presets.
        """
        provider_key = provider.strip().lower()
        provider_data = self.ensure_provider(provider_key)
        base_url = provider_data.get("base_url", "")
        if base_url:
            return base_url
        preset = PRESET_PROVIDERS.get(provider_key)
        return preset.base_url if preset else ""

    def set_active(self, provider: Optional[str] = None, model: Optional[str] = None, save: bool = True) -> None:
        """
        Set the active provider and model.
        """
        if provider:
            self.data["active_provider"] = provider.strip().lower()
        if model:
            self.data["active_model"] = model
        if save:
            self.save()

    def get_active_provider(self) -> str:
        """
        Return the active provider key.
        """
        return self.data.get("active_provider", "qwen")

    def get_active_model(self) -> str:
        """
        Return the active model name.
        """
        return self.data.get("active_model", "qwen-plus")

    def get_runtime(self, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get runtime options from the configuration.
        """
        runtime = self.data.setdefault("runtime", {})
        if key is None:
            return runtime
        return runtime.get(key, default)

    def set_runtime(self, key: str, value: Any, save: bool = True) -> None:
        """
        Store a runtime option such as timeout or temperature.
        """
        self.data.setdefault("runtime", {})[key] = value
        if save:
            self.save()

    def add_custom_model(self, provider: str, name: str, api_model: Optional[str] = None,
                         capabilities: Optional[Iterable[str]] = None,
                         model_type: str = "chat", description: str = "Custom model",
                         save: bool = True) -> Dict[str, Any]:
        """
        Add a custom model definition to api_keys.json.
        """
        item = ModelInfo(
            name=name,
            provider=provider.strip().lower(),
            api_model=api_model or name,
            capabilities=tuple(capabilities or ("text", "stream", "json")),
            model_type=model_type,
            description=description,
        ).to_dict()
        models = self.data.setdefault("models", {}).setdefault("custom", [])
        models.append(item)
        if save:
            self.save()
        return item

    def upsert_custom_models(self, models: Iterable[Dict[str, Any]], save: bool = True) -> List[Dict[str, Any]]:
        """
        Add or replace custom model definitions in api_keys.json.
        """
        stored = self.data.setdefault("models", {}).setdefault("custom", [])
        model_index: Dict[tuple, int] = {}
        for index, item in enumerate(stored):
            try:
                info = ModelInfo.from_dict(item)
                key = (info.provider.strip().lower(), info.name.strip().lower())
            except Exception:
                provider = str(item.get("provider", "")).strip().lower()
                name = str(item.get("name", "")).strip().lower()
                key = (provider, name)
            model_index[key] = index

        updated: List[Dict[str, Any]] = []
        for item in models:
            info = ModelInfo.from_dict(item)
            key = (info.provider.strip().lower(), info.name.strip().lower())
            model_data = info.to_dict()
            if key in model_index:
                stored[model_index[key]] = model_data
            else:
                model_index[key] = len(stored)
                stored.append(model_data)
            updated.append(model_data)

        if save and updated:
            self.save()
        return updated

    def get_custom_models(self) -> List[Dict[str, Any]]:
        """
        Return custom model definitions from api_keys.json.
        """
        return list(self.data.get("models", {}).get("custom", []))

    def load_custom_models_to_registry(self, registry: Optional[ModelRegistry] = None) -> ModelRegistry:
        """
        Load custom models from api_keys.json into a registry.
        """
        target = registry or ModelRegistry()
        target.load_custom_models(self.get_custom_models())
        return target

    def mask_api_key(self, api_key: str) -> str:
        """
        Return a masked API key suitable for display.
        """
        if not api_key:
            return ""
        if len(api_key) <= 8:
            return "*" * len(api_key)
        return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]

    def to_safe_dict(self) -> Dict[str, Any]:
        """
        Export configuration with masked API keys.
        """
        safe = json.loads(json.dumps(self.data))
        for provider_data in safe.get("providers", {}).values():
            provider_data["api_key"] = self.mask_api_key(provider_data.get("api_key", ""))
        return safe

    def create_example_file(self, output_path: Optional[str] = None) -> str:
        """
        Create an example API key file and return its path.
        """
        target = os.path.abspath(output_path or package_example_config_path())
        folder = os.path.dirname(target)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        with open(target, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_API_CONFIG, file, indent=2, ensure_ascii=False)
        return target
