"""
Tab 2: Decarbonization Lever Simulator
"""

import streamlit as st
from engine.mitigation import apply_mitigation_levers
from components.metrics_cards import render_target_status
from components.charts import create_abatement_waterfall


def render_tab_mitigation(baseline_data: dict, params: dict, target_pct: float):
    """
    Renders the Decarbonization Lever Simulator tab view.
    """
    st.subheader("🌱 Multi-Lever Decarbonization Simulator")
    st.write("Adjust operational adoption sliders to model decarbonization pathways toward the 2030 target.")
    
    col1, col2 = st.columns([5, 7])
    
    with col1:
        st.write("### Intervention Levers")
        
        ration_pct = st.slider(
            "Ration Balancing & Additives Adoption (%)",
            min_value=0,
            max_value=100,
            value=40,
            step=5,
            help="Reduces enteric fermentation methane emissions by optimizing dietary fiber and nitrogen ratios."
        ) / 100.0
        
        solar_pct = st.slider(
            "Village BMC Solarization (%)",
            min_value=0,
            max_value=100,
            value=60,
            step=5,
            help="Replaces diesel backup generators and grid electricity at rural Bulk Milk Cooling units with solar PV."
        ) / 100.0
        
        digester_pct = st.slider(
            "Community Manure Digesters (%)",
            min_value=0,
            max_value=100,
            value=25,
            step=5,
            help="Captures biogenic methane from manure storage for biogas utilization."
        ) / 100.0
        
        # Calculate Abatement Results
        mitigation_results = apply_mitigation_levers(
            baseline_results=baseline_data,
            ration_balancing_pct=ration_pct,
            solar_bmc_pct=solar_pct,
            manure_digester_pct=digester_pct,
            params=params
        )
        
    with col2:
        # Target Tracker Status Banner
        render_target_status(
            pct_achieved=mitigation_results["pct_reduction_achieved"],
            target_pct=target_pct
        )
        
        # Waterfall Chart
        fig_waterfall = create_abatement_waterfall(baseline_data["total_tco2e"], mitigation_results)
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
    st.markdown("---")
    
    # Impact Summary Table
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Abated Carbon Volume", f"{mitigation_results['total_abatement_tco2e']:,.0f} tCO₂e/yr")
    res_col2.metric("New Carbon Intensity", f"{mitigation_results['new_carbon_intensity']:.3f} kg CO₂e/kg")
    res_col3.metric("Net Intensity Reduction", f"-{mitigation_results['pct_reduction_achieved']:.1f}%")