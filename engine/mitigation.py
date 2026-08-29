"""
Decarbonization Lever Abatement Engine
Calculates carbon savings from active intervention sliders.
"""

from typing import Dict, Any


def apply_mitigation_levers(
    baseline_results: Dict[str, Any],
    ration_balancing_pct: float,  # 0.0 to 1.0
    solar_bmc_pct: float,         # 0.0 to 1.0
    manure_digester_pct: float,   # 0.0 to 1.0
    params: Dict[str, Any],
    genetics_health_pct: float = 0.0  # 0.0 to 1.0
) -> Dict[str, Any]:
    """
    Simulates cumulative emission reductions based on active adoption percentages.
    """
    total_baseline_tco2e = baseline_results["total_tco2e"]
    scope3_tco2e = baseline_results["scope3_tco2e"]
    scope2_tco2e = baseline_results["scope2_tco2e"]
    
    # Max reduction potentials from configuration
    max_ration_eff = params["mitigation_max_efficiencies"]["ration_balancing_max_enteric_reduction"]
    max_digester_eff = params["mitigation_max_efficiencies"]["manure_digester_max_methane_capture"]
    max_genetics_eff = params["mitigation_max_efficiencies"].get(
        "herd_health_genetics_max_abatement", 0.08
    )
    max_yield_improvement = params["mitigation_max_efficiencies"].get(
        "ration_balancing_max_yield_improvement", 0.35
    )
    
    # 1. Ration Balancing Savings (Applies to Scope 3 Enteric Portion ~75% of Scope 3)
    enteric_base_tco2e = scope3_tco2e * 0.75

    # Ration balancing lowers methane per animal and raises yield per animal.
    # The latter reduces the herd required for the fixed enterprise milk volume.
    baseline_yield = baseline_results.get("average_daily_yield_liters", 0.0)
    yield_improvement = ration_balancing_pct * max_yield_improvement
    herd_reduction = yield_improvement / (1.0 + yield_improvement) if baseline_yield else 0.0
    direct_enteric_reduction = ration_balancing_pct * max_ration_eff
    combined_enteric_reduction = 1.0 - (
        (1.0 - direct_enteric_reduction) * (1.0 - herd_reduction)
    )
    ration_abatement_tco2e = enteric_base_tco2e * combined_enteric_reduction
    improved_daily_yield = baseline_yield * (1.0 + yield_improvement)
    baseline_herd = baseline_results.get("baseline_active_herd_count", 0.0)
    mitigated_herd = baseline_herd * (1.0 - herd_reduction)
    
    # 2. Solar BMCs Savings (Replaces Scope 2 Grid Electricity & Diesel BMC Generators ~60% of Scope 2)
    solar_abatement_tco2e = scope2_tco2e * 0.60 * solar_bmc_pct
    
    # 3. Manure Digesters Savings (Applies to Scope 3 Manure Portion ~15% of Scope 3)
    manure_base_tco2e = scope3_tco2e * 0.15
    digester_abatement_tco2e = manure_base_tco2e * (manure_digester_pct * max_digester_eff)

    # Herd health/genetics improves productivity and reduces residual herd emissions.
    genetics_abatement_tco2e = total_baseline_tco2e * (genetics_health_pct * max_genetics_eff)
    
    # Total Abatement
    total_abatement_tco2e = (
        ration_abatement_tco2e
        + solar_abatement_tco2e
        + digester_abatement_tco2e
        + genetics_abatement_tco2e
    )
    mitigated_total_tco2e = max(0.0, total_baseline_tco2e - total_abatement_tco2e)
    
    # New Carbon Intensity
    annual_milk_kg = baseline_results["annual_milk_kg"]
    new_intensity = (mitigated_total_tco2e * 1000.0) / annual_milk_kg
    
    pct_reduction_achieved = ((total_baseline_tco2e - mitigated_total_tco2e) / total_baseline_tco2e) * 100.0
    
    return {
        "ration_abatement_tco2e": ration_abatement_tco2e,
        "solar_abatement_tco2e": solar_abatement_tco2e,
        "digester_abatement_tco2e": digester_abatement_tco2e,
        "genetics_health_abatement_tco2e": genetics_abatement_tco2e,
        "baseline_active_herd_count": baseline_herd,
        "mitigated_active_herd_count": mitigated_herd,
        "improved_daily_yield_liters": improved_daily_yield,
        "total_abatement_tco2e": total_abatement_tco2e,
        "mitigated_total_tco2e": mitigated_total_tco2e,
        "new_carbon_intensity": new_intensity,
        "pct_reduction_achieved": pct_reduction_achieved
    }
