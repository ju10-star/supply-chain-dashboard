import pandas as pd
from src.supply_chain_dashboard.kpi_calculator import scrap_calculate, scrap_per_product_calculate

def test_scrap_calculate_simple():
    df = pd.DataFrame({
        "producto": ["A","B"],
        "fabricados": [100, 200],
        "scrap": [5, 10]
    })
    assert abs(scrap_calculate(df) - (15/300)) < 1e-9

def test_scrap_per_product_calculate_zero():
    df = pd.DataFrame({
        "producto": ["A","B"],
        "fabricados": [0, 50],
        "scrap": [0, 5]
    })
    result = dict(scrap_per_product_calculate(df))
    assert result["A"] == 0.0
    assert abs(result["B"] - (5/50)) < 1e-9