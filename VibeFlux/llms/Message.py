# VibeFlux, AGPL-3.0 license
# File: llms/Message.py | Created: 2026-05-13
"""
Message builders for text, image, and file inputs.

These helpers convert user-provided paths or URLs into OpenAI-compatible message parts. They are intentionally small
and dependency-light, so they can be used from PySide6 slots without pulling in heavy document-processing packages.
"""
from __future__ import annotations

import base64
import mimetypes
import os
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union


MessageContent = Union[str, List[Dict[str, Any]]]
Message = Dict[str, MessageContent]

TEXT_EXTENSIONS = {
    ".txt", ".md", ".markdown", ".json", ".jsonl", ".csv", ".tsv", ".yaml", ".yml", ".xml", ".html",
    ".htm", ".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".hpp", ".cs", ".go", ".rs",
    ".php", ".rb", ".swift", ".kt", ".sql", ".log", ".ini", ".cfg", ".toml", ".qss", ".ui",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}


def _as_list(value: Optional[Union[str, Sequence[str]]]) -> List[str]:
    """
    Normalize a string or sequence into a list.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def guess_mime_type(path_or_url: str, default: str = "application/octet-stream") -> str:
    """
    Guess the MIME type of a local file path or URL.
    """
    mime_type, _ = mimetypes.guess_type(path_or_url)
    return mime_type or default


def is_image_file(path_or_url: str) -> bool:
    """
    Check whether a file path or URL looks like an image.
    """
    ext = os.path.splitext(path_or_url.split("?")[0])[1].lower()
    if ext in IMAGE_EXTENSIONS:
        return True
    return guess_mime_type(path_or_url).startswith("image/")


def file_to_base64(path: str) -> str:
    """
    Read a local file and return its base64 string.
    """
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def file_to_data_url(path: str, mime_type: Optional[str] = None) -> str:
    """
    Convert a local file to a data URL.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    mime = mime_type or guess_mime_type(path)
    return "data:{mime};base64,{data}".format(mime=mime, data=file_to_base64(path))


def image_to_part(path_or_url: str) -> Dict[str, Any]:
    """
    Convert a local image path or remote image URL to an OpenAI-compatible image_url part.
    """
    if path_or_url.startswith(("http://", "https://", "data:")):
        url = path_or_url
    else:
        url = file_to_data_url(path_or_url, guess_mime_type(path_or_url, "image/jpeg"))
    return {"type": "image_url", "image_url": {"url": url}}


def read_text_file(path: str, max_chars: int = 20000, encodings: Optional[Iterable[str]] = None) -> str:
    """
    Read a text file with several common encodings.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    encoding_candidates = list(encodings or ("utf-8", "utf-8-sig", "gb18030", "gbk", "latin-1"))
    last_error: Optional[Exception] = None
    for encoding in encoding_candidates:
        try:
            with open(path, "r", encoding=encoding) as file:
                content = file.read(max_chars + 1)
            if len(content) > max_chars:
                return content[:max_chars] + "\n...[truncated]"
            return content
        except UnicodeDecodeError as e:
            last_error = e
    raise UnicodeDecodeError("unknown", b"", 0, 1, f"Unable to decode text file {path}: {last_error}")


def read_pdf_text(path: str, max_chars: int = 20000) -> str:
    """
    Extract text from a PDF file if pypdf is installed.
    """
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as e:
        raise ImportError("PDF text extraction requires optional package pypdf.") from e

    reader = PdfReader(path)
    chunks: List[str] = []
    total = 0
    for page_index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if not text:
            continue
        page_text = "\n--- Page {page} ---\n{content}".format(page=page_index + 1, content=text)
        chunks.append(page_text)
        total += len(page_text)
        if total >= max_chars:
            break
    content = "".join(chunks)
    if len(content) > max_chars:
        content = content[:max_chars] + "\n...[truncated]"
    return content


def file_to_text_part(path: str, max_chars: int = 20000,
                      binary_files_as_base64: bool = False,
                      max_binary_bytes: int = 1024 * 256) -> Dict[str, str]:
    """
    Convert a local file into a text message part.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    filename = os.path.basename(path)
    if ext == ".pdf":
        try:
            content = read_pdf_text(path, max_chars=max_chars)
        except Exception as e:
            content = "PDF text extraction failed: {error}".format(error=str(e))
    elif ext in TEXT_EXTENSIONS or guess_mime_type(path, "").startswith("text/"):
        content = read_text_file(path, max_chars=max_chars)
    elif binary_files_as_base64:
        size = os.path.getsize(path)
        if size > max_binary_bytes:
            content = "Binary file is too large to embed. Size: {size} bytes.".format(size=size)
        else:
            content = file_to_data_url(path)
    else:
        content = "Binary file is attached by path only. Enable binary_files_as_base64 to embed it."

    text = "### Attached file: {filename}\n```{ext}\n{content}\n```".format(
        filename=filename,
        ext=ext.lstrip(".") or "text",
        content=content,
    )
    return {"type": "text", "text": text}


def build_user_content(text: Optional[str] = None,
                       images: Optional[Union[str, Sequence[str]]] = None,
                       image_urls: Optional[Union[str, Sequence[str]]] = None,
                       files: Optional[Union[str, Sequence[str]]] = None,
                       max_file_chars: int = 20000,
                       binary_files_as_base64: bool = False) -> MessageContent:
    """
    Build a user message content value from text, images, URLs, and files.
    """
    image_list = _as_list(images)
    image_url_list = _as_list(image_urls)
    file_list = _as_list(files)
    has_media = bool(image_list or image_url_list or file_list)

    if not has_media:
        return text or ""

    parts: List[Dict[str, Any]] = []
    if text:
        parts.append({"type": "text", "text": text})

    for file_path in file_list:
        if is_image_file(file_path):
            parts.append(image_to_part(file_path))
        else:
            parts.append(file_to_text_part(
                file_path,
                max_chars=max_file_chars,
                binary_files_as_base64=binary_files_as_base64,
            ))

    for image_path in image_list:
        parts.append(image_to_part(image_path))

    for url in image_url_list:
        parts.append(image_to_part(url))

    return parts


def build_message(role: str,
                  text: Optional[str] = None,
                  images: Optional[Union[str, Sequence[str]]] = None,
                  image_urls: Optional[Union[str, Sequence[str]]] = None,
                  files: Optional[Union[str, Sequence[str]]] = None,
                  max_file_chars: int = 20000,
                  binary_files_as_base64: bool = False) -> Dict[str, Any]:
    """
    Build one OpenAI-compatible message dictionary.
    """
    return {
        "role": role,
        "content": build_user_content(
            text=text,
            images=images,
            image_urls=image_urls,
            files=files,
            max_file_chars=max_file_chars,
            binary_files_as_base64=binary_files_as_base64,
        ),
    }


def normalize_messages(messages: Optional[Union[str, Dict[str, Any], Sequence[Dict[str, Any]]]]) -> List[Dict[str, Any]]:
    """
    Normalize strings, dictionaries, or message lists into a message list.
    """
    if messages is None:
        return []
    if isinstance(messages, str):
        return [{"role": "user", "content": messages}]
    if isinstance(messages, dict):
        return [messages]
    return list(messages)


def append_system_message(messages: List[Dict[str, Any]], system: Optional[str]) -> List[Dict[str, Any]]:
    """
    Prepend a system message if one is provided.
    """
    if not system:
        return messages
    if messages and messages[0].get("role") == "system":
        messages[0]["content"] = system
        return messages
    return [{"role": "system", "content": system}] + messages
