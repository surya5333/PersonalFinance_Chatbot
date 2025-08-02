from typing import Dict, Any, Tuple

# Tax slabs for old regime (FY 2023-24)
OLD_REGIME_SLABS = [
    (0, 250000, 0),           # 0% for income up to 2.5L
    (250001, 500000, 0.05),   # 5% for income between 2.5L and 5L
    (500001, 1000000, 0.20),  # 20% for income between 5L and 10L
    (1000001, float('inf'), 0.30)  # 30% for income above 10L
]

# Tax slabs for new regime (FY 2023-24)
NEW_REGIME_SLABS = [
    (0, 300000, 0),           # 0% for income up to 3L
    (300001, 600000, 0.05),   # 5% for income between 3L and 6L
    (600001, 900000, 0.10),   # 10% for income between 6L and 9L
    (900001, 1200000, 0.15),  # 15% for income between 9L and 12L
    (1200001, 1500000, 0.20), # 20% for income between 12L and 15L
    (1500001, float('inf'), 0.30)  # 30% for income above 15L
]

# Standard deduction amount
STANDARD_DEDUCTION = 50000

def calculate_tax(income: float, regime: str = "new") -> float:
    """Calculate income tax based on income and tax regime"""
    # Apply standard deduction
    taxable_income = max(0, income - STANDARD_DEDUCTION)
    
    # Select tax slabs based on regime
    slabs = NEW_REGIME_SLABS if regime.lower() == "new" else OLD_REGIME_SLABS
    
    # Calculate tax
    tax = 0
    for lower_limit, upper_limit, rate in slabs:
        if taxable_income > lower_limit:
            taxable_in_bracket = min(taxable_income, upper_limit) - lower_limit
            tax += taxable_in_bracket * rate
    
    # Add cess (4% of tax)
    tax += tax * 0.04
    
    return round(tax, 2)

def compare_tax_regimes(income: float) -> Dict[str, Any]:
    """Compare tax under old and new regimes"""
    old_regime_tax = calculate_tax(income, "old")
    new_regime_tax = calculate_tax(income, "new")
    
    difference = abs(old_regime_tax - new_regime_tax)
    better_regime = "old" if old_regime_tax < new_regime_tax else "new"
    savings = difference
    
    return {
        "old_regime_tax": old_regime_tax,
        "new_regime_tax": new_regime_tax,
        "difference": difference,
        "better_regime": better_regime,
        "savings": savings,
        "visualization_data": {
            "labels": ["Old Regime", "New Regime"],
            "values": [old_regime_tax, new_regime_tax]
        }
    }

def calculate_hra_exemption(hra_received: float, city_tier: int, rent_paid: float = 0, basic_salary: float = 0) -> Dict[str, float]:
    """Calculate HRA exemption based on city tier"""
    # If rent paid or basic salary is not provided, make assumptions
    if rent_paid == 0:
        # Assume rent paid is 40% of HRA received for Tier 1, 30% for Tier 2, 20% for Tier 3
        rent_multiplier = 0.4 if city_tier == 1 else (0.3 if city_tier == 2 else 0.2)
        rent_paid = hra_received * rent_multiplier * 12  # Annual rent
    
    if basic_salary == 0:
        # Assume basic salary is 2.5 times HRA received
        basic_salary = hra_received * 2.5
    
    # Calculate HRA exemption based on the minimum of:
    # 1. Actual HRA received
    # 2. Rent paid - 10% of basic salary
    # 3. 50% of basic salary for metro cities (Tier 1), 40% for non-metro cities (Tier 2, 3)
    
    exemption_1 = hra_received
    exemption_2 = max(0, rent_paid - (0.1 * basic_salary))
    exemption_3 = basic_salary * (0.5 if city_tier == 1 else 0.4)
    
    exemption = min(exemption_1, exemption_2, exemption_3)
    
    return {
        "hra_received": hra_received,
        "rent_paid": rent_paid,
        "basic_salary": basic_salary,
        "exemption_amount": round(exemption, 2),
        "city_tier": city_tier
    }