# VibeFlux, AGPL-3.0 license
# File: llms/Registry.py | Created: 2026-05-13
"""
Model and provider registry for OpenAI-compatible LLM services.

The registry stores the provider endpoint, API key environment variable, preset model names, and model capabilities.
It also supports adding custom model names at runtime so a GUI can expose both built-in and user-defined models.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple


@dataclass
class ProviderInfo:
    """
    Describes one LLM provider.

    Args:
        name (str): Internal provider key.
        display_name (str): Human-readable provider name.
        base_url (str): OpenAI-compatible base URL.
        api_key_env (str): Environment variable used as a fallback for API keys.
        chat_endpoint (str): Chat completions endpoint under base_url.
        image_endpoint (str): Image generation endpoint under base_url.
        description (str): Short description shown in UI or logs.
        docs_url (str): Official documentation URL.
    """
    name: str
    display_name: str
    base_url: str
    api_key_env: str = ""
    chat_endpoint: str = "/chat/completions"
    image_endpoint: str = "/images/generations"
    description: str = ""
    docs_url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the provider object to a dictionary.
        """
        return asdict(self)


@dataclass
class ModelInfo:
    """
    Describes one model entry.

    Args:
        name (str): Model display name or user-facing name.
        provider (str): Provider key, such as deepseek, qwen, doubao, or zhipu.
        api_model (str): Model ID passed to the API. If empty, name is used.
        model_type (str): Model type, usually chat, vision, audio, video, document, or image_generation.
        capabilities (Tuple[str, ...]): Capabilities such as text, vision, file, stream, json, tool, reasoning.
        description (str): Short description.
        aliases (Tuple[str, ...]): Additional names that can resolve to this model.
        extra (Dict[str, Any]): Extra provider-specific metadata.
    """
    name: str
    provider: str
    api_model: str = ""
    model_type: str = "chat"
    capabilities: Tuple[str, ...] = field(default_factory=tuple)
    description: str = ""
    aliases: Tuple[str, ...] = field(default_factory=tuple)
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Fill the API model with the display name if it was not explicitly provided.
        """
        if not self.api_model:
            self.api_model = self.name

    def supports(self, capability: str) -> bool:
        """
        Check whether the model supports a capability.
        """
        return capability in self.capabilities

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model object to a JSON-serializable dictionary.
        """
        data = asdict(self)
        data["capabilities"] = list(self.capabilities)
        data["aliases"] = list(self.aliases)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelInfo":
        """
        Build a ModelInfo from a dictionary loaded from JSON.
        """
        clean = dict(data)
        clean["capabilities"] = tuple(clean.get("capabilities", ()))
        clean["aliases"] = tuple(clean.get("aliases", ()))
        clean.setdefault("extra", {})
        return cls(**clean)


PRESET_PROVIDERS: Dict[str, ProviderInfo] = {
    "deepseek": ProviderInfo(
        name="deepseek",
        display_name="DeepSeek",
        base_url="https://api.deepseek.com",
        api_key_env="DEEPSEEK_API_KEY",
        description="DeepSeek OpenAI-compatible chat API.",
        docs_url="https://api-docs.deepseek.com/",
    ),
    "qwen": ProviderInfo(
        name="qwen",
        display_name="Alibaba Cloud Bailian / Qwen",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key_env="DASHSCOPE_API_KEY",
        description="Alibaba Cloud Model Studio OpenAI-compatible Qwen API.",
        docs_url="https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions",
    ),
    "doubao": ProviderInfo(
        name="doubao",
        display_name="Volcengine Ark / Doubao",
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key_env="ARK_API_KEY",
        description="Volcengine Ark OpenAI-compatible model API.",
        docs_url="https://www.volcengine.com/docs/82379/1330626",
    ),
    "zhipu": ProviderInfo(
        name="zhipu",
        display_name="ZhipuAI / GLM",
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        api_key_env="ZAI_API_KEY",
        description="ZhipuAI OpenAI-compatible GLM API.",
        docs_url="https://docs.bigmodel.cn/cn/guide/develop/openai/introduction",
    ),
    "custom": ProviderInfo(
        name="custom",
        display_name="Custom OpenAI-compatible Provider",
        base_url="",
        api_key_env="",
        description="A user-defined OpenAI-compatible provider.",
    ),
}


