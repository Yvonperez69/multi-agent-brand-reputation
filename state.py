from typing_extensions import TypedDict

class State(TypedDict):
    brand: str
    analysis: str
    crisis: str
    report: str
    score: int
    raw_data: dict
    metrics: dict