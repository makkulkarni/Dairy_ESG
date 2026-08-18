"""
Tab 3: IPCC Climate Stress-Test & Regional Sourcing
"""

import streamlit as st
import pandas as pd
from engine.climate_risk import stress_test_climate_risk
from components.charts import create_climate_risk_chart


def render_tab_climate_risk(baseline_data: dict, scenarios_df: pd.DataFrame, regional_data: list):
    """
    Renders the IPCC Climate Stress-Test tab view.
    """
    st.subheader("☀️ IPCC Physical Climate Risk & Heat Stress Simulator")
    
    col1, col2 = st.columns([5, 7])
    
    with col1:
        st.write("### Select Climate Scenario")
        
        selected_scenario_code = st.selectbox(
            "IPCC Shared Socioeconomic Pathway (SSP)",
            options=scenarios_df["scenario_code"].tolist(),
            format_func=lambda x: scenarios_df.loc[scenarios_df["scenario_code"] == x, "scenario_name"].values[0]
        )
        
        scenario_row = scenarios_df.loc[scenarios_df["scenario_code"] == selected_scenario_code].iloc[0].to_dict()
        
        # Run Stress Test Computation
        risk_results = stress_test_climate_risk(
            baseline_results=baseline_data,
            scenario_data=scenario_row,
            regional_data=regional_data
        )
        
        st.info(
            f"**Scenario Specs:** Under **{risk_results['scenario_name']}**, summer Temperature-Humidity "
            f"Index (THI) reaches **{risk_results['avg_summer_thi']}**, causing heat stress yield loss."
        )
        
    with col2:
        fig_climate = create_climate_risk_chart(scenarios_df, selected_scenario_code)
        st.plotly_chart(fig_climate, use_container_width=True)
        
    st.markdown("---")
    
    # Stress-Test Output Metrics
    st.write("### Climate Risk Impact Metrics")
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric("Average Yield Penalty", f"{risk_results['weighted_yield_loss_pct']:.1f}%")
    m2.metric("Herd Expansion Required", f"+{risk_results['herd_expansion_penalty_pct']:.1f}%")
    m3.metric("Escalated Intensity", f"{risk_results['escalated_intensity']:.3f} kg CO₂e")
    m4.metric("Intensity Escalation", f"+{risk_results['intensity_increase_pct']:.1f}%", delta_color="inverse")