PRESET_MODELS: Dict[str, ModelInfo] = {
    # DeepSeek
    "deepseek-v4-pro": ModelInfo(
        name="deepseek-v4-pro",
        provider="deepseek",
        model_type="chat",
        capabilities=("text", "stream", "json", "reasoning"),
        description="DeepSeek V4 Pro chat and reasoning model.",
    ),
    "deepseek-v4-flash": ModelInfo(
        name="deepseek-v4-flash",
        provider="deepseek",
        model_type="chat",
        capabilities=("text", "stream", "json", "reasoning"),
        description="DeepSeek V4 Flash chat model.",
    ),
    "deepseek-chat": ModelInfo(
        name="deepseek-chat",
        provider="deepseek",
        model_type="chat",
        capabilities=("text", "stream", "json"),
        description="Backward-compatible DeepSeek chat model name.",
    ),
    "deepseek-reasoner": ModelInfo(
        name="deepseek-reasoner",
        provider="deepseek",
        model_type="chat",
        capabilities=("text", "stream", "json", "reasoning"),
        description="Backward-compatible DeepSeek reasoning model name.",
    ),

    # Qwen / DashScope OpenAI-compatible models
    "qwen3-max": ModelInfo(
        name="qwen3-max",
        provider="qwen",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool", "reasoning"),
        description="Qwen3 Max stable commercial model.",
    ),
    "qwen3-max-2026-01-23": ModelInfo(
        name="qwen3-max-2026-01-23",
        provider="qwen",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool", "reasoning"),
        description="Qwen3 Max snapshot model.",
    ),
    "qwen3-max-2025-09-23": ModelInfo(
        name="qwen3-max-2025-09-23",
        provider="qwen",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool"),
        description="Qwen3 Max snapshot model.",
    ),
    "qwen3.5-plus": ModelInfo(
        name="qwen3.5-plus",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json", "tool"),
        description="Qwen3.5 Plus flagship multimodal model.",
    ),
    "qwen3.5-flash": ModelInfo(
        name="qwen3.5-flash",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json"),
        description="Qwen3.5 Flash low-latency multimodal model.",
    ),
    "qwen-plus": ModelInfo(
        name="qwen-plus",
        provider="qwen",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool"),
        description="General-purpose Qwen Plus chat model.",
    ),
    "qwen-max": ModelInfo(
        name="qwen-max",
        provider="qwen",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool"),
        description="Higher-capability Qwen Max chat model.",
    ),
    "qwen-turbo": ModelInfo(
        name="qwen-turbo",
        provider="qwen",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool"),
        description="Lower-latency Qwen Turbo chat model.",
    ),
    "qwen-long": ModelInfo(
        name="qwen-long",
        provider="qwen",
        model_type="chat",
        capabilities=("text", "file", "stream", "json"),
        description="Qwen long-context model for long documents and text.",
    ),
    "qwen3-vl-plus": ModelInfo(
        name="qwen3-vl-plus",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json", "reasoning"),
        description="Qwen3 VL Plus stable vision-language model.",
    ),
    "qwen3-vl-plus-2025-12-19": ModelInfo(
        name="qwen3-vl-plus-2025-12-19",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json", "reasoning"),
        description="Qwen3 VL Plus snapshot model.",
    ),
    "qwen3-vl-plus-2025-09-23": ModelInfo(
        name="qwen3-vl-plus-2025-09-23",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json", "reasoning"),
        description="Qwen3 VL Plus snapshot model.",
    ),
    "qwen3-vl-flash": ModelInfo(
        name="qwen3-vl-flash",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json", "reasoning"),
        description="Qwen3 VL Flash stable vision-language model.",
    ),
    "qwen3-vl-flash-2026-01-22": ModelInfo(
        name="qwen3-vl-flash-2026-01-22",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json", "reasoning"),
        description="Qwen3 VL Flash snapshot model.",
    ),
    "qwen3-vl-flash-2025-10-15": ModelInfo(
        name="qwen3-vl-flash-2025-10-15",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json", "reasoning"),
        description="Qwen3 VL Flash snapshot model.",
    ),
    "qwen3-vl-235b-a22b-thinking": ModelInfo(
        name="qwen3-vl-235b-a22b-thinking",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json", "reasoning"),
        description="Qwen3 VL open-weight thinking model served by Model Studio.",
    ),
    "qwen3-vl-235b-a22b-instruct": ModelInfo(
        name="qwen3-vl-235b-a22b-instruct",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json"),
        description="Qwen3 VL open-weight instruct model served by Model Studio.",
    ),
    "qwen-vl-plus": ModelInfo(
        name="qwen-vl-plus",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json"),
        description="Qwen vision-language model for image and video understanding.",
    ),
    "qwen-vl-max": ModelInfo(
        name="qwen-vl-max",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "stream", "json"),
        description="Higher-capability Qwen vision-language model.",
    ),
    "qwen-omni-turbo": ModelInfo(
        name="qwen-omni-turbo",
        provider="qwen",
        model_type="omni",
        capabilities=("text", "vision", "image", "audio", "video", "stream", "json"),
        description="Qwen multimodal model for text, image, audio, and video inputs.",
    ),
    "qvq-max": ModelInfo(
        name="qvq-max",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "stream", "json", "reasoning"),
        description="QVQ vision reasoning model.",
    ),
    "qvq-plus": ModelInfo(
        name="qvq-plus",
        provider="qwen",
        model_type="vision",
        capabilities=("text", "vision", "image", "stream", "json", "reasoning"),
        description="QVQ Plus vision reasoning model.",
    ),
    "qwen-vl-ocr": ModelInfo(
        name="qwen-vl-ocr",
        provider="qwen",
        model_type="document",
        capabilities=("text", "vision", "image", "file", "ocr", "stream", "json"),
        description="Qwen VL OCR model.",
    ),

    # Doubao / Volcengine Ark models. The display aliases keep the capitalized names requested by users.
    "doubao-seed-2-0-pro-260215": ModelInfo(
        name="doubao-seed-2-0-pro-260215",
        provider="doubao",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "file", "stream", "json", "reasoning", "tool"),
        description="Doubao Seed 2.0 Pro model on Volcengine Ark.",
        aliases=("Doubao-Seed-2.0-pro", "doubao-seed-2.0-pro"),
    ),
    "doubao-seed-2-0-mini-260215": ModelInfo(
        name="doubao-seed-2-0-mini-260215",
        provider="doubao",
        model_type="vision",
        capabilities=("text", "vision", "image", "file", "stream", "json"),
        description="Doubao Seed 2.0 Mini model on Volcengine Ark.",
        aliases=("Doubao-Seed-2.0-mini", "doubao-seed-2.0-mini"),
    ),
    "doubao-seed-2-0-lite-260215": ModelInfo(
        name="doubao-seed-2-0-lite-260215",
        provider="doubao",
        model_type="chat",
        capabilities=("text", "stream", "json"),
        description="Doubao Seed 2.0 Lite model on Volcengine Ark.",
        aliases=("Doubao-Seed-2.0-lite", "doubao-seed-2.0-lite"),
    ),
    "doubao-seed-2-0-code-260215": ModelInfo(
        name="doubao-seed-2-0-code-260215",
        provider="doubao",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool", "code"),
        description="Doubao Seed 2.0 Code model on Volcengine Ark.",
        aliases=("Doubao-Seed-2.0-Code", "doubao-seed-2.0-code"),
    ),
    "doubao-seed-1-8-251228": ModelInfo(
        name="doubao-seed-1-8-251228",
        provider="doubao",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "file", "stream", "json", "reasoning", "tool"),
        description="Doubao Seed 1.8 vision-language model on Volcengine Ark.",
        aliases=("Doubao-seed-1-8", "doubao-seed-1.8"),
    ),
    "doubao-seed-1-6-vision-250815": ModelInfo(
        name="doubao-seed-1-6-vision-250815",
        provider="doubao",
        model_type="vision",
        capabilities=("text", "vision", "image", "stream", "json"),
        description="Doubao Seed 1.6 vision model on Volcengine Ark.",
        aliases=("Doubao-seed-1-6-vision", "doubao-seed-1.6-vision"),
    ),
    "doubao-seed-1-6-251015": ModelInfo(
        name="doubao-seed-1-6-251015",
        provider="doubao",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool"),
        description="Doubao Seed 1.6 chat model on Volcengine Ark.",
        aliases=("Doubao-seed-1-6", "doubao-seed-1.6"),
    ),
    "doubao-seed-1-6-flash-250828": ModelInfo(
        name="doubao-seed-1-6-flash-250828",
        provider="doubao",
        model_type="chat",
        capabilities=("text", "stream", "json"),
        description="Doubao Seed 1.6 Flash chat model on Volcengine Ark.",
        aliases=("Doubao-seed-1-6-flash", "doubao-seed-1.6-flash"),
    ),
    "doubao-1-5-vision-pro-32k-250115": ModelInfo(
        name="doubao-1-5-vision-pro-32k-250115",
        provider="doubao",
        model_type="vision",
        capabilities=("text", "vision", "image", "stream", "json"),
        description="Doubao 1.5 Vision Pro 32K model on Volcengine Ark.",
        aliases=("Doubao-1.5-vision-pro-32k",),
    ),
    "doubao-1-5-pro-32k-250115": ModelInfo(
        name="doubao-1-5-pro-32k-250115",
        provider="doubao",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool"),
        description="Doubao 1.5 Pro 32K model on Volcengine Ark.",
        aliases=("Doubao-1.5-pro-32k",),
    ),
    "doubao-1-5-lite-32k-250115": ModelInfo(
        name="doubao-1-5-lite-32k-250115",
        provider="doubao",
        model_type="chat",
        capabilities=("text", "stream", "json"),
        description="Doubao 1.5 Lite 32K model on Volcengine Ark.",
        aliases=("Doubao-1.5-lite-32k",),
    ),
    "doubao-seedream-5.0-lite": ModelInfo(
        name="doubao-seedream-5.0-lite",
        provider="doubao",
        model_type="image_generation",
        capabilities=("text", "image", "image_generation", "image_edit"),
        description="Doubao Seedream 5.0 Lite image generation and image editing model.",
        aliases=("Doubao-Seedream-5.0-lite", "seedream-5-0-lite"),
    ),

    # Zhipu / GLM models
    "glm-5.1": ModelInfo(
        name="glm-5.1",
        provider="zhipu",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool", "reasoning"),
        description="ZhipuAI GLM 5.1 flagship model.",
    ),
    "glm-5": ModelInfo(
        name="glm-5",
        provider="zhipu",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool", "reasoning"),
        description="ZhipuAI GLM 5 base model.",
    ),
    "glm-5-turbo": ModelInfo(
        name="glm-5-turbo",
        provider="zhipu",
        model_type="chat",
        capabilities=("text", "stream", "json", "tool", "reasoning"),
        description="ZhipuAI GLM 5 Turbo model.",
    ),
    "glm-4.7": ModelInfo(
        name="glm-4.7",
        provider="zhipu",
        model_type="chat",
        capabilities=("text", "stream", "json", "reasoning", "tool"),
        description="ZhipuAI GLM 4.7 high-intelligence model.",
    ),
    "glm-4.7-flashx": ModelInfo(
        name="glm-4.7-flashx",
        provider="zhipu",
        model_type="chat",
        capabilities=("text", "stream", "json", "reasoning"),
        description="ZhipuAI GLM 4.7 FlashX model.",
    ),
    "glm-4.6": ModelInfo(
        name="glm-4.6",
        provider="zhipu",
        model_type="chat",
        capabilities=("text", "stream", "json", "reasoning", "tool"),
        description="ZhipuAI GLM 4.6 text model.",
    ),
    "glm-5v-turbo": ModelInfo(
        name="glm-5v-turbo",
        provider="zhipu",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "file", "stream", "json", "reasoning", "tool"),
        description="ZhipuAI GLM 5V Turbo vision model.",
        aliases=("GLM-5V-Turbo",),
    ),
    "glm-4.6v-flash": ModelInfo(
        name="glm-4.6v-flash",
        provider="zhipu",
        model_type="vision",
        capabilities=("text", "vision", "image", "video", "file", "stream", "json", "reasoning", "tool"),
        description="ZhipuAI GLM 4.6V Flash vision model.",
        aliases=("GLM-4.6V-Flash",),
    ),
    "glm-5.1-air": ModelInfo(
        name="glm-5.1-air",
        provider="zhipu",
        model_type="chat",
        capabilities=("text", "stream", "json"),
        description="ZhipuAI GLM 5.1 Air model.",
    ),
    "glm-4.6v": ModelInfo(
        name="glm-4.6v",
        provider="zhipu",
        model_type="vision",
        capabilities=("text", "vision", "image", "stream", "json"),
        description="ZhipuAI GLM vision model for image understanding.",
    ),
}


