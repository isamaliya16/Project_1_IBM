"""
NutritionAgent — Core Agentic AI logic
IBM Granite LLM via watsonx.ai
Agentic SDLC Phase: Agent Design & Execution
"""

import os
import logging
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

logger = logging.getLogger(__name__)

# ── Granite model constants ────────────────────────────────────────────────
GRANITE_MODEL_ID = "ibm/granite-13b-instruct-v2"

SYSTEM_PERSONA = """You are NutriGuide, a professional AI nutritionist powered by IBM Granite. 
Your role is to provide helpful, accurate, and personalized nutrition advice.

CORE PRINCIPLES (HAM — Helpful, Accurate, Mindful):
- Helpful: Provide actionable, practical advice tailored to the user.
- Accurate: Base recommendations on established nutritional science.
- Mindful: Be sensitive to cultural backgrounds, medical conditions, and personal preferences.

AI ETHICS GUARDRAILS:
- Never prescribe medications or act as a replacement for licensed medical professionals.
- Always include disclaimers for users with serious medical conditions.
- Do not provide extreme caloric restrictions (below 1200 kcal/day for adults).
- Respect dietary preferences (vegetarian, non-vegetarian, vegan, etc.).
- Be inclusive and non-judgmental about body types and food cultures.
- Protect user privacy — never ask for more personal information than needed.

RESPONSE FORMAT:
- Be warm, encouraging, and empathetic in tone.
- Use clear sections and bullet points for readability.
- Always end with a medical disclaimer when relevant."""


