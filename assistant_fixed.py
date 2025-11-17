import logging
from modules.emotion import detect_emotion, get_tone_prefix
from modules.logic import solve_expression, logical_puzzle
import openai
from config import OPENAI_API_KEY, OPENAI_MODEL, CONTEXT_LIMIT

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- AI response function using OpenAI ---
def ai_response(user_input: str, history: list):
    """Generate a concise, to-the-point response using OpenAI for all types of questions."""
    try:
        openai.api_key = OPENAI_API_KEY
        # Prepare context from history
        context = history[-CONTEXT_LIMIT:] if len(history) > CONTEXT_LIMIT else history
        messages = [{"role": "system", "content": "You are SKY, a helpful AI assistant. Provide concise, accurate, and to-the-point answers for any question. Keep responses short and direct."}]
        messages.extend(context)
        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=150,  # Limit for concise responses
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"AI response error: {e}")
        return "I'm sorry, I couldn't generate a response right now."

# --- Detect if query is factual ---
def is_factual_query(user_input: str):
    keywords = [
        "who", "what", "when", "where", "how", "tell me about",
        "latest", "news", "population", "capital", "invented", "discovered",
        "full form", "abbreviation", "stand for"
    ]
    return any(k in user_input.lower() for k in keywords)

# --- Main SKY reply function ---
def sky_reply(user_input: str, history: list):
    emotion = detect_emotion(user_input)
    tone = get_tone_prefix(emotion)
    user_lower = user_input.lower()

    # --- 1️⃣ Full-form queries → always search online ---
    if "full form" in user_lower or "stand for" in user_lower or "abbreviation" in user_lower:
        search_result = search_web(user_input)
        return f"Based on online sources:\n{search_result}"

    # --- 2️⃣ Arithmetic check ---
    arithmetic_keywords = ["+", "-", "*", "/", "calculate", "solve", "=", "what is"]
    if any(k in user_input for k in arithmetic_keywords):
        return solve_expression(user_input)

    # --- 3️⃣ Logical reasoning check ---
    logical_keywords = ["even", "odd", "logic", "reasoning", "puzzle"]
    if any(k in user_lower for k in logical_keywords):
        return logical_puzzle(user_input)

    # --- 4️⃣ All other queries → use AI for concise responses ---
    return ai_response(user_input, history)
