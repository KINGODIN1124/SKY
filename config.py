# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('AI/.env')

# Groq API key
GROQ_API_KEY = "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"

# Available models for SKY (Groq)
AVAILABLE_MODELS = ["llama-3.1-8b-instant", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"]
GROQ_MODEL = "llama-3.1-8b-instant"  # Default model

# Persona selection
CURRENT_PERSONA = "default"

# OpenAI API key for vision (if added)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Weather API key (OpenWeatherMap)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

# News API key (NewsAPI)
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# How many previous messages to keep in context (increased)
CONTEXT_LIMIT = 20
