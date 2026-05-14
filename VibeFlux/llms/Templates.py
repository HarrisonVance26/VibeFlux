# VibeFlux, AGPL-3.0 license
# File: llms/Templates.py | Created: 2026-05-13
"""
Preset output templates for detection, segmentation, understanding, and organization tasks.

Templates use strict JSON-style instructions so downstream PySide6 widgets can parse model outputs and render tables,
labels, masks, reports, or review panels more easily.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class OutputTemplate:
    """
    Standard task template for LLM output formatting.

    Args:
        name (str): Template key.
        title (str): Human-readable template title.
        system_prompt (str): System instruction for the model.
        user_prefix (str): Prefix appended before user input.
        response_schema (Dict[str, Any]): JSON-style schema shown to the model.
        description (str): Short template description.
    """
    name: str
    title: str
    system_prompt: str
    user_prefix: str
    response_schema: Dict[str, Any]
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the template to a dictionary.
        """
        return asdict(self)

    def render_user_prompt(self, user_input: Optional[str] = None,
                           extra_context: Optional[str] = None) -> str:
        """
        Render a user prompt with the schema and optional context.
        """
        lines: List[str] = [self.user_prefix.strip()]
        if user_input:
            lines.append("\nUser input:\n" + user_input.strip())
        if extra_context:
            lines.append("\nExtra context:\n" + extra_context.strip())
        lines.append("\nRequired JSON schema:\n" + _json_schema_text(self.response_schema))
        lines.append("\nReturn only valid JSON. Do not wrap it in Markdown code fences.")
        return "\n".join(lines)


def _json_schema_text(schema: Dict[str, Any]) -> str:
    """
    Convert a schema dictionary to a compact readable JSON-like string.
    """
    import json
    return json.dumps(schema, ensure_ascii=False, indent=2)


COMMON_SYSTEM_PROMPT = (
    "You are a precise multimodal analysis assistant. "
    "Follow the requested task and return structured JSON only. "
    "When a value is uncertain, use null or an empty list instead of inventing details. "
    "Coordinates should be normalized to the range [0, 1] unless the user explicitly asks for pixel coordinates."
)


