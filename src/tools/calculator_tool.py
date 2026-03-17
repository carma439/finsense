import numexpr as ne
from langchain.tools import tool
from src.logger import get_logger

logger = get_logger("calculator_tool")

@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    
    IMPORTANT:
    Do NOT use this tool for tax calculation, use tax_calculator for taxes.
    You must use this tool whenever a simple non-tax arithmetic calculation is required.
    Do NOT perform arithmetic yourself.
    Do NOT use this tool unless user has asked you to perform some
    calculation.
    
    Use this tool whenever the user asks for arithmetic
    operations like addition, subtraction, multiplication,
    division, percentage calculations, or differences.

    Input must be a valid mathematical expression in string format.
    """

    try:
        logger.info(f"Calculator called with expression: {expression}")
        
        result = ne.evaluate(str(expression))
        
        logger.info(f"Calculator result: {result.item()}")
        
        return str(result.item())
    except Exception as e:
        logger.error(f"Calculator error: {str(e)}")
        return f"Calculation error: {str(e)}"