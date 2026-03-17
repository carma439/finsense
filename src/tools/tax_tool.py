from playwright.sync_api import sync_playwright
from typing import Optional, Literal
from pydantic import Field
from src.logger import get_logger

logger = get_logger("tax_tool")

def calculate_tax_online(income: int = Field(
            description="Annual taxable income in INR"
    ),

    assessee_type: Literal["Individual", "HUF", "AOPs/BOI",
                    "Domestic Company", "Firms", "LLP",
                    "Foreign Company", "Co-operative Society"] = Field(
        default="Individual",
        description="Type of taxpayer such as Individual, HUF, Company ..."
    ),

    financial_year: Literal['2026-27', '2025-26', '2024-25',
                    '2023-24', '2022-23', '2021-22'] = Field(
        default="2025-26",
        description="Financial year for tax calculation"
    ),

    old_regime: Literal["Yes", "No"] = Field(
        default="No",
        description="Whether using old tax regime or not. Yes means choosing old regime and No means choosing new regime."
    ),

    age_category: Optional[
        Literal["Less than 60 years", 
        "Equal to 60 years or more but less than 80 years",
        "Equal to 80 years or more"]] = Field(
        default="Less than 60 years",
        description="Age category if assessee type is Individual"
    ),

    resident_status: Optional[Literal[
        "Resident", "Non-Resident"]] = Field(
        default="Resident",
        description="Residential status if assessee type is Individual"
    )) -> str:

    """Tax calculator tool to calculate tax."""
    
    logger.info(f"tax_calculator tool called")
    
    browser = None
    
    try: 
        with sync_playwright() as p:
            
            logger.info("Launching Playwright browser")
            
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    # "--disable-dev-shm-usage",
                    # "--disable-gpu",
                    # "--no-zygote",
                    # "--disable-setuid-sandbox"
                ],
                timeout=30000   # 30 seconds
            )
            
            logger.info("Browser launched")
            
            page = browser.new_page()

            page.goto(
                "https://incometaxindia.gov.in/Pages/tools/tax-calculator.aspx"
            , timeout=30000)

            logger.info(
                "Using params: income=%s, year=%s, type=%s, regime=%s, age=%s, resident=%s",
                income, financial_year, assessee_type, old_regime, age_category, resident_status
            )
            
            year_id = "#ctl00_SPWebPartManager1_g_0a7fb9b8_bcbb_4a46_a0d0_fbb3d804d05e_cbassyear"
            type_id = "#ctl00_SPWebPartManager1_g_0a7fb9b8_bcbb_4a46_a0d0_fbb3d804d05e_cbasstype"
            regime_id = "#ctl00_SPWebPartManager1_g_0a7fb9b8_bcbb_4a46_a0d0_fbb3d804d05e_ddlbac115"
            
            income_id = "#ctl00_SPWebPartManager1_g_0a7fb9b8_bcbb_4a46_a0d0_fbb3d804d05e_txtNetIncome"
            tax_id = "ctl00_SPWebPartManager1_g_0a7fb9b8_bcbb_4a46_a0d0_fbb3d804d05e_txttotaltax"

            page.select_option(year_id, financial_year)
            page.select_option(type_id, assessee_type)
            page.select_option(regime_id, old_regime)

            if assessee_type == "Individual":
                age_id = "#ctl00_SPWebPartManager1_g_0a7fb9b8_bcbb_4a46_a0d0_fbb3d804d05e_cmbasscategory"
                resident_id = "#ctl00_SPWebPartManager1_g_0a7fb9b8_bcbb_4a46_a0d0_fbb3d804d05e_cmbresistatus"
                page.select_option(age_id, age_category)
                page.select_option(resident_id, resident_status)

            page.fill(income_id, str(income))

            page.click("body")

            tax = page.input_value(f"input[id*={tax_id}]")
            
            logger.info("Tax tool returned tax value = %s ", tax)
            
            browser.close()
            
            return tax
        
    except Exception as e:
        logger.error(f"Tax tool failed: {e}")
        return "Tax calculation service is currently unavailable. Please try later."
