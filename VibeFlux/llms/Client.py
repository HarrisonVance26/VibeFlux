# VibeFlux, AGPL-3.0 license
# File: llms/Client.py | Created: 2026-05-13
"""
Unified client for OpenAI-compatible LLM providers.

The client is designed for desktop applications: users can save one provider API key, select a preset or custom model,
and then call text, image, or file-assisted chat through one interface. It uses Python's standard library HTTP stack to
avoid adding mandatory dependencies to VibeFlux.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, Iterable, Iterator, List, Optional, Sequence, Union

from .Config import APIKeyManager
from .Message import append_system_message, build_message, image_to_part, normalize_messages
from .Registry import ModelInfo, ModelRegistry, ProviderInfo
from .Templates import get_template


@dataclass
class LLMResponse:
    """
    Normalized LLM response object.

    Args:
        content (str): Assistant text content.
        provider (str): Provider key.
        model (str): Model ID used by the API.
        raw (Dict[str, Any]): Raw JSON response.
        reasoning_content (str): Optional reasoning text returned by compatible providers.
        reasoning_details (Dict[str, Any]): Optional structured reasoning metadata returned by compatible providers.
        usage (Dict[str, Any]): Token usage information if available.
        finish_reason (str): Finish reason from the first choice.
        tool_calls (List[Dict[str, Any]]): Tool call objects if present.
    """
    content: str
    provider: str
    model: str
    raw: Dict[str, Any] = field(default_factory=dict)
    reasoning_content: str = ""
    reasoning_details: Dict[str, Any] = field(default_factory=dict)
    usage: Dict[str, Any] = field(default_factory=dict)
    finish_reason: str = ""
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the response to a dictionary.
        """
        return {
            "content": self.content,
            "reasoning_content": self.reasoning_content,
            "reasoning_details": self.reasoning_details,
            "provider": self.provider,
            "model": self.model,
            "usage": self.usage,
            "finish_reason": self.finish_reason,
            "tool_calls": self.tool_calls,
            "raw": self.raw,
        }


class LLMAPIError(Exception):
    """
    Error raised when a provider API call fails.
    """


