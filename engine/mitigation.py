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
    params: Dict[str, Any]
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
    
    # 1. Ration Balancing Savings (Applies to Scope 3 Enteric Portion ~75% of Scope 3)
    enteric_base_tco2e = scope3_tco2e * 0.75
    ration_abatement_tco2e = enteric_base_tco2e * (ration_balancing_pct * max_ration_eff)
    
    # 2. Solar BMCs Savings (Replaces Scope 2 Grid Electricity & Diesel BMC Generators ~60% of Scope 2)
    solar_abatement_tco2e = scope2_tco2e * 0.60 * solar_bmc_pct
    
    # 3. Manure Digesters Savings (Applies to Scope 3 Manure Portion ~15% of Scope 3)
    manure_base_tco2e = scope3_tco2e * 0.15
    digester_abatement_tco2e = manure_base_tco2e * (manure_digester_pct * max_digester_eff)
    
    # Total Abatement
    total_abatement_tco2e = ration_abatement_tco2e + solar_abatement_tco2e + digester_abatement_tco2e
    mitigated_total_tco2e = max(0.0, total_baseline_tco2e - total_abatement_tco2e)
    
    # New Carbon Intensity
    annual_milk_kg = baseline_results["annual_milk_kg"]
    new_intensity = (mitigated_total_tco2e * 1000.0) / annual_milk_kg
    
    pct_reduction_achieved = ((total_baseline_tco2e - mitigated_total_tco2e) / total_baseline_tco2e) * 100.0
    
    return {
        "ration_abatement_tco2e": ration_abatement_tco2e,
        "solar_abatement_tco2e": solar_abatement_tco2e,
        "digester_abatement_tco2e": digester_abatement_tco2e,
        "total_abatement_tco2e": total_abatement_tco2e,
        "mitigated_total_tco2e": mitigated_total_tco2e,
        "new_carbon_intensity": new_intensity,
        "pct_reduction_achieved": pct_reduction_achieved
    }