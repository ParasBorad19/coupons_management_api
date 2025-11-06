from abc import ABC, abstractmethod
from typing import Dict

class CouponStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, details: Dict, cart: Dict) -> float:
        ...
