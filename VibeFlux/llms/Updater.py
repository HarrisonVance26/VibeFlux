# VibeFlux, AGPL-3.0 license
# File: llms/Updater.py | Created: 2026-05-13
"""
Model preset updater for OpenAI-compatible LLM services.

The updater calls a provider's model list endpoint, converts returned model IDs into ModelInfo entries, and saves new
models as custom entries in api_keys.json. This keeps the built-in preset table stable while allowing users to refresh
the selectable model list from official provider APIs.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from .Config import APIKeyManager
from .Registry import ModelInfo, ModelRegistry, ProviderInfo


@dataclass
class ModelPresetUpdateResult:
    """
    Result returned after refreshing model presets from a provider endpoint.
    """
    provider: str
    endpoint: str
    models: List[ModelInfo] = field(default_factory=list)
    added: List[ModelInfo] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    saved: bool = False
    error: str = ""

    @property
    def added_names(self) -> List[str]:
        """
        Return names of models added to the registry.
        """
        return [item.name for item in self.added]


class ModelPresetUpdater:
    """
    Refresh provider model entries from OpenAI-compatible model list APIs.
    """

    def __init__(self,
                 config_path: Optional[str] = None,
                 registry: Optional[ModelRegistry] = None,
                 timeout: int = 30) -> None:
        """
        Initialize the updater.
        """
        self.config = APIKeyManager(config_path=config_path, auto_create=True)
        self.registry = registry or ModelRegistry()
        self.config.load_custom_models_to_registry(self.registry)
        self.timeout = timeout

    def refresh_provider(self,
                         provider: Optional[str] = None,
                         api_key: Optional[str] = None,
                         base_url: Optional[str] = None,
                         endpoint: str = "/models",
                         save: bool = True,
                         overwrite: bool = False) -> ModelPresetUpdateResult:
        """
        Fetch and merge model entries for one provider.
        """
        provider_info = self._resolve_provider(provider)
        request_url = ""
        try:
            request_url = self._build_url(self._effective_base_url(provider_info.name, base_url), endpoint)
            result = ModelPresetUpdateResult(provider=provider_info.name, endpoint=request_url)
            models = self.fetch_provider_models(
                provider=provider_info.name,
                api_key=api_key,
                base_url=base_url,
                endpoint=endpoint,
            )
        except Exception as exc:
            result = ModelPresetUpdateResult(provider=provider_info.name, endpoint=request_url)
            result.error = str(exc)
            return result

        result.models = models
        for model in models:
            if self._is_registered_model(model, overwrite=overwrite):
                result.skipped.append(model.name)
                continue
            self.registry.add_model(model)
            result.added.append(model)

        if save and result.added:
            self.config.upsert_custom_models([item.to_dict() for item in result.added], save=True)
            result.saved = True
        return result

    def refresh_all(self,
                    providers: Optional[Iterable[str]] = None,
                    save: bool = True,
                    overwrite: bool = False) -> List[ModelPresetUpdateResult]:
        """
        Refresh all configured providers. Providers without an API key return an error result.
        """
        if providers is None:
            providers = [item.name for item in self.registry.list_providers() if item.name != "custom"]
        output: List[ModelPresetUpdateResult] = []
        for provider in providers:
            output.append(self.refresh_provider(provider=provider, save=save, overwrite=overwrite))
        return output

    def fetch_provider_models(self,
                              provider: Optional[str] = None,
                              api_key: Optional[str] = None,
                              base_url: Optional[str] = None,
                              endpoint: str = "/models") -> List[ModelInfo]:
        """
        Call a provider model list API and return normalized ModelInfo entries.
        """
        provider_info = self._resolve_provider(provider)
        request_url = self._build_url(self._effective_base_url(provider_info.name, base_url), endpoint)
        token = api_key if api_key is not None else self.config.get_api_key(provider_info.name)
        if not token:
            raise ValueError(
                "API key is empty for provider '{provider}'. Enter one in the config dialog or set {env_name}.".format(
                    provider=provider_info.name,
                    env_name=provider_info.api_key_env or "the provider API key environment variable",
                )
            )

        payload = self._request_models(request_url, token)
        return self.parse_provider_models(provider_info.name, payload)

    def parse_provider_models(self, provider: str, payload: Any) -> List[ModelInfo]:
        """
        Parse a provider model list response into ModelInfo entries.
        """
        provider_info = self._resolve_provider(provider)
        items = self._extract_model_items(payload)
        output: List[ModelInfo] = []
        seen: set = set()
        for item in items:
            model_id = self._model_id_from_item(item)
            if not model_id:
                continue
            key = model_id.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            output.append(self._model_info_from_id(provider_info, model_id, item))
        return output

    def _resolve_provider(self, provider: Optional[str]) -> ProviderInfo:
        """
        Resolve a provider from an explicit name or the active configuration.
        """
        provider_name = (provider or self.config.get_active_provider()).strip().lower()
        return self.registry.get_provider(provider_name)

    def _effective_base_url(self, provider: str, base_url: Optional[str]) -> str:
        """
        Resolve a base URL from an explicit value, config, or provider preset.
        """
        if base_url:
            return base_url
        provider_info = self.registry.get_provider(provider)
        return self.config.get_base_url(provider) or provider_info.base_url

    def _build_url(self, base_url: str, endpoint: str) -> str:
        """
        Join a provider base URL and endpoint.
        """
        if not base_url:
            raise ValueError("base_url is empty. Please configure provider base_url in api_keys.json.")
        return base_url.rstrip("/") + "/" + endpoint.lstrip("/")

    def _request_models(self, url: str, api_key: str) -> Any:
        """
        Send a GET request to a model list endpoint and parse JSON.
        """
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + api_key,
        }
        request = urllib.request.Request(url=url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            message = "HTTP {code} {reason}".format(code=exc.code, reason=exc.reason)
            if body:
                message += ": " + body[:500]
            raise RuntimeError(message)
        except urllib.error.URLError as exc:
            raise RuntimeError(str(exc.reason))

    def _extract_model_items(self, payload: Any) -> List[Any]:
        """
        Extract likely model entries from common model-list response shapes.
        """
        if isinstance(payload, list):
            return list(payload)
        if not isinstance(payload, dict):
            return []

        for key in ("data", "models", "items", "model_list", "available_models", "result"):
            value = payload.get(key)
            items = self._extract_model_items(value)
            if items:
                return items
        if self._model_id_from_item(payload):
            return [payload]
        return []

    def _model_id_from_item(self, item: Any) -> str:
        """
        Return the model ID from a string or dictionary item.
        """
        if isinstance(item, str):
            return item
        if not isinstance(item, dict):
            return ""
        for key in ("id", "model", "model_id", "name", "modelName"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    def _model_info_from_id(self, provider: ProviderInfo, model_id: str, raw: Any) -> ModelInfo:
        """
        Convert one remote model ID into a ModelInfo object.
        """
        model_type, capabilities = self._infer_model_profile(model_id)
        extra = {"source": "models_endpoint"}
        if isinstance(raw, dict):
            for key in ("object", "owned_by", "created", "permission"):
                if key in raw:
                    extra[key] = raw[key]
            raw_capabilities = raw.get("capabilities")
            if isinstance(raw_capabilities, Sequence) and not isinstance(raw_capabilities, (str, bytes)):
                capabilities = self._merge_capabilities(capabilities, [str(item) for item in raw_capabilities])

        return ModelInfo(
            name=model_id,
            provider=provider.name,
            api_model=model_id,
            model_type=model_type,
            capabilities=capabilities,
            description="Remote model fetched from {provider}.".format(provider=provider.display_name),
            extra=extra,
        )

    def _infer_model_profile(self, model_id: str) -> Tuple[str, Tuple[str, ...]]:
        """
        Infer a conservative model type and capabilities from a model ID.
        """
        name = model_id.lower()
        model_type = "chat"
        capabilities: List[str] = ["text", "stream", "json"]

        image_generation_terms = (
            "seedream", "wanx", "cogview", "flux", "image-generation", "image_generation", "text-to-image"
        )
        video_generation_terms = ("cogvideo", "video-generation", "video_generation", "text-to-video")
        embedding_terms = ("embedding", "embed", "text-embedding")
        rerank_terms = ("rerank", "reranker")
        audio_terms = ("audio", "speech", "tts", "asr")
        vision_terms = ("vl", "vision", "qvq", "omni", "5v", "4.6v", "ocr", "visual", "multimodal")
        reasoning_terms = ("reasoner", "reasoning", "thinking", "r1", "qvq", "deepseek-v4", "qwen3", "glm-5", "glm-4.7")

        if any(term in name for term in embedding_terms):
            return "embedding", ("embedding",)
        if any(term in name for term in rerank_terms):
            return "rerank", ("rerank",)
        if any(term in name for term in image_generation_terms):
            return "image_generation", ("text", "image", "image_generation")
        if any(term in name for term in video_generation_terms):
            return "video_generation", ("text", "video", "video_generation")

        if any(term in name for term in audio_terms):
            model_type = "audio"
            capabilities.extend(["audio"])
        if "omni" in name:
            model_type = "omni"
            capabilities.extend(["vision", "image", "audio", "video"])
        elif any(term in name for term in vision_terms):
            model_type = "document" if "ocr" in name else "vision"
            capabilities.extend(["vision", "image"])
            if "video" in name or "vl" in name or "omni" in name:
                capabilities.append("video")
            if "ocr" in name or "document" in name or "long" in name:
                capabilities.extend(["file", "ocr"])
        if "code" in name or "coder" in name:
            capabilities.append("code")
        if any(term in name for term in reasoning_terms):
            capabilities.append("reasoning")
        if "tool" in name or "function" in name:
            capabilities.append("tool")
        return model_type, self._merge_capabilities((), capabilities)

    def _merge_capabilities(self, base: Iterable[str], updates: Iterable[str]) -> Tuple[str, ...]:
        """
        Merge capability lists while preserving order.
        """
        output: List[str] = []
        for item in list(base) + list(updates):
            value = str(item).strip().lower()
            if value and value not in output:
                output.append(value)
        return tuple(output)

    def _is_registered_model(self, model: ModelInfo, overwrite: bool = False) -> bool:
        """
        Return True when a model already exists and should not be overwritten.
        """
        if overwrite:
            return False
        try:
            existing = self.registry.get_model(model.name)
        except KeyError:
            return False
        return existing.provider.strip().lower() == model.provider.strip().lower()
