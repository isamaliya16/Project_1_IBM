"""
GuardrailEngine — AI Ethics & Safety Layer
Agentic AI SDLC Phase: Safety & Guardrails
Implements: Input validation, harmful content detection, output sanitization
"""

import re
import logging

logger = logging.getLogger(__name__)

# ── Harmful/dangerous query patterns ──────────────────────────────────────
HARMFUL_PATTERNS = [
    r"\bsuicid\w*\b",
    r"\bself[- ]?harm\b",
    r"\boverdos\w*\b",
    r"\bpurge\b",
    r"\bbulimi\w*\b",
    r"\banorexi\w*\b",
    r"\bstarv\w*\b",
    r"\bkill\s+(yourself|myself)\b",
    r"\bextreme\s+fast\w*\b",
    r"\b(0|zero)\s*calor\w*\b",
]

# ── Patterns to strip from model output ───────────────────────────────────
OUTPUT_STRIP_PATTERNS = [
    r"As an AI language model.*?[.!]",
    r"I am not a (doctor|medical|physician).*?[.!]",  # keep our own disclaimer
    r"<\|.*?\|>",     # model tokens
    r"\[INST\].*?\[/INST\]",  # instruction tokens
]

# ── Required fields for a valid user profile ──────────────────────────────
REQUIRED_FIELDS = ["name", "age", "diet_preference", "city", "country"]

VALID_DIET_PREFS = {
    "vegetarian", "non-vegetarian", "vegan", "pescatarian",
    "flexitarian", "keto", "paleo", "gluten-free"
}


class GuardrailEngine:
    """
    Multi-layer safety engine:
    1. Input validation — ensures required fields are present and sane
    2. Harmful query detection — blocks dangerous/self-harm queries
    3. Output sanitization — removes model artefacts and unsafe content
    """

    # ── Input Validation ───────────────────────────────────────────────────
    def validate_user_input(self, data: dict) -> dict:
        # Check required fields
        for field in REQUIRED_FIELDS:
            val = data.get(field, "")
            if not str(val).strip():
                return {
                    "valid": False,
                    "message": f"Missing required field: '{field}'. Please complete all fields."
                }

        # Age validation
        try:
            age = int(data["age"])
            if not (1 <= age <= 120):
                return {"valid": False, "message": "Please enter a valid age between 1 and 120."}
        except (ValueError, TypeError):
            return {"valid": False, "message": "Age must be a valid number."}

        # Diet preference validation
        diet = data.get("diet_preference", "").lower().strip()
        if diet not in VALID_DIET_PREFS:
            return {
                "valid": False,
                "message": f"Invalid diet preference. Choose from: {', '.join(sorted(VALID_DIET_PREFS))}."
            }

        # Name sanity check
        name = data.get("name", "")
        if len(name) > 100 or not re.match(r"^[\w\s'\-\.]+$", name):
            return {"valid": False, "message": "Please enter a valid name (letters, spaces, hyphens only)."}

        # Check for prompt injection attempts
        injection_patterns = [
            r"ignore\s+(previous|above|all)\s+instructions",
            r"jailbreak",
            r"pretend\s+you\s+are",
            r"act\s+as\s+if",
            r"<script",
            r"javascript:",
        ]
        full_text = json_safe_str(data)
        for pat in injection_patterns:
            if re.search(pat, full_text, re.IGNORECASE):
                return {
                    "valid": False,
                    "message": "Invalid input detected. Please provide genuine health information."
                }

        return {"valid": True, "message": "OK"}

    # ── Harmful Query Detection ────────────────────────────────────────────
    def is_harmful_query(self, text: str) -> bool:
        text_lower = text.lower()
        for pattern in HARMFUL_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                logger.warning("Harmful query pattern detected: %s", pattern)
                return True
        return False

    # ── Output Sanitization ────────────────────────────────────────────────
    def sanitize_output(self, text: str) -> str:
        if not text:
            return text
        for pattern in OUTPUT_STRIP_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)
        # Remove any leftover model-specific tokens
        text = re.sub(r"<<[A-Z_]+>>", "", text)
        # Normalize excessive blank lines
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        return text.strip()


def json_safe_str(data: dict) -> str:
    """Flatten dict values to a single string for pattern matching."""
    import json
    try:
        return json.dumps(data)
    except Exception:
        return str(data)
