"""
Scope 1, 2, and 3 GHG Accounting Core
Calculates baseline enterprise carbon intensity (kg CO2e / kg milk).
"""

from typing import Dict, Any


def calculate_baseline_emissions(
    daily_volume_liters: float,
    regional_data: list[Dict[str, Any]],
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Computes total annual emissions (tCO2e) and carbon intensity (kg CO2e / kg milk).
    """
    annual_volume_kg = daily_volume_liters * 365 * 1.03  # Milk density: ~1.03 kg/L
    
    # 1. Scope 1: Direct Diesel Generation & Thermal Fuel
    # ~0.005 L diesel per kg milk processed
    total_diesel_liters = annual_volume_kg * 0.005
    scope1_kg_co2e = total_diesel_liters * params["enterprise_defaults"]["diesel_emission_factor_kg_co2e_liter"]
    
    # 2. Scope 2: Purchased Electricity
    # ~0.04 kWh per kg milk processed
    total_kwh = annual_volume_kg * 0.04
    scope2_kg_co2e = total_kwh * params["enterprise_defaults"]["grid_emission_factor_kg_co2e_kwh"]
    
    # 3. Scope 3: Upstream Farm + Transport Logistics
    scope3_farm_kg_co2e = 0.0
    scope3_transport_kg_co2e = 0.0
    
    gwp_ch4 = params["ipcc_gwp_ar6"]["ch4_biogenic"]
    gwp_n2o = params["ipcc_gwp_ar6"]["n2o"]
    
    for zone in regional_data:
        zone_volume_kg = annual_volume_kg * (zone["share_pct"] / 100.0)
        
        # Sourcing Transport
        # Tone-km = (Volume in Metric Tons) * Distance (km)
        ton_km = (zone_volume_kg / 1000.0) * zone["avg_transport_km"]
        scope3_transport_kg_co2e += ton_km * params["enterprise_defaults"]["tanker_transit_factor_kg_co2e_tonkm"]
        
        # Farm Emissions (Weighted by herd composition)
        mix = {
            "crossbred_cow": zone["crossbred_share"],
            "buffalo": zone["buffalo_share"],
            "indigenous_cow": zone["indigenous_share"]
        }
        
        for animal_type, share in mix.items():
            if share <= 0:
                continue
            
            daily_yield = params["scope3_farm_baseline"]["average_milk_yield_liters_per_day"][animal_type]
            annual_animal_yield_kg = daily_yield * 365 * 1.03
            
            # Head count needed for zone share
            head_count = (zone_volume_kg * share) / annual_animal_yield_kg
            
            # Methane & Nitrous Oxide per head
            enteric_ch4 = params["scope3_farm_baseline"]["enteric_ch4_kg_per_head_yr"][animal_type] * head_count
            manure_ch4 = params["scope3_farm_baseline"]["manure_ch4_kg_per_head_yr"][animal_type] * head_count
            feed_n2o = params["scope3_farm_baseline"]["feed_n2o_kg_per_head_yr"][animal_type] * head_count
            
            animal_co2e = (enteric_ch4 + manure_ch4) * gwp_ch4 + (feed_n2o * gwp_n2o)
            scope3_farm_kg_co2e += animal_co2e

    scope3_total_kg_co2e = scope3_farm_kg_co2e + scope3_transport_kg_co2e
    total_emissions_kg_co2e = scope1_kg_co2e + scope2_kg_co2e + scope3_total_kg_co2e
    
    carbon_intensity = total_emissions_kg_co2e / annual_volume_kg
    
    return {
        "annual_milk_kg": annual_volume_kg,
        "scope1_tco2e": scope1_kg_co2e / 1000.0,
        "scope2_tco2e": scope2_kg_co2e / 1000.0,
        "scope3_tco2e": scope3_total_kg_co2e / 1000.0,
        "total_tco2e": total_emissions_kg_co2e / 1000.0,
        "carbon_intensity_kg_co2e_per_kg_milk": carbon_intensity,
        "scope3_share_pct": (scope3_total_kg_co2e / total_emissions_kg_co2e) * 100.0
    }