import json
from typing import Any, Dict, List
import requests
from agents.agent_interface import AgentInterface
from agents.utils import get_chatbot_response

class ClassificationAgent(AgentInterface):
    
    def __init__(self, model_name: str):
        self.session = requests.Session()
        self.model_name = model_name

    def get_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        system_prompt = """
        You are a helpful AI assistant for a small restaurant application that serves food.
        Your task is to determine what agent should handle the user request. You have three agents to choose from:
        1. details_agent: This agent is responsible for answeting questions about the restaurant, like location, working hours, details about the menu items, the menu itself, or what we have and also information about out ai assistant,  
        2. order_agent: This agent is responsible for taking orders from the user. It's responsible to have a conversation with the user about the order untill it's complete.
        3. other_agent: This agent is responsible for handle user requests that doesn't fit in the previous agents.

        
        Ensure your output strictly follows this rules:
        1. You must ensure it's a well structured JSON output.
        2. You must ensure it's a valid JSON output.
        3. You are not allowed to write escape characters for single quoted strings in the JSON output.
        4. You are not alloed to write anithing else but the JSON format bellow.
        5. You must ensure the output follows the JSON structured shown bellow.

        {
            "chain_of_thought": Go over each of the agents above and write your thoughts about what agent should handle the user request,
            "selected_agent": Use the chain_of_thought points to select the correct agent `details_agent` or `order_agent` or `other_agent`. You can only pick one agent,
        }
        """

        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]

        response = get_chatbot_response(
            self.session,
            self.model_name,
            input_messages
        )
        print(response["message"]["content"])
        output = json.loads(response["message"]["content"])
        return output
