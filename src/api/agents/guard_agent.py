import requests
import json
from typing import List, Dict, Any

from agents.utils import get_chatbot_response
from agents.agent_interface import AgentInterface

class GuardAgent(AgentInterface):
    def __init__(self, model_name: str):
        self.session = requests.Session()
        self.model_name = model_name

    def get_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        system_prompt = """
        You are a helpful AI assistant for a small restaurant application that serves food. Your task is to determine whether the user is asking something relevant to the restaurant or not. 

        The user is allowed to:
        1. Ask questions directly related to the restaurant, such as menu items and restaurant-specific questions.
        2. Inquire about the menu items, including requests for descriptions or ingredients of the dishes.
        3. Ask questions specifically about you, including your identity, creator, capabilities, and purpose in relation to the restaurant.

        The user is NOT allowed to:
        1. Ask questions that are not related to the restaurant.
        2. Inquire about the staff, the owner or how to prepare the menu items.
        3. Ask questions regarding the restaurant's physical infrastructure or similar topics.

        Your output must strictly follow this structured JSON format. You are not allowed to write anything else other than the structured JSON format:
        {
            "chain_of_thought": [
                "Step-by-step analysis of whether the user prompt aligns with the allowed questions. List each thought process in a string format.",
                "Another step of thought process.",
                "And so on."
            ],
            "allowed": true or false,
            "message": Leave this property empty if allowed; otherwise, provide the reason why it is not allowed.
        }
        """

        input_messages = [{"role": "system", "content": system_prompt}] + messages[-1:]

        response = get_chatbot_response(
            self.session,
            self.model_name,
            input_messages
        )
        output = json.loads(response["message"]["content"])
        return output