class ModelRegistry:
    """
    Registry that stores built-in and custom provider/model definitions.
    """

    def __init__(self, providers: Optional[Dict[str, ProviderInfo]] = None,
                 models: Optional[Dict[str, ModelInfo]] = None) -> None:
        """
        Initialize the registry with preset providers and models.
        """
        self.providers: Dict[str, ProviderInfo] = dict(providers or PRESET_PROVIDERS)
        self.models: Dict[str, ModelInfo] = dict(models or PRESET_MODELS)
        self._alias_map: Dict[str, str] = {}
        self._rebuild_alias_map()

    def _normalize_key(self, value: str) -> str:
        """
        Normalize names for case-insensitive lookup.
        """
        return value.strip().lower()

    def _rebuild_alias_map(self) -> None:
        """
        Build a lookup table for model names, API model IDs, and aliases.
        """
        self._alias_map = {}
        for key, info in self.models.items():
            candidates = [key, info.name, info.api_model] + list(info.aliases)
            for candidate in candidates:
                if candidate:
                    self._alias_map[self._normalize_key(candidate)] = key

    def get_provider(self, provider: str) -> ProviderInfo:
        """
        Return a provider by key.
        """
        key = self._normalize_key(provider)
        if key not in self.providers:
            raise KeyError(f"Unknown provider: {provider}")
        return self.providers[key]

    def add_provider(self, provider: ProviderInfo) -> None:
        """
        Add or replace a provider.
        """
        self.providers[self._normalize_key(provider.name)] = provider

    def list_providers(self) -> List[ProviderInfo]:
        """
        Return all registered providers.
        """
        return list(self.providers.values())

    def get_model(self, model: str) -> ModelInfo:
        """
        Return a model by name, API model ID, or alias.
        """
        key = self._alias_map.get(self._normalize_key(model))
        if not key:
            raise KeyError(f"Unknown model: {model}")
        return self.models[key]

    def add_model(self, model: ModelInfo) -> None:
        """
        Add or replace a model entry.
        """
        self.models[self._normalize_key(model.name)] = model
        self._rebuild_alias_map()

    def add_custom_model(self, provider: str, name: str, api_model: Optional[str] = None,
                         capabilities: Optional[Iterable[str]] = None,
                         model_type: str = "chat", description: str = "Custom model",
                         aliases: Optional[Iterable[str]] = None,
                         extra: Optional[Dict[str, Any]] = None) -> ModelInfo:
        """
        Add a custom model to the registry.
        """
        normalized_provider = self._normalize_key(provider)
        if normalized_provider not in self.providers:
            raise KeyError(f"Unknown provider: {provider}")
        info = ModelInfo(
            name=name,
            provider=normalized_provider,
            api_model=api_model or name,
            model_type=model_type,
            capabilities=tuple(capabilities or ("text", "stream", "json")),
            description=description,
            aliases=tuple(aliases or ()),
            extra=extra or {},
        )
        self.add_model(info)
        return info

    def remove_model(self, model: str) -> bool:
        """
        Remove a model from the registry.
        """
        key = self._alias_map.get(self._normalize_key(model))
        if key and key in self.models:
            del self.models[key]
            self._rebuild_alias_map()
            return True
        return False

    def list_models(self, provider: Optional[str] = None,
                    capability: Optional[str] = None,
                    model_type: Optional[str] = None) -> List[ModelInfo]:
        """
        List models with optional filters.
        """
        result: List[ModelInfo] = []
        provider_key = self._normalize_key(provider) if provider else None
        type_key = self._normalize_key(model_type) if model_type else None
        for info in self.models.values():
            if provider_key and self._normalize_key(info.provider) != provider_key:
                continue
            if capability and not info.supports(capability):
                continue
            if type_key and self._normalize_key(info.model_type) != type_key:
                continue
            result.append(info)
        return result

    def load_custom_models(self, models: Iterable[Dict[str, Any]]) -> None:
        """
        Load custom model definitions from a list of dictionaries.
        """
        for item in models:
            self.add_model(ModelInfo.from_dict(item))

    def export_custom_models(self, preset_names: Optional[Iterable[str]] = None) -> List[Dict[str, Any]]:
        """
        Export model entries that are not part of the preset registry.
        """
        preset_keys = set(preset_names or PRESET_MODELS.keys())
        output: List[Dict[str, Any]] = []
        for key, info in self.models.items():
            if key not in preset_keys:
                output.append(info.to_dict())
        return output

    def to_dict(self) -> Dict[str, Any]:
        """
        Export the registry to a dictionary.
        """
        return {
            "providers": {key: provider.to_dict() for key, provider in self.providers.items()},
            "models": {key: model.to_dict() for key, model in self.models.items()},
        }
