"""
Unit Tests for engine/mitigation.py and engine/climate_risk.py
"""

import json
import pytest
import pandas as pd
from engine.carbon_math import calculate_baseline_emissions
from engine.mitigation import apply_mitigation_levers
from engine.climate_risk import stress_test_climate_risk


@pytest.fixture
def setup_engine_data():
    """Sets up baseline results and data fixtures for testing."""
    with open("data/config/baseline_params.json", "r") as f:
        params = json.load(f)
    
    regional_df = pd.read_csv("data/raw/regional_zones.csv")
    regional_data = regional_df.to_dict(orient="records")
    scenarios_df = pd.read_csv("data/raw/climate_scenarios.csv")
    
    baseline_results = calculate_baseline_emissions(20_000_000, regional_data, params)
    return params, regional_data, scenarios_df, baseline_results


def test_mitigation_levers_zero_adoption(setup_engine_data):
    """When all sliders are 0%, total abatement should be 0 tCO2e."""
    params, _, _, baseline_results = setup_engine_data
    
    mitigation = apply_mitigation_levers(
        baseline_results=baseline_results,
        ration_balancing_pct=0.0,
        solar_bmc_pct=0.0,
        manure_digester_pct=0.0,
        params=params
    )
    
    assert mitigation["total_abatement_tco2e"] == 0.0
    assert mitigation["pct_reduction_achieved"] == 0.0


def test_mitigation_levers_reduction(setup_engine_data):
    """Full adoption of levers should successfully reduce emissions and new intensity."""
    params, _, _, baseline_results = setup_engine_data
    
    mitigation = apply_mitigation_levers(
        baseline_results=baseline_results,
        ration_balancing_pct=1.0,
        solar_bmc_pct=1.0,
        manure_digester_pct=1.0,
        params=params
    )
    
    assert mitigation["total_abatement_tco2e"] > 0.0
    assert mitigation["new_carbon_intensity"] < baseline_results["carbon_intensity_kg_co2e_per_kg_milk"]


def test_climate_risk_escalation(setup_engine_data):
    """Extreme heat scenario (SSP5-8.5) should escalate carbon intensity due to yield loss penalties."""
    _, regional_data, scenarios_df, baseline_results = setup_engine_data
    
    ssp585_row = scenarios_df.loc[scenarios_df["scenario_code"] == "ssp5_85"].iloc[0].to_dict()
    
    risk_results = stress_test_climate_risk(
        baseline_results=baseline_results,
        scenario_data=ssp585_row,
        regional_data=regional_data
    )
    
    assert risk_results["herd_expansion_penalty_pct"] > 0.0
    assert risk_results["escalated_intensity"] > baseline_results["carbon_intensity_kg_co2e_per_kg_milk"]