from dataclasses import dataclass
from typing import Optional

@dataclass
class Cost:
    label: str
    amount: float
    category: str = "general"
    date: Optional[str] = None
    id: Optional[int] = None

    def __str__(self):
        return f"[{self.id}] {self.date} | {self.label} | {self.amount}€ | {self.category}"