PRESET_TASK_TEMPLATES: Dict[str, OutputTemplate] = {
    "image_detection": OutputTemplate(
        name="image_detection",
        title="Image Object Detection",
        description="Detect objects, text regions, defects, or targets in an image.",
        system_prompt=COMMON_SYSTEM_PROMPT,
        user_prefix="Analyze the image and detect visible targets. Use normalized bounding boxes.",
        response_schema={
            "task": "image_detection",
            "image_summary": "string",
            "detections": [
                {
                    "label": "string",
                    "category": "string|null",
                    "confidence": "number|null",
                    "bbox": {
                        "x_min": "number",
                        "y_min": "number",
                        "x_max": "number",
                        "y_max": "number"
                    },
                    "attributes": ["string"],
                    "evidence": "string"
                }
            ],
            "warnings": ["string"]
        },
    ),
    "image_segmentation": OutputTemplate(
        name="image_segmentation",
        title="Image Segmentation Description",
        description="Describe instance or semantic segmentation regions in a format that can be post-processed.",
        system_prompt=COMMON_SYSTEM_PROMPT,
        user_prefix=(
            "Analyze the image and describe segmentation targets. If exact masks cannot be produced, return "
            "polygon-like approximate regions and a clear natural-language mask description."
        ),
        response_schema={
            "task": "image_segmentation",
            "image_summary": "string",
            "segments": [
                {
                    "label": "string",
                    "segment_type": "semantic|instance|region",
                    "confidence": "number|null",
                    "bbox": {
                        "x_min": "number",
                        "y_min": "number",
                        "x_max": "number",
                        "y_max": "number"
                    },
                    "polygon": [["number", "number"]],
                    "mask_description": "string",
                    "attributes": ["string"]
                }
            ],
            "warnings": ["string"]
        },
    ),
    "image_understanding": OutputTemplate(
        name="image_understanding",
        title="Image Understanding",
        description="Understand scene content, OCR text, relationships, risks, and useful conclusions.",
        system_prompt=COMMON_SYSTEM_PROMPT,
        user_prefix="Understand the image comprehensively and organize the result for a desktop CV application.",
        response_schema={
            "task": "image_understanding",
            "scene_summary": "string",
            "main_objects": [
                {
                    "name": "string",
                    "location": "string",
                    "attributes": ["string"]
                }
            ],
            "relationships": ["string"],
            "ocr_text": ["string"],
            "quality_notes": ["string"],
            "risks_or_abnormalities": ["string"],
            "recommended_next_steps": ["string"]
        },
    ),
    "text_detection": OutputTemplate(
        name="text_detection",
        title="Text Information Detection",
        description="Extract entities, events, numbers, claims, and abnormalities from text.",
        system_prompt=COMMON_SYSTEM_PROMPT,
        user_prefix="Detect key information from the text and keep the output easy to render as tables.",
        response_schema={
            "task": "text_detection",
            "summary": "string",
            "entities": [
                {
                    "name": "string",
                    "type": "person|organization|location|product|date|number|other",
                    "value": "string",
                    "evidence": "string"
                }
            ],
            "events": [
                {
                    "event": "string",
                    "time": "string|null",
                    "participants": ["string"],
                    "evidence": "string"
                }
            ],
            "issues_or_risks": ["string"],
            "action_items": ["string"]
        },
    ),
    "text_organization": OutputTemplate(
        name="text_organization",
        title="Text Organization",
        description="Rewrite messy text into a structured report or note.",
        system_prompt=COMMON_SYSTEM_PROMPT,
        user_prefix="Organize the supplied text into a clean, structured result.",
        response_schema={
            "task": "text_organization",
            "title": "string",
            "abstract": "string",
            "sections": [
                {
                    "heading": "string",
                    "bullets": ["string"]
                }
            ],
            "key_terms": ["string"],
            "todo_list": [
                {
                    "item": "string",
                    "priority": "high|medium|low|null"
                }
            ]
        },
    ),
    "file_summary": OutputTemplate(
        name="file_summary",
        title="File Understanding",
        description="Summarize an attached text or extracted document file.",
        system_prompt=COMMON_SYSTEM_PROMPT,
        user_prefix="Understand the attached file content and produce a concise structured summary.",
        response_schema={
            "task": "file_summary",
            "file_type": "string|null",
            "summary": "string",
            "key_points": ["string"],
            "tables_or_fields": [
                {
                    "name": "string",
                    "value": "string",
                    "note": "string|null"
                }
            ],
            "potential_errors": ["string"],
            "suggested_actions": ["string"]
        },
    ),
    "structured_report": OutputTemplate(
        name="structured_report",
        title="Structured Report",
        description="General-purpose structured analysis report for text, image, or file inputs.",
        system_prompt=COMMON_SYSTEM_PROMPT,
        user_prefix="Create a structured analysis report from the current input.",
        response_schema={
            "task": "structured_report",
            "title": "string",
            "executive_summary": "string",
            "observations": [
                {
                    "item": "string",
                    "confidence": "number|null",
                    "evidence": "string|null"
                }
            ],
            "conclusions": ["string"],
            "next_steps": ["string"],
            "raw_notes": ["string"]
        },
    ),
}


def get_template(name: str) -> OutputTemplate:
    """
    Return a preset task template by name.
    """
    key = name.strip().lower()
    if key not in PRESET_TASK_TEMPLATES:
        raise KeyError(f"Unknown LLM output template: {name}")
    return PRESET_TASK_TEMPLATES[key]


def list_templates() -> List[OutputTemplate]:
    """
    Return all preset templates.
    """
    return list(PRESET_TASK_TEMPLATES.values())


def template_names() -> List[str]:
    """
    Return all preset template names.
    """
    return list(PRESET_TASK_TEMPLATES.keys())


def render_template_prompt(name: str, user_input: Optional[str] = None,
                           extra_context: Optional[str] = None) -> str:
    """
    Render the user prompt of a preset template.
    """
    return get_template(name).render_user_prompt(user_input=user_input, extra_context=extra_context)
