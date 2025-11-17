# sky.py
from modules.memory import load_memory, save_memory, build_embeddings
from modules.speech import init_tts, speak_text, listen_to_user
from modules.assistant import sky_reply
from modules.file_handler import handle_file_upload
from modules.web_browse import browse_web
from modules.translation import translate_text
from config import CURRENT_PERSONA

# --- Initialize ---
conversation_history = load_memory()
# Defer embeddings build until needed to speed up startup
enable_tts = input("Do you want SKY to speak? (y/n): ").strip().lower() == "y"
engine = init_tts(enable_tts)
print("\nSKY is ready! Type 'exit' to quit.\n")

# Initial greeting
initial_reply = "Hello! ready to answer all the questions"
speak_text(initial_reply, engine, enable_tts)
conversation_history.append({"role": "assistant", "content": initial_reply})
save_memory(conversation_history)

while True:
    user_input = listen_to_user()
    if user_input.strip().lower() in ["exit", "quit", "bye"]:
        speak_text("Goodbye!", engine, enable_tts)
        break

    # Generate reply (search + logic + rule-based + tools)
    reply = sky_reply(user_input, conversation_history)

    # Speak and display reply
    speak_text(reply, engine, enable_tts)

    # Save conversation history
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": reply})
    save_memory(conversation_history)
