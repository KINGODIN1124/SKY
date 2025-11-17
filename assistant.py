import logging
from modules.emotion import detect_emotion, get_tone_prefix
from modules.logic import solve_expression, logical_puzzle
from modules.file_handler import handle_file_upload
from modules.web_browse import browse_web
from modules.personas import get_persona_prompt
from modules.translation import translate_text, detect_language
from modules.rich_output import render_rich_output
from modules.monitoring import log_interaction
from modules.memory import retrieve_relevant_memory
from modules.weather import get_weather, detect_location
from modules.news import get_latest_news
from modules.stocks import get_stock_price
from modules.sports import get_sports_scores
from modules.currency import get_exchange_rate
from modules.wiki import get_wikipedia_summary
from config import GROQ_API_KEY, GROQ_MODEL, CONTEXT_LIMIT, CURRENT_PERSONA, AVAILABLE_MODELS
from groq import Groq

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress httpx logs to avoid HTTP request details in output
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- AI response function using Groq ---
def ai_response(user_input: str, history: list, model=GROQ_MODEL):
    """Generate a concise, to-the-point response using Groq for all types of questions."""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        # Prepare context from history with embeddings
        relevant_memory = retrieve_relevant_memory(user_input, history)
        context = (relevant_memory + history)[-CONTEXT_LIMIT:] if len(history) > CONTEXT_LIMIT else history
        # Check for repeat queries
        if relevant_memory and any(user_input.lower() in mem['content'].lower() for mem in relevant_memory):
            # Find the assistant's response to the similar query
            similar_idx = next((i for i, mem in enumerate(relevant_memory) if user_input.lower() in mem['content'].lower()), None)
            if similar_idx is not None:
                # Get the next message if it's assistant's response
                history_idx = history.index(relevant_memory[similar_idx]) + 1
                if history_idx < len(history) and history[history_idx]['role'] == 'assistant':
                    return history[history_idx]['content']
            return relevant_memory[0]['content']
        system_prompt = get_persona_prompt(CURRENT_PERSONA)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(context)
        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=150,  # Limit for concise responses
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        # Log interaction (suppress output)
        log_interaction(user_input, reply, model, CURRENT_PERSONA)
        # Render rich output (suppress output)
        render_rich_output(reply)
        return reply
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

# --- Short answers for common questions ---
short_answers = {
    "what are non renewable sources of energy": "Non-renewable energy sources include fossil fuels like coal, petroleum, and natural gas, which cannot be replenished once depleted.",
    "what is non renewable energy": "Non-renewable energy is energy from sources that will eventually run out, such as fossil fuels (coal, oil, gas) and nuclear energy.",
    # Add more as needed
}

# --- Tool calling for file/web ---
def handle_tool_calls(user_input: str):
    if user_input.startswith("upload:"):
        file_path = user_input[7:].strip()
        return handle_file_upload(file_path)
    elif user_input.startswith("browse:"):
        url = user_input[7:].strip()
        return browse_web(url)
    elif user_input.startswith("translate:"):
        parts = user_input[10:].split(" to ")
        if len(parts) == 2:
            text, lang = parts
            return translate_text(text.strip(), lang.strip())
        else:
            return "Usage: translate: <text> to <lang>"
    elif "latest news" in user_input.lower():
        # Extract topic if specified, e.g., "latest news of Paris" -> "Paris"
        parts = user_input.lower().split("latest news")
        if len(parts) > 1 and parts[1].strip():
            topic = parts[1].strip()
            if topic.startswith("of ") or topic.startswith("for "):
                topic = topic[3:].strip()
            return get_latest_news(query=topic)
        else:
            return get_latest_news()
    elif user_input.lower().startswith("how is the weather") or user_input.lower().startswith("what is the weather") or user_input.lower().startswith("weather today"):
        city, country = detect_location()
        if city:
            return get_weather(city)
        else:
            return "Unable to detect your location. Please specify a city, e.g., 'weather in New York'."
    elif user_input.lower().startswith("weather in"):
        city = user_input[11:].strip()
        return get_weather(city)
    elif user_input.lower().startswith("stock price of") or user_input.lower().startswith("price of"):
        symbol = user_input.split()[-1].upper()
        return get_stock_price(symbol)
    elif user_input.lower().startswith("latest sports scores") or user_input.lower().startswith("sports scores"):
        return get_sports_scores()
    elif user_input.lower().startswith("exchange rate") or user_input.lower().startswith("convert currency"):
        # Simple parsing: e.g., "exchange rate USD to EUR"
        parts = user_input.split()
        if len(parts) >= 4:
            from_curr = parts[-3].upper()
            to_curr = parts[-1].upper()
            return get_exchange_rate(from_curr, to_curr)
        else:
            return "Usage: exchange rate USD to EUR"
    elif user_input.lower().startswith("wikipedia") or user_input.lower().startswith("tell me about"):
        topic = user_input[10:].strip() if user_input.lower().startswith("wikipedia") else user_input[13:].strip()
        return get_wikipedia_summary(topic)
    return None

# --- Main SKY reply function ---
def sky_reply(user_input: str, history: list):
    emotion = detect_emotion(user_input)
    tone = get_tone_prefix(emotion)
    user_lower = user_input.lower()

    # --- 0️⃣ Tool calls ---
    tool_result = handle_tool_calls(user_input)
    if tool_result:
        return tool_result

    # --- 1️⃣ Full-form queries → use AI ---
    if "full form" in user_lower or "stand for" in user_lower or "abbreviation" in user_lower:
        return ai_response(user_input, history)

    # --- 2️⃣ Arithmetic check ---
    arithmetic_keywords = ["+", "-", "*", "/", "calculate", "solve", "="]
    if any(k in user_input for k in arithmetic_keywords) or user_input.lower().startswith("what is") and any(char.isdigit() for char in user_input):
        return solve_expression(user_input)

    # --- 3️⃣ Logical reasoning check ---
    logical_keywords = ["even", "odd", "logic", "reasoning", "puzzle"]
    if any(k in user_lower for k in logical_keywords):
        return logical_puzzle(user_input)

    # --- 4️⃣ All other queries → use AI for concise responses ---
    return ai_response(user_input, history, model=GROQ_MODEL)
