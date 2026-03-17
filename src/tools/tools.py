from langchain_core.tools.structured import StructuredTool
from src.tools.tax_schema import TaxCalculationInput
from src.tools.tax_tool import calculate_tax_online
from src.tools.rag_tool import rag_search
from src.tools.calculator_tool import calculator

tax_calculator_tool = StructuredTool.from_function(
    func=calculate_tax_online,
    name="tax_calculator",
    description="""Calculate income tax using the official government tax calculator.

    This tool must be used whenever tax values are required.
    Never estimate tax yourself or through any other tool.

    Input:
    annual income in INR.

    Output:
    tax payable.""",
    args_schema=TaxCalculationInput
)

rag_tool = rag_search

calculator_tool = calculator

tool_list = [rag_tool, tax_calculator_tool, calculator_tool]