from .models import CalculationType

def compute(a: float, b: float, op: CalculationType) -> float:
    if op == CalculationType.add:
        return a + b
    if op == CalculationType.sub:
        return a - b
    if op == CalculationType.multiply:
        return a * b
    if op == CalculationType.divide:
        return a / b
    raise ValueError(f"Unsupported calculation type: {op}")
