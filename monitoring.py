import logging
from datetime import datetime

# Set up monitoring logger (suppress console output)
monitor_logger = logging.getLogger('sky_monitor')
monitor_logger.setLevel(logging.INFO)
handler = logging.FileHandler('sky_monitor.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
monitor_logger.addHandler(handler)
# Prevent propagation to root logger to avoid console output
monitor_logger.propagate = False

def log_interaction(user_input, response, model_used, persona):
    """
    Log user interactions for analytics. Suppress console output.
    """
    # Suppress logging to console, only log to file
    monitor_logger.info(f"User: {user_input[:100]}... | Response: {response[:100]}... | Model: {model_used} | Persona: {persona}")

def get_stats():
    """
    Placeholder for retrieving stats from logs.
    """
    # In a real implementation, parse the log file for stats
    return {"total_interactions": 0, "models_used": [], "personas_used": []}