class LLMClient:
    """
    Unified LLM client for text, vision, file-assisted chat, streaming, and image generation.
    """

    def __init__(self,
                 provider: Optional[str] = None,
                 model: Optional[str] = None,
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 config_path: Optional[str] = None,
                 registry: Optional[ModelRegistry] = None,
                 timeout: Optional[int] = None,
                 max_retries: Optional[int] = None) -> None:
        """
        Initialize the client.
        """
        self.config = APIKeyManager(config_path=config_path, auto_create=True)
        self.registry = registry or ModelRegistry()
        self.config.load_custom_models_to_registry(self.registry)
        self.provider_name = (provider or self.config.get_active_provider()).strip().lower()
        self.model_name = model or self.config.get_active_model()
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = int(timeout if timeout is not None else self.config.get_runtime("timeout", 60))
        self.max_retries = int(max_retries if max_retries is not None else self.config.get_runtime("max_retries", 2))
        self.history: List[Dict[str, Any]] = []

    def configure(self,
                  provider: Optional[str] = None,
                  model: Optional[str] = None,
                  api_key: Optional[str] = None,
                  base_url: Optional[str] = None,
                  save: bool = True) -> None:
        """
        Update active provider, model, API key, or base URL.
        """
        if provider:
            self.provider_name = provider.strip().lower()
        if model:
            self.model_name = model
        if api_key is not None:
            self.api_key = api_key
            self.config.set_api_key(self.provider_name, api_key, save=save)
        if base_url is not None:
            self.base_url = base_url
            self.config.set_base_url(self.provider_name, base_url, save=save)
        if save:
            self.config.set_active(self.provider_name, self.model_name, save=True)

    def set_api_key(self, api_key: str, provider: Optional[str] = None, save: bool = True) -> None:
        """
        Set an API key for the current or given provider.
        """
        target = (provider or self.provider_name).strip().lower()
        self.config.set_api_key(target, api_key, save=save)
        if target == self.provider_name:
            self.api_key = api_key

    def add_custom_model(self, provider: str, name: str, api_model: Optional[str] = None,
                         capabilities: Optional[Iterable[str]] = None,
                         model_type: str = "chat", description: str = "Custom model",
                         save: bool = True) -> ModelInfo:
        """
        Add a custom model to both runtime registry and api_keys.json.
        """
        info = self.registry.add_custom_model(
            provider=provider,
            name=name,
            api_model=api_model,
            capabilities=capabilities,
            model_type=model_type,
            description=description,
        )
        self.config.add_custom_model(
            provider=provider,
            name=name,
            api_model=api_model,
            capabilities=capabilities,
            model_type=model_type,
            description=description,
            save=save,
        )
        return info

    def list_models(self, provider: Optional[str] = None,
                    capability: Optional[str] = None,
                    model_type: Optional[str] = None) -> List[ModelInfo]:
        """
        List registered models with optional filters.
        """
        return self.registry.list_models(provider=provider, capability=capability, model_type=model_type)

    def list_providers(self) -> List[ProviderInfo]:
        """
        List registered providers.
        """
        return self.registry.list_providers()

    def refresh_models(self,
                       provider: Optional[str] = None,
                       api_key: Optional[str] = None,
                       base_url: Optional[str] = None,
                       endpoint: str = "/models",
                       save: bool = True,
                       overwrite: bool = False) -> "ModelPresetUpdateResult":
        """
        Refresh provider model entries through the OpenAI-compatible model list API.
        """
        from .Updater import ModelPresetUpdater

        updater = ModelPresetUpdater(
            config_path=self.config.config_path,
            registry=self.registry,
            timeout=self.timeout,
        )
        return updater.refresh_provider(
            provider=provider or self.provider_name,
            api_key=api_key if api_key is not None else self.api_key,
            base_url=base_url if base_url is not None else self.base_url,
            endpoint=endpoint,
            save=save,
            overwrite=overwrite,
        )

    def resolve_model(self, model: Optional[str] = None, provider: Optional[str] = None) -> ModelInfo:
        """
        Resolve a model. Unknown model names are treated as custom names under the selected provider.
        """
        model_name = model or self.model_name
        try:
            info = self.registry.get_model(model_name)
        except KeyError:
            provider_name = (provider or self.provider_name).strip().lower()
            info = ModelInfo(
                name=model_name,
                provider=provider_name,
                api_model=model_name,
                model_type="chat",
                capabilities=("text", "stream", "json"),
                description="Runtime custom model",
            )
            self.registry.add_model(info)
        return info

    def resolve_provider(self, provider: Optional[str] = None, model_info: Optional[ModelInfo] = None) -> ProviderInfo:
        """
        Resolve a provider using explicit provider, model provider, or active provider.
        """
        provider_name = (provider or (model_info.provider if model_info else self.provider_name)).strip().lower()
        return self.registry.get_provider(provider_name)

    def _effective_api_key(self, provider_name: str) -> str:
        """
        Resolve the API key from explicit value, api_keys.json, or environment variable.
        """
        if self.api_key:
            return self.api_key
        return self.config.get_api_key(provider_name)

    def _effective_base_url(self, provider_name: str, provider_info: ProviderInfo) -> str:
        """
        Resolve the API base URL from explicit value, api_keys.json, or provider presets.
        """
        if self.base_url:
            return self.base_url
        return self.config.get_base_url(provider_name) or provider_info.base_url

    def _build_url(self, base_url: str, endpoint: str) -> str:
        """
        Join a provider base URL and endpoint.
        """
        if not base_url:
            raise ValueError("base_url is empty. Please configure provider base_url in api_keys.json.")
        return base_url.rstrip("/") + "/" + endpoint.lstrip("/")

    def _request_json(self, provider_info: ProviderInfo, payload: Dict[str, Any],
                      endpoint: Optional[str] = None, stream: bool = False) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        """
        Send an HTTP POST request and return parsed JSON or a streaming iterator.
        """
        provider_name = provider_info.name
        api_key = self._effective_api_key(provider_name)
        if not api_key:
            raise ValueError(
                "API key is empty for provider '{provider}'. Set it in api_keys.json or environment variable.".format(
                    provider=provider_name
                )
            )
        base_url = self._effective_base_url(provider_name, provider_info)
        url = self._build_url(base_url, endpoint or provider_info.chat_endpoint)
        clean_payload = _remove_none(payload)
        data = json.dumps(clean_payload, ensure_ascii=False).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + api_key,
        }
        request = urllib.request.Request(url=url, data=data, headers=headers, method="POST")

        if stream:
            return self._stream_request(request)

        return self._json_request_with_retry(request)

    def _json_request_with_retry(self, request: urllib.request.Request) -> Dict[str, Any]:
        """
        Send a non-streaming HTTP request with retries.
        """
        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    body = response.read().decode("utf-8")
                    return json.loads(body) if body else {}
            except urllib.error.HTTPError as e:
                message = _read_http_error(e)
                raise LLMAPIError(message) from e
            except Exception as e:
                last_error = e
                if attempt >= self.max_retries:
                    break
                time.sleep(min(2 ** attempt, 8))
        raise LLMAPIError("LLM API request failed: {error}".format(error=str(last_error)))

    def _stream_request(self, request: urllib.request.Request) -> Iterator[Dict[str, Any]]:
        """
        Stream an SSE-style response as JSON chunks.
        """
        try:
            response = urllib.request.urlopen(request, timeout=self.timeout)
        except urllib.error.HTTPError as e:
            message = _read_http_error(e)
            raise LLMAPIError(message) from e
        except Exception as e:
            raise LLMAPIError("LLM API stream request failed: {error}".format(error=str(e))) from e

        def _iterator() -> Iterator[Dict[str, Any]]:
            with response:
                for raw_line in response:
                    line = raw_line.decode("utf-8", errors="ignore").strip()
                    if not line:
                        continue
                    if line.startswith("data:"):
                        line = line[5:].strip()
                    if not line or line == "[DONE]":
                        if line == "[DONE]":
                            break
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue
        return _iterator()

    def chat(self,
             messages: Optional[Union[str, Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
             prompt: Optional[str] = None,
             system: Optional[str] = None,
             template: Optional[str] = None,
             extra_context: Optional[str] = None,
             images: Optional[Union[str, Sequence[str]]] = None,
             image_urls: Optional[Union[str, Sequence[str]]] = None,
             files: Optional[Union[str, Sequence[str]]] = None,
             provider: Optional[str] = None,
             model: Optional[str] = None,
             stream: bool = False,
             temperature: Optional[float] = None,
             max_tokens: Optional[int] = None,
             response_format: Optional[Union[str, Dict[str, Any]]] = None,
             thinking: Optional[Union[bool, str, Dict[str, Any]]] = None,
             return_reasoning: bool = True,
             reasoning_effort: Optional[str] = None,
             binary_files_as_base64: bool = False,
             extra_body: Optional[Dict[str, Any]] = None,
             **kwargs: Any) -> Union[LLMResponse, Iterator[str]]:
        """
        Call a chat completion model.
        """
        model_info = self.resolve_model(model=model, provider=provider)
        provider_info = self.resolve_provider(provider=provider, model_info=model_info)
        provider_name = provider_info.name
        task_template = get_template(template) if template else None

        system_prompt = system
        if task_template and not system_prompt:
            system_prompt = task_template.system_prompt

        message_list = normalize_messages(messages)
        if prompt is not None or images is not None or image_urls is not None or files is not None:
            user_prompt = prompt or ""
            if task_template:
                user_prompt = task_template.render_user_prompt(user_input=user_prompt, extra_context=extra_context)
            message_list.append(build_message(
                role="user",
                text=user_prompt,
                images=images,
                image_urls=image_urls,
                files=files,
                max_file_chars=int(self.config.get_runtime("max_file_chars", 20000)),
                binary_files_as_base64=binary_files_as_base64,
            ))
        elif task_template:
            message_list.append({"role": "user", "content": task_template.render_user_prompt(extra_context=extra_context)})

        message_list = append_system_message(message_list, system_prompt)
        message_list = _strip_reasoning_from_messages(message_list)

        payload: Dict[str, Any] = {
            "model": model_info.api_model,
            "messages": message_list,
            "stream": stream,
            "temperature": temperature if temperature is not None else self.config.get_runtime("temperature", 0.2),
            "max_tokens": max_tokens,
        }
        if response_format:
            payload["response_format"] = _normalize_response_format(response_format)
        _apply_thinking_options(
            payload=payload,
            provider=provider_name,
            model_info=model_info,
            thinking=thinking,
            reasoning_effort=reasoning_effort,
        )
        if extra_body:
            payload.update(extra_body)
        payload.update(kwargs)

        if stream:
            chunks = self._request_json(provider_info, payload, endpoint=provider_info.chat_endpoint, stream=True)
            return _stream_content(chunks, include_reasoning=return_reasoning)  # type: ignore[arg-type]

        raw = self._request_json(provider_info, payload, endpoint=provider_info.chat_endpoint, stream=False)
        return _parse_response(
            raw,
            provider=provider_name,
            model=model_info.api_model,
            return_reasoning=return_reasoning,
        )  # type: ignore[arg-type]

    def single_chat(self, prompt: str, **kwargs: Any) -> Union[LLMResponse, Iterator[str]]:
        """
        Convenience method for a single-turn chat call.
        """
        return self.chat(prompt=prompt, **kwargs)

    def reset_history(self, system: Optional[str] = None) -> None:
        """
        Clear conversation history and optionally keep a system prompt.
        """
        self.history = []
        if system:
            self.history.append({"role": "system", "content": system})

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Return a copy of the current conversation history.
        """
        return list(self.history)

    def set_history(self, messages: Sequence[Dict[str, Any]]) -> None:
        """
        Replace the current conversation history.
        """
        self.history = list(messages)

    def send(self,
             prompt: str,
             images: Optional[Union[str, Sequence[str]]] = None,
             image_urls: Optional[Union[str, Sequence[str]]] = None,
             files: Optional[Union[str, Sequence[str]]] = None,
             keep_history: bool = True,
             stream: bool = False,
             **kwargs: Any) -> Union[LLMResponse, Iterator[str]]:
        """
        Send one user turn in a multi-round conversation.
        """
        user_message = build_message(
            role="user",
            text=prompt,
            images=images,
            image_urls=image_urls,
            files=files,
            max_file_chars=int(self.config.get_runtime("max_file_chars", 20000)),
        )
        messages = self.history + [user_message]
        if stream:
            stream_result = self.chat(messages=messages, stream=True, **kwargs)

            def _collector() -> Iterator[str]:
                collected: List[str] = []
                for chunk in stream_result:  # type: ignore[union-attr]
                    collected.append(chunk)
                    yield chunk
                if keep_history:
                    self.history.append(user_message)
                    self.history.append({"role": "assistant", "content": "".join(collected)})
            return _collector()

        response = self.chat(messages=messages, stream=False, **kwargs)
        if keep_history and isinstance(response, LLMResponse):
            self.history.append(user_message)
            self.history.append({"role": "assistant", "content": response.content})
        return response

    def ask_image(self, image: Union[str, Sequence[str]], prompt: str = "Please analyze this image.",
                  task: str = "image_understanding", **kwargs: Any) -> Union[LLMResponse, Iterator[str]]:
        """
        Analyze one or more images with a vision-capable model.
        """
        return self.chat(prompt=prompt, images=image, template=task, **kwargs)

    def analyze_file(self, file_path: Union[str, Sequence[str]], prompt: str = "Please analyze this file.",
                     task: str = "file_summary", **kwargs: Any) -> Union[LLMResponse, Iterator[str]]:
        """
        Analyze one or more files by inserting extracted text into the message.
        """
        return self.chat(prompt=prompt, files=file_path, template=task, **kwargs)

    def generate_image(self,
                       prompt: str,
                       images: Optional[Union[str, Sequence[str]]] = None,
                       image_urls: Optional[Union[str, Sequence[str]]] = None,
                       provider: Optional[str] = None,
                       model: Optional[str] = None,
                       size: Optional[str] = None,
                       n: int = 1,
                       extra_body: Optional[Dict[str, Any]] = None,
                       **kwargs: Any) -> Dict[str, Any]:
        """
        Call an OpenAI-compatible image generation endpoint.
        """
        model_info = self.resolve_model(model=model or self.model_name, provider=provider)
        provider_info = self.resolve_provider(provider=provider, model_info=model_info)
        body: Dict[str, Any] = {
            "model": model_info.api_model,
            "prompt": prompt,
            "n": n,
            "size": size,
        }
        reference_urls: List[str] = []
        for image in _as_list(images):
            reference_urls.append(image_to_part(image)["image_url"]["url"])
        for url in _as_list(image_urls):
            reference_urls.append(url)
        if reference_urls:
            body["image_urls"] = reference_urls
        if extra_body:
            body.update(extra_body)
        body.update(kwargs)
        raw = self._request_json(provider_info, body, endpoint=provider_info.image_endpoint, stream=False)
        return raw  # type: ignore[return-value]


def _as_list(value: Optional[Union[str, Sequence[str]]]) -> List[str]:
    """
    Normalize a string or sequence into a list.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def _remove_none(value: Any) -> Any:
    """
    Remove None values recursively from a JSON payload.
    """
    if isinstance(value, dict):
        return {key: _remove_none(item) for key, item in value.items() if item is not None}
    if isinstance(value, list):
        return [_remove_none(item) for item in value]
    return value


def _read_http_error(error: urllib.error.HTTPError) -> str:
    """
    Read and format an HTTP error body.
    """
    try:
        body = error.read().decode("utf-8", errors="ignore")
    except Exception:
        body = ""
    return "HTTP {code} {reason}: {body}".format(code=error.code, reason=error.reason, body=body)


def _normalize_response_format(response_format: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Normalize response_format into an OpenAI-compatible dictionary.
    """
    if isinstance(response_format, dict):
        return response_format
    value = response_format.strip().lower()
    if value in ("json", "json_object"):
        return {"type": "json_object"}
    if value in ("text", "plain_text"):
        return {"type": "text"}
    return {"type": value}


def _normalize_thinking_mode(thinking: Optional[Union[bool, str, Dict[str, Any]]]) -> Optional[str]:
    """
    Normalize a thinking option into enabled, disabled, auto, or None.
    """
    if thinking is None:
        return None
    if isinstance(thinking, bool):
        return "enabled" if thinking else "disabled"
    if isinstance(thinking, dict):
        value = thinking.get("type") or thinking.get("mode") or thinking.get("thinking_type")
        return str(value).strip().lower() if value else None
    value = str(thinking).strip().lower()
    if value in ("none", "default", "model_default", "off"):
        return None
    if value in ("true", "on", "yes", "enable", "enabled"):
        return "enabled"
    if value in ("false", "no", "disable", "disabled"):
        return "disabled"
    if value in ("auto", "automatic"):
        return "auto"
    return value


def _apply_thinking_options(payload: Dict[str, Any],
                            provider: str,
                            model_info: ModelInfo,
                            thinking: Optional[Union[bool, str, Dict[str, Any]]] = None,
                            reasoning_effort: Optional[str] = None) -> None:
    """
    Apply provider-compatible thinking controls to a chat payload.
    """
    mode = _normalize_thinking_mode(thinking)
    if isinstance(thinking, dict):
        if "enable_thinking" in thinking:
            payload["enable_thinking"] = thinking["enable_thinking"]
        if "thinking" in thinking and isinstance(thinking["thinking"], dict):
            payload["thinking"] = thinking["thinking"]

    if reasoning_effort:
        payload["reasoning_effort"] = reasoning_effort

    if not mode:
        return

    provider_key = provider.strip().lower()
    supports_reasoning = model_info.supports("reasoning")
    if provider_key == "qwen":
        if mode in ("enabled", "disabled"):
            payload["enable_thinking"] = mode == "enabled"
        return

    if provider_key in ("doubao", "zhipu", "custom") or supports_reasoning:
        payload["thinking"] = {"type": mode}


def _strip_reasoning_from_messages(messages: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove reasoning fields from outgoing messages because several providers reject them in input.
    """
    output: List[Dict[str, Any]] = []
    for message in messages:
        clean = dict(message)
        for key in ("reasoning_content", "reasoning", "reasoning_details", "thinking"):
            clean.pop(key, None)
        output.append(clean)
    return output


def _parse_response(raw: Dict[str, Any], provider: str, model: str, return_reasoning: bool = True) -> LLMResponse:
    """
    Parse a chat completion response into LLMResponse.
    """
    choices = raw.get("choices") or []
    first = choices[0] if choices else {}
    message = first.get("message") or {}
    content = _content_to_text(message.get("content", ""))
    reasoning_details = _extract_reasoning_details(raw, message)
    reasoning = _extract_reasoning_text(raw, message) if return_reasoning else ""
    tool_calls = message.get("tool_calls") or []
    return LLMResponse(
        content=content,
        reasoning_content=reasoning,
        reasoning_details=reasoning_details,
        provider=provider,
        model=raw.get("model", model),
        raw=raw,
        usage=raw.get("usage") or {},
        finish_reason=first.get("finish_reason", ""),
        tool_calls=tool_calls,
    )


def _extract_reasoning_text(raw: Dict[str, Any], message: Dict[str, Any]) -> str:
    """
    Extract reasoning text from common provider response fields.
    """
    fields = (
        message.get("reasoning_content"),
        message.get("reasoning"),
        message.get("thinking"),
        message.get("thoughts"),
        raw.get("reasoning_content"),
        raw.get("thinking"),
    )
    for field in fields:
        text = _content_to_text(field)
        if text:
            return text
    content = message.get("content")
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            item_type = str(item.get("type", "")).lower()
            if item_type in ("reasoning", "thinking", "reasoning_content"):
                parts.append(_content_to_text(item.get("text") or item.get("content") or item.get("reasoning")))
        return "".join(parts)
    return ""


def _extract_reasoning_details(raw: Dict[str, Any], message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract structured reasoning metadata when a provider returns it.
    """
    details: Dict[str, Any] = {}
    for key in ("reasoning_details", "reasoning", "thinking"):
        value = message.get(key)
        if isinstance(value, dict):
            details[key] = value
    usage = raw.get("usage") or {}
    if isinstance(usage, dict):
        for key in ("reasoning_tokens", "reasoning_content_tokens", "completion_tokens_details"):
            if key in usage:
                details[key] = usage[key]
    return details


def _content_to_text(content: Any) -> str:
    """
    Convert provider-specific content values into text.
    """
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        for key in ("text", "content", "reasoning_content", "reasoning", "thinking"):
            if key in content:
                return _content_to_text(content.get(key))
        return ""
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                if "text" in item:
                    parts.append(str(item.get("text") or ""))
                elif "content" in item:
                    parts.append(str(item.get("content") or ""))
                elif "reasoning_content" in item:
                    parts.append(str(item.get("reasoning_content") or ""))
            else:
                parts.append(str(item))
        return "".join(parts)
    return str(content)


def _stream_content(chunks: Iterator[Dict[str, Any]], include_reasoning: bool = True) -> Iterator[str]:
    """
    Convert streaming JSON chunks into text chunks.
    """
    for chunk in chunks:
        choices = chunk.get("choices") or []
        if not choices:
            continue
        delta = choices[0].get("delta") or choices[0].get("message") or {}
        text = delta.get("content")
        if text is None and include_reasoning:
            text = delta.get("reasoning_content")
        if text is None and include_reasoning:
            text = delta.get("reasoning") or delta.get("thinking")
        if isinstance(text, list):
            text = _content_to_text(text)
        if text:
            yield str(text)