class NutritionAgent:
    """
    Agentic AI system that:
    1. Accepts structured user profiles (name, age, diet, medical history, location)
    2. Generates a personalized multi-day nutrition plan via IBM Granite
    3. Answers follow-up queries in a conversational agentic loop
    """

    def __init__(self):
        self._client = None
        self._model = None
        self._init_model()

    def _init_model(self):
        """Initialize IBM watsonx.ai Granite model."""
        api_key = os.getenv("WATSONX_API_KEY", "")
        url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        project_id = os.getenv("WATSONX_PROJECT_ID", "")

        if not api_key or api_key == "your_ibm_cloud_api_key_here":
            logger.warning("WATSONX_API_KEY not set — running in demo/mock mode.")
            self._model = None
            return

        try:
            credentials = Credentials(url=url, api_key=api_key)
            self._client = APIClient(credentials)
            self._model = ModelInference(
                model_id=GRANITE_MODEL_ID,
                credentials=credentials,
                project_id=project_id,
                params={
                    GenParams.MAX_NEW_TOKENS: 1200,
                    GenParams.MIN_NEW_TOKENS: 100,
                    GenParams.TEMPERATURE: 0.7,
                    GenParams.TOP_P: 0.9,
                    GenParams.REPETITION_PENALTY: 1.1,
                    GenParams.STOP_SEQUENCES: ["<|endoftext|>"],
                }
            )
            logger.info("IBM Granite model initialized successfully.")
        except Exception as exc:
            logger.error("Failed to initialize Granite model: %s", exc)
            self._model = None

    # ── Public: Generate full nutrition plan ──────────────────────────────
    def generate_nutrition_plan(self, user_data: dict) -> str:
        prompt = self._build_plan_prompt(user_data)
        if self._model:
            try:
                response = self._model.generate_text(prompt=prompt)
                return response.strip()
            except Exception as exc:
                logger.error("Granite API error: %s", exc)
                return self._mock_nutrition_plan(user_data)
        return self._mock_nutrition_plan(user_data)

    # ── Public: Answer a follow-up query ──────────────────────────────────
    def answer_query(self, query: str, user_profile: dict) -> str:
        prompt = self._build_chat_prompt(query, user_profile)
        if self._model:
            try:
                response = self._model.generate_text(prompt=prompt)
                return response.strip()
            except Exception as exc:
                logger.error("Granite API error: %s", exc)
                return self._mock_chat_response(query)
        return self._mock_chat_response(query)

    # ── Prompt builders ────────────────────────────────────────────────────
    def _build_plan_prompt(self, u: dict) -> str:
        medical = u.get("medical_history", "None")
        allergies = u.get("allergies", "None")
        goals = u.get("goals", "General healthy eating")
        activity = u.get("activity_level", "Moderate")

        return f"""{SYSTEM_PERSONA}

USER PROFILE:
- Name: {u.get('name', 'User')}
- Age: {u.get('age', 'N/A')} years
- Gender: {u.get('gender', 'Not specified')}
- Location: {u.get('city', '')}, {u.get('country', '')}
- Diet Preference: {u.get('diet_preference', 'Non-vegetarian')}
- Medical History: {medical}
- Allergies / Intolerances: {allergies}
- Health Goals: {goals}
- Activity Level: {activity}

TASK:
Generate a comprehensive, personalized 7-day nutrition plan for this user.

The plan MUST include:
1. **Nutritional Overview** — daily calorie target, macronutrient breakdown (protein/carbs/fats), key vitamins & minerals to focus on, considering their medical conditions.
2. **7-Day Meal Plan** — For each day list Breakfast, Mid-Morning Snack, Lunch, Afternoon Snack, and Dinner with approximate calorie counts.
3. **Hydration Guidelines** — daily water intake recommendation.
4. **Foods to Emphasize** — 8–10 foods specifically beneficial for their condition.
5. **Foods to Avoid/Limit** — based on medical history and diet preference.
6. **Supplement Suggestions** (if appropriate) — with a note to consult a doctor first.
7. **Lifestyle Tips** — 3–5 tips aligned with their health goals and activity level.
8. **Medical Disclaimer** — clear and prominent.

Tone: warm, encouraging, professional. Use emojis sparingly for readability.

NUTRITION PLAN:"""

    def _build_chat_prompt(self, query: str, profile: dict) -> str:
        context = ""
        if profile:
            context = (
                f"User context: {profile.get('name', 'User')}, "
                f"Age {profile.get('age', 'N/A')}, "
                f"Diet: {profile.get('diet_preference', 'N/A')}, "
                f"Medical history: {profile.get('medical_history', 'None')}. "
            )

        return f"""{SYSTEM_PERSONA}

{context}

USER QUESTION: {query}

Provide a helpful, accurate, and safe answer. If the question requires medical diagnosis or treatment, 
remind the user to consult a healthcare professional. Keep the answer concise (under 200 words) and practical.

ANSWER:"""

    # ── Mock responses (when API key not configured) ───────────────────────
    def _mock_nutrition_plan(self, u: dict) -> str:
        name = u.get("name", "there")
        diet = u.get("diet_preference", "balanced")
        medical = u.get("medical_history", "None")
        age = u.get("age", "N/A")

        medical_note = ""
        if "diabetes" in str(medical).lower():
            medical_note = "\n> ⚠️ **Diabetes-Specific Note:** Low glycemic index foods are prioritized. Limit refined carbohydrates and sugars. Monitor blood sugar regularly."
        elif "blood pressure" in str(medical).lower() or "hypertension" in str(medical).lower():
            medical_note = "\n> ⚠️ **Blood Pressure Note:** Low-sodium foods are emphasized. Rich in potassium and magnesium. Limit processed and salty foods."

        return f"""# 🥗 Personalized 7-Day Nutrition Plan for {name}

**Generated by NutriGuide AI | Powered by IBM Granite**
**Date:** {__import__('datetime').datetime.now().strftime('%B %d, %Y')}
{medical_note}

---

## 📊 Nutritional Overview

| Parameter | Target |
|-----------|--------|
| Daily Calories | ~1,800–2,000 kcal |
| Protein | 25–30% (~112–150g) |
| Carbohydrates | 45–50% (~202–250g) |
| Healthy Fats | 20–25% (~40–55g) |
| Fiber | ≥25g/day |
| Sodium | <2,300mg/day |

---

## 🍽️ 7-Day Meal Plan

### Day 1 — Monday
| Meal | Food | Calories |
|------|------|----------|
| Breakfast | Oatmeal with berries & chia seeds + Green tea | ~350 kcal |
| Mid-Morning | Apple + 10 almonds | ~150 kcal |
| Lunch | Brown rice, lentil dal, mixed vegetable curry, salad | ~550 kcal |
| Snack | Carrot sticks with hummus | ~120 kcal |
| Dinner | Grilled {'chicken breast' if 'veg' not in diet.lower() else 'tofu'} + steamed broccoli + quinoa | ~450 kcal |

### Day 2 — Tuesday
| Meal | Food | Calories |
|------|------|----------|
| Breakfast | Greek yogurt with banana & flaxseeds | ~320 kcal |
| Mid-Morning | Orange + walnuts (6 halves) | ~160 kcal |
| Lunch | Whole wheat roti, chickpea curry, cucumber raita | ~500 kcal |
| Snack | Mixed seeds trail mix | ~130 kcal |
| Dinner | {'Baked salmon' if 'veg' not in diet.lower() else 'Paneer tikka'} + roasted vegetables + brown rice | ~480 kcal |

### Day 3 — Wednesday
| Meal | Food | Calories |
|------|------|----------|
| Breakfast | Vegetable omelette / Scrambled tofu + whole grain toast | ~370 kcal |
| Mid-Morning | Pear + pumpkin seeds | ~140 kcal |
| Lunch | Multigrain bread sandwich, sprout salad, buttermilk | ~480 kcal |
| Snack | Roasted chana (chickpeas) | ~120 kcal |
| Dinner | {'Chicken soup' if 'veg' not in diet.lower() else 'Lentil soup'} + whole wheat bread + salad | ~430 kcal |

### Day 4 — Thursday
| Meal | Food | Calories |
|------|------|----------|
| Breakfast | Smoothie (spinach, banana, almond milk, protein powder) | ~340 kcal |
| Mid-Morning | Guava + handful of cashews | ~155 kcal |
| Lunch | Quinoa pulao with mixed vegetables + raita | ~520 kcal |
| Snack | Sliced cucumber & tomato with lemon | ~60 kcal |
| Dinner | {'Grilled fish tacos' if 'veg' not in diet.lower() else 'Veggie tacos'} with whole wheat wrap | ~460 kcal |

### Day 5 — Friday
| Meal | Food | Calories |
|------|------|----------|
| Breakfast | Poha (flattened rice) with vegetables + herbal tea | ~300 kcal |
| Mid-Morning | Watermelon slices | ~80 kcal |
| Lunch | Mixed dal, rice, bitter gourd sabzi + salad | ~530 kcal |
| Snack | Roasted makhana (fox nuts) | ~100 kcal |
| Dinner | {'Egg curry' if 'veg' not in diet.lower() else 'Palak paneer'} + 2 rotis + steamed vegetables | ~500 kcal |

### Day 6 — Saturday
| Meal | Food | Calories |
|------|------|----------|
| Breakfast | Idli (3) with sambar & coconut chutney | ~330 kcal |
| Mid-Morning | Mixed fruit bowl | ~120 kcal |
| Lunch | {'Chicken biryani (small portion)' if 'veg' not in diet.lower() else 'Vegetable biryani'} + raita + salad | ~560 kcal |
| Snack | Herbal green tea + digestive biscuits (2) | ~100 kcal |
| Dinner | Vegetable soup + whole grain crispbreads + {'boiled egg' if 'veg' not in diet.lower() else 'cheese'} | ~380 kcal |

### Day 7 — Sunday
| Meal | Food | Calories |
|------|------|----------|
| Breakfast | Whole grain pancakes with honey & fruit | ~360 kcal |
| Mid-Morning | Coconut water + handful of almonds | ~140 kcal |
| Lunch | {'Mutton/chicken stew' if 'veg' not in diet.lower() else 'Rajma curry'} + brown rice + salad | ~580 kcal |
| Snack | Dark chocolate (1–2 squares) + walnuts | ~150 kcal |
| Dinner | Grilled vegetables + {'tuna' if 'veg' not in diet.lower() else 'paneer'} salad + whole grain bread | ~420 kcal |

---

## 💧 Hydration Guidelines
- Drink **8–10 glasses (2.0–2.5 litres)** of water daily
- Start each morning with 1 glass of warm water + lemon
- Herbal teas (green tea, chamomile) count toward hydration
- Limit sugary drinks, sodas, and excessive caffeine (max 2 cups/day)

---

## ✅ Foods to Emphasize

1. **Leafy greens** (spinach, kale, methi) — Iron, folate, antioxidants
2. **Whole grains** (brown rice, quinoa, oats) — Fiber, sustained energy
3. **Legumes** (lentils, chickpeas, rajma) — Plant protein, fiber
4. **Berries** (blueberries, strawberries) — Antioxidants, low glycemic
5. **Nuts & seeds** (almonds, walnuts, flaxseeds) — Omega-3, healthy fats
6. **Cruciferous vegetables** (broccoli, cauliflower) — Cancer-fighting compounds
7. **Citrus fruits** (oranges, lemons) — Vitamin C, immune support
8. **Fermented foods** (yogurt, buttermilk) — Probiotics, gut health
9. **Sweet potato** — Beta-carotene, fiber, low GI
10. **Turmeric & ginger** — Anti-inflammatory properties

---

## ❌ Foods to Avoid / Limit

- Refined sugars and white flour products (maida, white bread, cakes)
- Deep-fried and ultra-processed foods (chips, instant noodles)
- Sugary beverages (sodas, packaged juices, energy drinks)
- Excessive salt and high-sodium processed foods
- Alcohol (limit strictly, especially with medical conditions)
- Artificial sweeteners in excess

---

## 💊 Supplement Suggestions
*(Consult your doctor before starting any supplement)*

- **Vitamin D3** (if limited sun exposure)
- **Omega-3 fatty acids** (if low fish intake)
- **Vitamin B12** (especially for vegetarians)
- **Magnesium** (supports sleep, muscle function)
- **Probiotics** (gut health and immunity)

---

## 🌟 Lifestyle Tips

1. **Eat mindfully** — Chew slowly, avoid screens during meals, stop at 80% full
2. **Meal prep Sundays** — Prepare staples (grains, legumes) in advance to stay on track
3. **Move daily** — Even 30 minutes of brisk walking makes a significant difference
4. **Sleep 7–8 hours** — Poor sleep disrupts hunger hormones and increases cravings
5. **Stress management** — Practice deep breathing, yoga, or meditation to reduce cortisol-driven eating

---

## ⚕️ Medical Disclaimer

> **IMPORTANT:** This nutrition plan is generated by an AI system for general informational and educational purposes only. It is **not** a substitute for professional medical advice, diagnosis, or treatment.
>
> - **Always consult** a registered dietitian, nutritionist, or licensed physician before making significant changes to your diet, especially if you have existing medical conditions (diabetes, hypertension, kidney disease, cardiovascular conditions, etc.).
> - **Do not use** this plan as a basis for stopping or modifying prescribed medications.
> - Individual nutritional needs vary. This plan provides general guidance and should be personalized by a healthcare professional.
> - In case of any adverse reactions or health concerns, **seek immediate medical attention**.
>
> *NutriGuide AI | Powered by IBM Granite | Generated with care, not a substitute for clinical care.*

---
*Plan generated for {name} | Age: {age} | Diet: {diet.title()} | {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}*
"""

    def _mock_chat_response(self, query: str) -> str:
        q = query.lower()
        if any(w in q for w in ["diabetes", "sugar", "blood sugar", "glucose"]):
            return (
                "For diabetes management, focus on **low glycemic index (GI) foods** like oats, legumes, "
                "leafy greens, and whole grains. Avoid refined sugars, white bread, and sugary drinks. "
                "Eating smaller, frequent meals helps stabilize blood sugar. Fiber-rich foods slow glucose absorption. "
                "Always monitor your blood sugar as advised by your doctor and follow their medication plan. 🩺"
            )
        if any(w in q for w in ["blood pressure", "hypertension", "bp"]):
            return (
                "For blood pressure management, follow the **DASH diet** — rich in fruits, vegetables, whole grains, "
                "and low-fat dairy. Reduce sodium to <2,300mg/day. Potassium-rich foods (bananas, sweet potatoes) "
                "help counter sodium's effects. Limit alcohol, caffeine, and processed foods. "
                "Regular exercise (30 min/day) also significantly lowers BP. Consult your cardiologist regularly. 💙"
            )
        if any(w in q for w in ["protein", "muscle", "gym", "workout"]):
            return (
                "For muscle building and fitness, aim for **1.6–2.2g of protein per kg body weight** daily. "
                "Good sources: eggs, chicken, fish, lentils, Greek yogurt, tofu, and quinoa. "
                "Time your protein intake — consume 20–30g within 30 minutes post-workout. "
                "Don't neglect carbohydrates — they fuel your workouts. Stay well hydrated! 💪"
            )
        if any(w in q for w in ["weight loss", "lose weight", "fat loss", "slim"]):
            return (
                "Sustainable weight loss comes from a **modest caloric deficit (300–500 kcal/day)** combined with exercise. "
                "Focus on whole foods, high fiber, and lean proteins to stay full. "
                "Avoid crash diets — they cause muscle loss and nutrient deficiencies. "
                "Aim for 0.5–1kg loss per week. Drink water before meals. Sleep 7–8 hours. "
                "Small, consistent changes beat dramatic short-term fixes. 🌿"
            )
        return (
            "That's a great nutrition question! As your AI nutritionist, I recommend focusing on **whole, "
            "minimally processed foods**, staying hydrated, and eating a balanced variety of macronutrients. "
            "For personalized advice specific to your health condition, please consult a registered dietitian. "
            "Feel free to ask me anything about nutrition, meal planning, or healthy eating habits! 😊"
        )
