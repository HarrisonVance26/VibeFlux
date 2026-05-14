# VibeFlux, AGPL-3.0 license
# File: llms/QtBridge.py | Created: 2026-05-13
"""
PySide6 bridge for running LLM calls without blocking the UI thread.

LLMWorker is a QObject that can be moved to a QThread. LLMQtRunner is a convenience wrapper that creates and cleans up
threads automatically while forwarding text chunks and final responses as Qt signals.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from PySide6.QtCore import QObject, QThread, Signal, Slot

from .Client import LLMClient, LLMResponse


class LLMWorker(QObject):
    """
    Worker object for one LLM request.
    """

    started = Signal()
    chunkReady = Signal(str)
    responseReady = Signal(str)
    responseObjectReady = Signal(object)
    failed = Signal(str)
    finished = Signal()

    def __init__(self, client: LLMClient, request_kwargs: Optional[Dict[str, Any]] = None,
                 parent: Optional[QObject] = None) -> None:
        """
        Initialize the worker.
        """
        super().__init__(parent)
        self.client = client
        self.request_kwargs = request_kwargs or {}

    @Slot()
    def run(self) -> None:
        """
        Execute the request and emit Qt signals.
        """
        self.started.emit()
        try:
            stream = bool(self.request_kwargs.get("stream", False))
            result = self.client.chat(**self.request_kwargs)
            if stream:
                collected = []
                for chunk in result:  # type: ignore[union-attr]
                    collected.append(chunk)
                    self.chunkReady.emit(chunk)
                text = "".join(collected)
                self.responseReady.emit(text)
                self.responseObjectReady.emit(text)
            elif isinstance(result, LLMResponse):
                self.responseReady.emit(result.content)
                self.responseObjectReady.emit(result)
            else:
                text = "".join(list(result))  # type: ignore[arg-type]
                self.responseReady.emit(text)
                self.responseObjectReady.emit(text)
        except Exception as e:
            self.failed.emit(str(e))
        finally:
            self.finished.emit()


class LLMQtRunner(QObject):
    """
    Convenience QObject that starts LLM calls in a managed QThread.
    """

    started = Signal()
    chunkReady = Signal(str)
    responseReady = Signal(str)
    responseObjectReady = Signal(object)
    failed = Signal(str)
    finished = Signal()

    def __init__(self, client: Optional[LLMClient] = None, parent: Optional[QObject] = None) -> None:
        """
        Initialize the runner.
        """
        super().__init__(parent)
        self.client = client or LLMClient()
        self._thread: Optional[QThread] = None
        self._worker: Optional[LLMWorker] = None

    def configure(self, **kwargs: Any) -> None:
        """
        Forward configuration to the underlying LLMClient.
        """
        self.client.configure(**kwargs)

    @Slot(dict)
    def run_request(self, request_kwargs: Dict[str, Any]) -> None:
        """
        Run a chat request in a new QThread.
        """
        thread = QThread(self)
        worker = LLMWorker(self.client, request_kwargs)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.started.connect(self.started.emit)
        worker.chunkReady.connect(self.chunkReady.emit)
        worker.responseReady.connect(self.responseReady.emit)
        worker.responseObjectReady.connect(self.responseObjectReady.emit)
        worker.failed.connect(self.failed.emit)
        worker.finished.connect(self.finished.emit)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._clear_thread)

        self._thread = thread
        self._worker = worker
        thread.start()

    def ask(self, prompt: str, stream: bool = False, **kwargs: Any) -> None:
        """
        Run a prompt request in a new QThread.
        """
        request_kwargs = dict(kwargs)
        request_kwargs["prompt"] = prompt
        request_kwargs["stream"] = stream
        self.run_request(request_kwargs)

    @Slot()
    def _clear_thread(self) -> None:
        """
        Clear references after the thread finishes.
        """
        self._thread = None
        self._worker = None
