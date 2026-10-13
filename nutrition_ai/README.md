# 🥗 NutriGuide AI — Personalized Nutrition Agentic Application

> **Powered by IBM Granite LLM via IBM watsonx.ai**  
> Built following all phases of the **Agentic AI Software Development Life Cycle (SDLC)**

---

## 📋 Project Overview

**NutriGuide AI** is a web-based Agentic AI application that collects user health profiles and generates personalized 7-day nutrition plans using IBM Granite LLM. It features a conversational AI agent for follow-up queries, follows AI ethics guidelines (HAM principles), includes guardrails, and exports plans as Markdown files.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- IBM watsonx.ai account (optional — demo mode available without it)

### Run the Application (Windows)
```bash
# Simply double-click or run:
run.bat
```

The `.bat` file will:
1. ✅ Check Python installation  
2. ✅ Create a virtual environment  
3. ✅ Install all dependencies  
4. ✅ Guide you through `.env` configuration  
5. ✅ Launch the app at `http://localhost:5000`

---

## ⚙️ Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/nutrition-agentic-ai.git
cd nutrition-agentic-ai/nutrition_ai

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
copy .env.example .env
# Edit .env with your IBM watsonx.ai API key and project ID

# 5. Run the application
python app.py
```

---

## 🔑 IBM watsonx.ai Configuration

Edit the `.env` file with your credentials:

```env
WATSONX_API_KEY=your_ibm_cloud_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_watsonx_project_id_here
FLASK_SECRET_KEY=your_random_secret_key
FLASK_PORT=5000
```

**How to get credentials:**
1. Sign in to [IBM Cloud](https://cloud.ibm.com/)
2. Navigate to **watsonx.ai** → Create or open a project
3. Go to **IAM** → **API Keys** → Create a new API key
4. Copy the **Project ID** from your watsonx.ai project settings

> **Demo Mode:** If no API key is configured, the app runs in demo mode with built-in nutrition templates.

---

## 🏗️ Project Structure

```
nutrition_ai/
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── run.bat                 # Windows launcher script
├── README.md               # This file
│
├── agents/
│   ├── __init__.py
│   └── nutrition_agent.py  # IBM Granite LLM agentic core
│
├── utils/
│   ├── __init__.py
│   ├── guardrails.py       # AI safety & ethics engine
│   └── plan_exporter.py    # Markdown plan file exporter
│
├── frontend/
│   ├── index.html          # Web UI
│   ├── style.css           # Styling
│   └── app.js              # Frontend logic
│
└── plans/                  # Generated .md nutrition plans (auto-created)
```

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

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web application home |
| `POST` | `/api/generate-plan` | Generate personalized nutrition plan |
| `POST` | `/api/chat` | Agentic Q&A with NutriGuide |
| `GET` | `/api/download-plan/<filename>` | Download generated .md plan |
| `GET` | `/api/health` | Service health check |

---

## 🛡️ AI Ethics & Guardrails

### HAM Principles
- **H**elpful — Actionable, practical nutrition advice
- **A**ccurate — Evidence-based nutritional science
- **M**indful — Sensitive to medical conditions, culture, and preferences

### Safety Guardrails
- ✅ **Input validation** — Required fields, age range, injection detection
- ✅ **Harmful query detection** — Blocks self-harm, extreme dieting, dangerous advice
- ✅ **Output sanitization** — Removes model artifacts and unsafe patterns
- ✅ **Medical disclaimer** — Included in every generated plan
- ✅ **Privacy** — No user data is persisted beyond the session

---

## 📱 Features

- 📋 **7-Day Personalized Nutrition Plan** — Breakfast, snacks, lunch, dinner with calorie counts
- 🩺 **Medical Condition Awareness** — Tailored plans for diabetes, hypertension, and more
- 💬 **Agentic AI Chat** — Ask follow-up nutrition questions in real time
- ⬇️ **Download Plan** — Export as a Markdown `.md` file
- 🛡️ **Ethics Engine** — Guardrails prevent harmful advice
- ⚕️ **Medical Disclaimer** — Clear disclaimer on every plan
- 📱 **Responsive Design** — Works on desktop and mobile

---

## 📂 GitHub Setup (Task 1)

```bash
# 1. Sign in to github.com
# 2. Create new repository: nutrition-agentic-ai
# 3. Clone locally
git clone https://github.com/YOUR_USERNAME/nutrition-agentic-ai.git

# 4. Copy project files into the cloned folder
# 5. Push to GitHub
git add .
git commit -m "feat: initial Nutrition Agentic AI application"
git push origin main
```

---

## ⚕️ Medical Disclaimer

> This application provides AI-generated nutritional information for **educational and informational purposes only**. It is **not a substitute** for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider, registered dietitian, or licensed nutritionist before making significant dietary changes, especially if you have existing medical conditions (diabetes, hypertension, kidney disease, cardiovascular conditions, etc.).

---

## 📄 License

MIT License — Free to use, modify, and distribute with attribution.

---

*NutriGuide AI · Powered by IBM Granite · Built with ❤️ and AI Ethics*
