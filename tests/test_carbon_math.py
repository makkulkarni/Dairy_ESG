"""
Unit Tests for engine/carbon_math.py
"""

import json
import pytest
import pandas as pd
from engine.carbon_math import calculate_baseline_emissions


@pytest.fixture
def mock_params_and_regional():
    """Loads baseline configuration and regional data for testing."""
    with open("data/config/baseline_params.json", "r") as f:
        params = json.load(f)
    
    regional_df = pd.read_csv("data/raw/regional_zones.csv")
    regional_data = regional_df.to_dict(orient="records")
    
    return params, regional_data


def test_calculate_baseline_emissions_structure(mock_params_and_regional):
    """Verifies that all expected keys exist in the calculation output."""
    params, regional_data = mock_params_and_regional
    daily_volume = 20_000_000  # 20M Liters/day
    
    results = calculate_baseline_emissions(daily_volume, regional_data, params)
    
    expected_keys = [
        "annual_milk_kg",
        "scope1_tco2e",
        "scope2_tco2e",
        "scope3_tco2e",
        "total_tco2e",
        "carbon_intensity_kg_co2e_per_kg_milk",
        "scope3_share_pct"
    ]
    for key in expected_keys:
        assert key in results, f"Missing expected key: {key}"


def test_baseline_intensity_range(mock_params_and_regional):
    """Ensures calculated baseline carbon intensity falls within typical dairy ranges (1.5 - 3.0 kg CO2e / kg milk)."""
    params, regional_data = mock_params_and_regional
    daily_volume = 20_000_000
    
    results = calculate_baseline_emissions(daily_volume, regional_data, params)
    intensity = results["carbon_intensity_kg_co2e_per_kg_milk"]
    
    assert 1.5 <= intensity <= 3.0, f"Unusual carbon intensity calculated: {intensity:.2f}"


def test_scope3_dominance(mock_params_and_regional):
    """Confirms Scope 3 emissions account for the vast majority (>70%) of total emissions."""
    params, regional_data = mock_params_and_regional
    daily_volume = 20_000_000
    
    results = calculate_baseline_emissions(daily_volume, regional_data, params)
    
    assert results["scope3_share_pct"] > 70.0, "Scope 3 share should be greater than 70%"