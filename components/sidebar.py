"""
Sidebar Component
Renders sidebar controls and handles parameter inputs.
"""

import streamlit as st
from typing import Dict, Any


def render_sidebar() -> Dict[str, Any]:
    """
    Renders global app sidebar controls and returns configuration inputs.
    """
    st.sidebar.image("https://img.icons8.com/color/96/milk-bottle.png", width=64)
    st.sidebar.title("⚙️ Enterprise Controls")
    
    st.sidebar.markdown("---")
    
    # 1. Processing Volume & Target Settings
    st.sidebar.subheader("🏢 Procurement Scale")
    daily_volume_m_liters = st.sidebar.slider(
        "Daily Processing Volume (Million L/day)",
        min_value=5.0,
        max_value=50.0,
        value=20.0,
        step=1.0,
        help="Total daily raw milk procurement across all collection hubs."
    )
    
    target_reduction_pct = st.sidebar.slider(
        "2030 Decarbonization Target (%)",
        min_value=10.0,
        max_value=50.0,
        value=30.0,
        step=5.0,
        help="Target carbon intensity reduction percentage relative to baseline."
    )
    
    st.sidebar.markdown("---")
    
    # 2. Emission Factor Overrides
    st.sidebar.subheader("⚡ Emission Factors")
    grid_ef = st.sidebar.number_input(
        "Grid Electricity Factor (kg CO₂e / kWh)",
        min_value=0.10,
        max_value=1.50,
        value=0.716,
        step=0.01
    )
    
    transit_ef = st.sidebar.number_input(
        "Tanker Transport Factor (kg CO₂e / ton-km)",
        min_value=0.01,
        max_value=0.50,
        value=0.11,
        step=0.01
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("🥛 *Dairy Decarbonization Decision Support System*")
    
    return {
        "daily_volume_liters": daily_volume_m_liters * 1_000_000,
        "target_reduction_pct": target_reduction_pct,
        "grid_ef": grid_ef,
        "transit_ef": transit_ef
    }