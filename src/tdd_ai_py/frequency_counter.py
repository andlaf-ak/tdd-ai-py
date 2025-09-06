from collections import Counter
from typing import Dict


def create_frequency_map(text: str) -> Dict[str, int]:
    return dict(Counter(text))
