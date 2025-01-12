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
        You are a helpful AI assistant for a small restaurant application which serves food.
        Your task is to determine whether the user is asking something relevant to the restaurant or not. In order to classify correctly the user request, you have to take into account the last message from the user.
        
        The user is allowed to:
        1. Ask questions about the restaurant, like menu items and retaurant related questions.
        2. Ask questions about menu items, they can ask for the description or ingredients of the dishes.
        3. Ask questions about you, like who are you, who's your creator or which are your capabilities and purpose related to the restaurant.
        
        The user is NOT allowed to:
        1. Ask questions about anything else other than our restaurant.
        2. Ask questions about the staff or how to make the menu items.

        Your output should be in a structured json format like the following. Your are not allowed to output anything else than the structured json.
        {
            "chain_of_thought": Go over each of the points above and make see if the message lies under this point or not. Write in a list form all your thoughts about the user request. Your not allowd to write anithing else than your thoughts in a string format. 
            "allowed": `true` or `false`. Pick only one of those.
            "message": Leave this property empty if it's allowed, otherwise write the reason why it's not allowed.
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