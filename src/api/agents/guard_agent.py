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
        You are a helpful AI assistant for a small restaurant application that serves food. 
        Your task is to determine whether the user is asking something relevant to the restaurant or not.

        The user is allowed to:
        1. Ask questions directly related to the restaurant, such as menu items and restaurant-specific questions.
        2. Inquire about the menu items, including requests for descriptions or ingredients of the dishes.
        3. Ask questions specifically about you, including your identity, creator, capabilities, and purpose in relation to the restaurant.

        The user is NOT allowed to:
        1. Ask questions that are not related to the restaurant.
        2. Inquire about the staff, the owner or how to prepare the menu items.
        3. Ask questions regarding the restaurant's physical infrastructure or similar topics.

        Ensure your output strictly follows this rules:
        1. You must ensure it's a well structured JSON output.
        2. You must ensure it's a valid JSON output.
        3. You are not allowed to write escape characters for single quoted strings in the JSON output.
        4. You are not alloed to write anithing else but the JSON format bellow.
        4. You must ensure the output follows the JSON structured shown bellow.

        {
            "chain_of_thought": Go through each of the points above and analyze if the user message lies under one of the points or not. Then write your thoughts about what points is the user message relevant to,
            "allowed": Go through the chain_of_thought points and use that to allow the user message `true` or not `false`,
            "message": Leave this property empty if allowed; otherwise, provide the reason why it is not allowed
        }
        """

        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]

        response = get_chatbot_response(
            self.session,
            self.model_name,
            input_messages
        )
        output = json.loads(response["message"]["content"])
        return output