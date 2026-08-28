"""
Dairy Enterprise Decarbonization & Climate Risk Dashboard
Main Streamlit Application Entry Point
"""

import json
import pandas as pd
import streamlit as st
import os
from engine.carbon_math import calculate_baseline_emissions
from components.sidebar import render_sidebar
from views.tab_baseline import render_tab_baseline
from views.tab_mitigation import render_tab_mitigation
from views.tab_climate_risk import render_tab_climate_risk

# --- Sidebar Documentation Download Section ---
st.sidebar.markdown("---")
st.sidebar.subheader("📖 Documentation")

doc_path = os.path.join("docs", "Dairy_ESG_Analytics_Architecture.docx")

if os.path.exists(doc_path):
    with open(doc_path, "rb") as file:
        st.sidebar.download_button(
            label="📄 Download ESG Architecture Doc",
            data=file,
            file_name="Dairy_ESG_Analytics_Architecture.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            help="Download the complete technical documentation and architecture design document."
        )
else:
    st.sidebar.warning("Documentation file not found in `docs/` folder.")

# 1. Page Configuration
st.set_page_config(
    page_title="Dairy Decarbonization & Climate Simulator",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Data Loader Functions
@st.cache_data
def load_configuration_data():
    with open("data/config/baseline_params.json", "r") as f:
        params = json.load(f)
    
    regional_df = pd.read_csv("data/raw/regional_zones.csv")
    scenarios_df = pd.read_csv("data/raw/climate_scenarios.csv")
    
    return params, regional_df, scenarios_df

# Load static resources
params, regional_df, scenarios_df = load_configuration_data()

# 3. Render Sidebar Controls
user_inputs = render_sidebar()

# Dynamic Parameter Overrides
params["enterprise_defaults"]["grid_emission_factor_kg_co2e_kwh"] = user_inputs["grid_ef"]
params["enterprise_defaults"]["tanker_transit_factor_kg_co2e_tonkm"] = user_inputs["transit_ef"]

# 4. Main Executive Header
st.title("🥛 Enterprise Dairy Decarbonization & Risk Dashboard")
st.markdown(
    "Decision support tool for baseline Scope 1, 2, & 3 GHG emissions accounting, "
    "IPCC climate stress-testing, and 2030 target pathway simulation."
)
st.markdown("---")

# 5. Execute Core Baseline Accounting Engine
regional_list = regional_df.to_dict(orient="records")
baseline_results = calculate_baseline_emissions(
    daily_volume_liters=user_inputs["daily_volume_liters"],
    regional_data=regional_list,
    params=params
)

# 6. Tab Navigation Layout
tab_overview,tab1, tab2, tab3 = st.tabs([
    "📋 Overview & Methodology",
    "📊 Baseline Footprint", 
    "🌱 Decarbonization Simulator", 
    "☀️ Climate Stress-Test"
])

with tab_overview:
    st.header("Dairy Value Chain Decarbonization Framework")
    st.caption("Strategic Executive Briefing: Enterprise Goals, Operational Process & Baseline Assumptions")
    
    st.markdown("---")
    
    # Section 1: Enterprise Goal
    st.subheader("🎯 Enterprise Decarbonization Goal")
    st.markdown("""
    * **Primary Target:** Achieve a **30% reduction in overall carbon intensity** ($1.870 \\rightarrow 1.309\\text{ kg CO}_2\\text{e / kg milk}$) by **2030**.
    * **Enterprise Scale:** Base procurement volume of **2.0 Million Liters/day** ($\approx 2,060,000\\text{ kg/day}$ at $1.03\\text{ kg/L}$ density), totaling **~751.8 Million kg annually**.
    * **Comprehensive Scope:** Full accounting across **Scope 1** (diesel generators/boilers), **Scope 2** (purchased grid power), and **Scope 3** (upstream smallholder farming & milk transport logistics).
    """)
    
    st.markdown("---")
    
    # Section 2: Operational Process
    st.subheader("⚙️ ESG Accounting & Modeling Process")
    
    col_proc1, col_proc2, col_proc3 = st.columns(3)
    
    with col_proc1:
        st.markdown("**1. Baseline Footprinting**")
        st.markdown("""
        * Track physical milk mass balance across regional procurement zones.
        * Convert multi-gas emissions ($\text{CO}_2, \text{CH}_4, \text{N}_2\text{O}$) using **IPCC AR6** Global Warming Potentials.
        * Establish current carbon intensity per kg of raw milk processed.
        """)
        
    with col_proc2:
        st.markdown("**2. Intervention Simulation**")
        st.markdown("""
        * Model 3 targeted decarbonization levers: **Precision Feed Rationing**, **Solar BMC Conversion**, and **Manure Digesters**.
        * Dynamically calculate herd yield improvements (*Dilution of Maintenance Effect*).
        * Project step-by-step abatement pathways on a dynamic waterfall chart.
        """)
        
    with col_proc3:
        st.markdown("**3. Physical Climate Stress Testing**")
        st.markdown("""
        * Model Temperature-Humidity Index (THI) heat stress under climate scenarios (SSP5-8.5).
        * Quantify biological milk yield loss penalties in cattle/buffaloes.
        * Calculate total herd expansion requirements and financial/carbon feedback risks.
        """)

    st.markdown("---")

    # Section 3: Key Assumptions & Parameters
    st.subheader("📌 Key Modeling Assumptions & Parameters")
    
    col_asm1, col_asm2 = st.columns(2)
    
    with col_asm1:
        st.markdown("**Operational & Grid Parameters**")
        st.markdown("""
        * **Raw Milk Density:** $1.03\\text{ kg/L}$ (Standard dairy conversion factor).
        * **Plant Diesel Usage (Scope 1):** $0.005\\text{ Liters / kg milk}$ ($2.68\\text{ kg CO}_2\\text{e / L}$).
        * **Grid Electricity Usage (Scope 2):** $0.04\\text{ kWh / kg milk}$ ($0.716\\text{ kg CO}_2\\text{e / kWh}$).
        * **Collection Transit (Scope 3):** Average $100\\text{--}120\\text{ km}$ radius ($0.11\\text{ kg CO}_2\\text{e / ton-km}$).
        """)
        
    with col_asm2:
        st.markdown("**Livestock & Biological Factors (Scope 3)**")
        st.markdown("""
        * **Global Warming Potentials (GWP):** $\\text{CH}_4 = 28.0\\times\\text{CO}_2\\text{e}$, $\\text{N}_2\\text{O} = 265.0\\times\\text{CO}_2\\text{e}$.
        * **Enteric Methane Emission Factors:** $58\\text{ to }65\\text{ kg CH}_4/\\text{head/year}$ across regional herd mix.
        * **Yield Dilution Effect:** Optimized feed boosts individual yield, reducing total required herd size for fixed enterprise targets.
        """)

    st.info("💡 **Navigation:** Click on **'📊 Baseline Footprint'** above to examine detailed emissions breakdowns, or move to **'🌱 Decarbonization Simulator'** to test adoption levers.")
# P


with tab1:
    render_tab_baseline(baseline_results, regional_df)

with tab2:
    render_tab_mitigation(
        baseline_data=baseline_results,
        params=params,
        target_pct=user_inputs["target_reduction_pct"]
    )

with tab3:
    render_tab_climate_risk(
        baseline_data=baseline_results,
        scenarios_df=scenarios_df,
        regional_data=regional_list
    )
