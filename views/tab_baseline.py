"""
Tab 1: Baseline GHG Footprint & Disclosures
"""

import streamlit as st
import pandas as pd
from components.metrics_cards import render_baseline_metrics
from components.charts import create_scope_donut_chart


def render_tab_baseline(baseline_data: dict, regional_df: pd.DataFrame):
    """
    Renders the Baseline GHG Footprint tab view.
    """
    st.subheader("📊 Enterprise Baseline Footprint (GHG Protocol Standards)")
    
    # 1. Metric Cards Row
    render_baseline_metrics(baseline_data)
    
    st.markdown("---")
    
    # 2. Charts and Data Breakdown Row
    col1, col2 = st.columns([5, 7])
    
    with col1:
        fig_donut = create_scope_donut_chart(baseline_data)
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col2:
        st.write("### Regional Procurement & Baseline Footprint")
        st.dataframe(
            regional_df[[
                "zone_name", 
                "share_pct", 
                "baseline_intensity_kg_co2e_kg_milk", 
                "avg_transport_km"
            ]].rename(columns={
                "zone_name": "Procurement Zone",
                "share_pct": "Procurement Share (%)",
                "baseline_intensity_kg_co2e_kg_milk": "Intensity (kg CO₂e/kg)",
                "avg_transport_km": "Avg Transit Distance (km)"
            }),
            use_container_width=True,
            hide_index=True
        )
        
        with st.expander("ℹ️ **Accounting Methodological Notes**"):
            st.markdown(
                """
                * **Scope 1:** Includes direct stationary diesel generator combustion and thermal process heating.
                * **Scope 2:** Calculated using location-based grid emission factors per state grid mix.
                * **Scope 3:** Follows IPCC Tier 1/2 livestock emissions methodologies for biogenic methane ($CH_4$) and nitrous oxide ($N_2O$).
                """
            )