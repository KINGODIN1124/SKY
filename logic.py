# modules/logic.py
import math

def solve_expression(expr: str):
    """
    Solves arithmetic expressions safely, including large numbers, complex operations, and scientific functions.
    Examples: '2 + 3 * 5', '123456789 * 987654321', 'math.sin(1.57)', '2 ** 10'
    """
    try:
        # Allow numbers, operators, spaces, letters for math functions, and **
        allowed = "0123456789+-*%/(). abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if any(c not in allowed for c in expr):
            return "I can only solve basic arithmetic and scientific expressions."
        # Clean the expression: remove 'what is' prefix if present, but only if it's arithmetic
        if expr.lower().startswith("what is"):
            expr = expr[7:].strip()
        # Use eval with limited globals: no builtins, but allow math module
        result = eval(expr, {"__builtins__": None, "math": math}, {})
        return str(result)
    except Exception as e:
        return f"Error solving expression: {e}"

def logical_puzzle(question: str):
    """
    Simple pattern-based reasoning for logic puzzles
    """
    # Add your puzzle rules here
    if "even" in question and "number" in question:
        return "An even number is divisible by 2."
    if "odd" in question and "number" in question:
        return "An odd number is not divisible by 2."
    return "Let me think… I need more info to solve that."
