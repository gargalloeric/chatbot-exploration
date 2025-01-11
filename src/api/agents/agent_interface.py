from typing import List, Dict, Any
from abc import ABC, abstractmethod

class AgentInterface(ABC):
    @abstractmethod
    def get_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass