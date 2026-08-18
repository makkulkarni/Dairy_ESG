"""
Metric Cards Component
Renders key performance indicators and target tracking badges.
"""

import streamlit as st


def render_baseline_metrics(baseline_data: dict):
    """
    Renders top-level baseline GHG emission metrics.
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Enterprise Footprint",
            value=f"{baseline_data['total_tco2e']:,.0f} tCO₂e",
            help="Annual total absolute greenhouse gas emissions across Scopes 1, 2, and 3."
        )
        
    with col2:
        st.metric(
            label="Baseline Carbon Intensity",
            value=f"{baseline_data['carbon_intensity_kg_co2e_per_kg_milk']:.3f} kg CO₂e",
            delta="Per kg Milk",
            delta_color="off"
        )
        
    with col3:
        st.metric(
            label="Upstream Scope 3 Share",
            value=f"{baseline_data['scope3_share_pct']:.1f}%",
            help="Percentage of emissions originating from smallholder farming and transport."
        )
        
    with col4:
        st.metric(
            label="Annual Raw Milk Processed",
            value=f"{baseline_data['annual_milk_kg'] / 1e6:,.1f}M kg",
            help="Total annual milk procurement volume in kilograms."
        )


def render_target_status(pct_achieved: float, target_pct: float):
    """
    Renders a status card indicating whether active levers meet the 2030 target.
    """
    if pct_achieved >= target_pct:
        st.success(
            f"🎯 **2030 Target Met!** Current interventions achieve a **{pct_achieved:.1f}%** reduction "
            f"(Target: {target_pct:.0f}%)."
        )
    else:
        gap = target_pct - pct_achieved
        st.warning(
            f"⚠️ **Target Shortfall:** Current interventions achieve a **{pct_achieved:.1f}%** reduction. "
            f"Additional **{gap:.1f}%** reduction required to meet the {target_pct:.0f}% 2030 goal."
        )