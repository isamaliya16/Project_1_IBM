"""
Plan Exporter — saves generated nutrition plans as Markdown (.md) files
Agentic AI SDLC Phase: Output & Persistence
"""

import os
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

PLANS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plans")


def export_plan_to_md(user_data: dict, plan_content: str) -> str:
    """
    Saves the nutrition plan as a .md file.
    Returns the filename (not full path) for the download endpoint.
    """
    os.makedirs(PLANS_DIR, exist_ok=True)

    name_slug = re.sub(r"[^\w]", "_", user_data.get("name", "user").lower())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nutrition_plan_{name_slug}_{timestamp}.md"
    filepath = os.path.join(PLANS_DIR, filename)

    header = f"""---
title: "Personalized Nutrition Plan — {user_data.get('name', 'User')}"
generated_by: "NutriGuide AI (IBM Granite)"
generated_at: "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
user_age: {user_data.get('age', 'N/A')}
diet_preference: "{user_data.get('diet_preference', 'N/A')}"
location: "{user_data.get('city', '')}, {user_data.get('country', '')}"
medical_history: "{user_data.get('medical_history', 'None')}"
---

"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header + plan_content)

    logger.info("Nutrition plan saved: %s", filepath)
    return filename
