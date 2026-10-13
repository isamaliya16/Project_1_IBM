"""
Nutrition Agentic AI Application
Powered by IBM Granite LLM via watsonx.ai
Follows Agentic AI SDLC, HAM principles, and AI Ethics guidelines.
"""

import os
import re
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from agents.nutrition_agent import NutritionAgent
from utils.guardrails import GuardrailEngine
from utils.plan_exporter import export_plan_to_md

# ── Bootstrap ──────────────────────────────────────────────────────────────
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "nutrition_ai_secret_2024")

# Singleton agent & guardrail engine
nutrition_agent = NutritionAgent()
guardrail_engine = GuardrailEngine()

# ── Static Frontend ────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


# ── API: Collect User Profile & Generate Plan ──────────────────────────────
@app.route("/api/generate-plan", methods=["POST"])
def generate_plan():
    try:
        data = request.get_json(force=True)
        logger.info("Received plan request for user: %s", data.get("name", "unknown"))

        # ── Guardrail: Input validation ─────────────────────────────────
        validation = guardrail_engine.validate_user_input(data)
        if not validation["valid"]:
            return jsonify({"success": False, "error": validation["message"]}), 400

        # ── Agent: Generate nutrition plan ──────────────────────────────
        plan = nutrition_agent.generate_nutrition_plan(data)

        # ── Guardrail: Output safety check ──────────────────────────────
        safe_plan = guardrail_engine.sanitize_output(plan)

        # ── Export to Markdown ──────────────────────────────────────────
        md_filename = export_plan_to_md(data, safe_plan)

        return jsonify({
            "success": True,
            "plan": safe_plan,
            "md_file": md_filename,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as exc:
        logger.error("Error generating plan: %s", exc, exc_info=True)
        return jsonify({"success": False, "error": "An internal error occurred. Please try again."}), 500


# ── API: Agentic Q&A Chat ──────────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()
        user_profile = data.get("user_profile", {})

        if not user_message:
            return jsonify({"success": False, "error": "Message cannot be empty."}), 400

        # Guardrail: block harmful queries
        if guardrail_engine.is_harmful_query(user_message):
            return jsonify({
                "success": True,
                "reply": (
                    "I'm your Nutrition AI assistant and I'm here to help with diet and "
                    "wellness questions. For medical emergencies or specific diagnoses, "
                    "please consult a qualified healthcare professional."
                )
            })

        reply = nutrition_agent.answer_query(user_message, user_profile)
        safe_reply = guardrail_engine.sanitize_output(reply)

        return jsonify({"success": True, "reply": safe_reply})

    except Exception as exc:
        logger.error("Chat error: %s", exc, exc_info=True)
        return jsonify({"success": False, "error": "Could not process your message. Please try again."}), 500


# ── API: Download saved .md plan ───────────────────────────────────────────
@app.route("/api/download-plan/<filename>")
def download_plan(filename):
    # Security: only allow simple filenames (no path traversal)
    if not re.match(r'^[\w\-]+\.md$', filename):
        return jsonify({"error": "Invalid filename."}), 400
    plans_dir = os.path.join(os.path.dirname(__file__), "plans")
    return send_from_directory(plans_dir, filename, as_attachment=True)


# ── API: Health check ──────────────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Nutrition Agentic AI", "model": "IBM Granite"})


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    logger.info("Starting Nutrition Agentic AI on http://localhost:%s", port)
    app.run(debug=False, host="0.0.0.0", port=port)
