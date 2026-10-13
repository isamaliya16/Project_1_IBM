# 🥗 NutriGuide AI — Personalized Nutrition Agentic Application

> **Powered by IBM Granite LLM via IBM watsonx.ai**  
> Built following all phases of the **Agentic AI Software Development Life Cycle (SDLC)**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-black?logo=flask)](https://flask.palletsprojects.com/)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-blue?logo=ibm)](https://www.ibm.com/watsonx)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Project Overview

**NutriGuide AI** is a web-based Agentic AI application that collects user health profiles and generates personalized **7-day nutrition plans** using IBM Granite LLM (via IBM watsonx.ai). It features:

- 🤖 **Agentic AI** — Conversational AI powered by IBM Granite 13B Instruct
- 🩺 **Medical Awareness** — Tailored advice for diabetes, hypertension, and more
- 🛡️ **AI Ethics & Guardrails** — HAM principles (Helpful, Accurate, Mindful)
- 💬 **Interactive Chat** — Follow-up nutrition Q&A in real time
- ⬇️ **Export** — Download your plan as a Markdown `.md` file
- 📱 **Responsive UI** — Works on desktop and mobile browsers
- 🔒 **Demo Mode** — Fully functional even without IBM API credentials

---

## 🚀 Quick Start (Windows)

### Option 1 — One-Click Launch

```bash
# Navigate into the app folder and double-click, OR run:
cd nutrition_ai
run.bat
```

The launcher will automatically:
1. ✅ Check Python installation
2. ✅ Create a virtual environment
3. ✅ Install all dependencies
4. ✅ Guide you through `.env` configuration
5. ✅ Open the app at `http://localhost:5000`

### Option 2 — Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/YogeshRaje/NutritionAgent-IBMBob.git
cd NutritionAgent-IBMBob/nutrition_ai

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
copy .env.example .env
# Edit .env with your IBM watsonx.ai credentials (see below)

# 5. Run the application
python app.py
```

Open your browser at **http://localhost:5000**

---

## ⚙️ Environment Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```env
# IBM watsonx.ai Credentials
WATSONX_API_KEY=your_ibm_cloud_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_watsonx_project_id_here

# Flask Settings
FLASK_SECRET_KEY=change_this_to_a_random_secret_key
FLASK_PORT=5000
```

### How to get IBM watsonx.ai credentials

1. Sign in to [IBM Cloud](https://cloud.ibm.com/)
2. Navigate to **watsonx.ai** → Create or open a project
3. Go to **IAM** → **API Keys** → Create a new API key
4. Copy the **Project ID** from your watsonx.ai project settings

> **Demo Mode:** If no API key is configured, the app runs in demo mode with built-in nutrition templates — no credentials required.

---

## 🏗️ Project Structure

```
NutritionAgent-IBMBob/
│
└── nutrition_ai/                     # Application root
    ├── app.py                        # Flask REST API entry point
    ├── requirements.txt              # Python dependencies
    ├── .env.example                  # Environment variables template
    ├── run.bat                       # Windows one-click launcher
    │
    ├── agents/
    │   ├── __init__.py
    │   └── nutrition_agent.py        # IBM Granite LLM agentic core
    │
    ├── utils/
    │   ├── __init__.py
    │   ├── guardrails.py             # AI safety & ethics engine
    │   └── plan_exporter.py          # Markdown plan file exporter
    │
    ├── frontend/
    │   ├── index.html                # Web UI
    │   ├── style.css                 # Styling
    │   └── app.js                    # Frontend JavaScript logic
    │
    └── plans/                        # Auto-generated .md nutrition plans
        └── sample_nutrition_plan_priya_sharma.md
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web application home |
| `POST` | `/api/generate-plan` | Generate personalized 7-day nutrition plan |
| `POST` | `/api/chat` | Agentic Q&A with NutriGuide |
| `GET` | `/api/download-plan/<filename>` | Download generated `.md` plan |
| `GET` | `/api/health` | Service health check |

---

## 🔄 Agentic AI SDLC Phases

| Phase | Implementation |
|-------|---------------|
| **1. Problem Identification** | Personalized nutrition guidance gap for health-conscious users |
| **2. Agent Design** | `NutritionAgent` class with IBM Granite LLM persona (NutriGuide) |
| **3. Data Collection** | Structured web form: name, age, gender, location, diet, medical history |
| **4. Safety & Guardrails** | `GuardrailEngine`: input validation, harmful query detection, output sanitization |
| **5. Model Integration** | IBM Granite 13B Instruct via `ibm-watsonx-ai` SDK |
| **6. Development** | Flask REST API + HTML/CSS/JS frontend |
| **7. Testing** | Mock mode fallback, error handling, API health endpoint |
| **8. Deployment** | `run.bat` one-click launcher |
| **9. Monitoring** | Python logging, structured error responses |

---

## 🛡️ AI Ethics & Guardrails

### HAM Principles
- **H**elpful — Actionable, practical nutrition advice tailored to the individual
- **A**ccurate — Evidence-based nutritional science recommendations
- **M**indful — Sensitive to medical conditions, cultural background, and dietary preferences

### Safety Guardrails
| Layer | Protection |
|-------|-----------|
| ✅ Input Validation | Required fields, age range (1–120), diet preference whitelist |
| ✅ Injection Detection | Blocks prompt injection and jailbreak attempts |
| ✅ Harmful Query Detection | Blocks self-harm, eating disorder, and extreme diet queries |
| ✅ Output Sanitization | Strips model artifacts and unsafe output patterns |
| ✅ Medical Disclaimer | Automatically appended to every generated plan |
| ✅ Privacy | No user data persisted beyond the current session |

---

## 📱 Features at a Glance

| Feature | Description |
|---------|-------------|
| 📋 7-Day Meal Plan | Breakfast, snacks, lunch & dinner with calorie counts |
| 🩺 Medical Awareness | Optimized for diabetes, hypertension, and more |
| 💬 AI Chat | Ask NutriGuide follow-up nutrition questions |
| ⬇️ Download Plan | Export as Markdown `.md` file |
| 🛡️ Ethics Engine | Multi-layer guardrails prevent harmful advice |
| ⚕️ Disclaimer | Medical disclaimer on every plan |
| 📱 Responsive | Desktop and mobile friendly |

---

## 🐍 Requirements

```
Python >= 3.11
flask==3.0.3
flask-cors==4.0.1
ibm-watsonx-ai==1.1.2
python-dotenv==1.0.1
requests==2.32.3
markdown==3.6
```

---

## ⚕️ Medical Disclaimer

> This application provides AI-generated nutritional information for **educational and informational purposes only**. It is **not a substitute** for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider, registered dietitian, or licensed nutritionist before making significant dietary changes, especially if you have existing medical conditions (diabetes, hypertension, kidney disease, cardiovascular conditions, etc.).

---

## 📄 License

MIT License — Free to use, modify, and distribute with attribution.

---

*NutriGuide AI · Powered by IBM Granite · Built with AI Ethics*
