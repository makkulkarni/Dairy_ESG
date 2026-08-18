"""
IPCC Climate Risk & THI Yield Penalty Engine
Models heat stress effects and re-evaluates upstream carbon intensity escalation.
"""

from typing import Dict, Any


def stress_test_climate_risk(
    baseline_results: Dict[str, Any],
    scenario_data: Dict[str, Any],
    regional_data: list[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Evaluates THI heat stress yield penalties and calculates compensating herd growth.
    """
    yield_loss_crossbred = scenario_data["crossbred_yield_loss_pct"] / 100.0
    yield_loss_buffalo = scenario_data["buffalo_yield_loss_pct"] / 100.0
    
    # Weighted average yield loss based on average enterprise herd mix
    total_crossbred_share = sum(z["crossbred_share"] * z["share_pct"] for z in regional_data) / 100.0
    total_buffalo_share = sum(z["buffalo_share"] * z["share_pct"] for z in regional_data) / 100.0
    
    weighted_yield_loss = (
        (yield_loss_crossbred * total_crossbred_share) +
        (yield_loss_buffalo * total_buffalo_share)
    )
    
    # Herd expansion penalty required to maintain constant milk volume output
    # Extra Herd % = Yield Loss / (1 - Yield Loss)
    if weighted_yield_loss < 1.0:
        herd_expansion_penalty_pct = (weighted_yield_loss / (1.0 - weighted_yield_loss)) * 100.0
    else:
        herd_expansion_penalty_pct = 0.0
        
    # Carbon intensity escalation (Scope 3 farm emissions increase directly with herd growth)
    baseline_scope3 = baseline_results["scope3_tco2e"]
    escalated_scope3 = baseline_scope3 * (1.0 + (herd_expansion_penalty_pct / 100.0))
    
    escalated_total_tco2e = (
        baseline_results["scope1_tco2e"] + 
        baseline_results["scope2_tco2e"] + 
        escalated_scope3
    )
    
    escalated_intensity = (escalated_total_tco2e * 1000.0) / baseline_results["annual_milk_kg"]
    intensity_increase_pct = ((escalated_intensity - baseline_results["carbon_intensity_kg_co2e_per_kg_milk"]) / baseline_results["carbon_intensity_kg_co2e_per_kg_milk"]) * 100.0
    
    return {
        "scenario_code": scenario_data["scenario_code"],
        "scenario_name": scenario_data["scenario_name"],
        "avg_summer_thi": scenario_data["avg_summer_thi"],
        "weighted_yield_loss_pct": weighted_yield_loss * 100.0,
        "herd_expansion_penalty_pct": herd_expansion_penalty_pct,
        "escalated_total_tco2e": escalated_total_tco2e,
        "escalated_intensity": escalated_intensity,
        "intensity_increase_pct": intensity_increase_pct
    }