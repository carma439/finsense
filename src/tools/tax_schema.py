from pydantic import BaseModel, Field
from typing import Optional, Literal


class TaxCalculationInput(BaseModel):

    income: int = Field(
            description="Annual taxable income in INR"
    )

    assessee_type: Literal["Individual", "HUF", "AOPs/BOI",
                    "Domestic Company", "Firms", "LLP",
                    "Foreign Company", "Co-operative Society"] = Field(
        default="Individual",
        description="Type of taxpayer such as Individual, HUF, Company ..."
    )

    financial_year: Literal['2026-27', '2025-26', '2024-25',
                    '2023-24', '2022-23', '2021-22'] = Field(
        default="2025-26",
        description="Financial year for tax calculation"
    )

    old_regime: Literal["Yes", "No"] = Field(
        default="No",
        description="Whether using old tax regime or not. Yes means choosing old regime and No means choosing new regime."
    )

    age_category: Optional[
        Literal["Less than 60 years", 
        "Equal to 60 years or more but less than 80 years",
        "Equal to 80 years or more"]] = Field(
        default="Less than 60 years",
        description="Age category if assessee type is Individual"
    )

    resident_status: Optional[Literal[
        "Resident", "Non-Resident"]] = Field(
        default="Resident",
        description="Residential status if assessee type is Individual"
    )