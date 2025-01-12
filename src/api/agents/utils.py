import requests
import json

# Ollama constants
OLLAMA_CHATBOT_URL="http://localhost:11434/api/chat"
OLLAMA_EMBEDDING_URL="http://localhost:11434/api/embed"

def get_chatbot_response(session: requests.Session , model_name: str, messages, temperature: float = 0.0):
    response = session.post(
        OLLAMA_CHATBOT_URL,
        data=json.dumps({
            "model": model_name,
            "messages": messages,
            "options": {
                "temperature": temperature,
                "top_p": 0.8
            },
            "stream": False
        })
    )
    return response.json()

def get_embedding(session: requests.Session, model_name: str, text_input):
    response = session.post(
        OLLAMA_EMBEDDING_URL,
        data=json.dumps({
            "model": model_name,
            "input": text_input
        })
    )
    return response.json()