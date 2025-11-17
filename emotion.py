# modules/emotion.py

def detect_emotion(text: str) -> str:
    text = text.lower()
    if any(word in text for word in ["sad", "unhappy", "upset"]):
        return "sad"
    elif any(word in text for word in ["angry", "mad", "frustrated"]):
        return "angry"
    elif any(word in text for word in ["happy", "great", "awesome"]):
        return "happy"
    elif any(word in text for word in ["why", "how", "what", "who"]):
        return "curious"
    else:
        return "neutral"

def get_tone_prefix(emotion: str) -> str:
    mapping = {
        "happy": "friendly and upbeat",
        "sad": "empathetic and supportive",
        "angry": "calm and professional",
        "curious": "informative and detailed",
        "neutral": "neutral and clear"
    }
    return mapping.get(emotion, "neutral and clear")
