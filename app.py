"""
Dairy Enterprise Decarbonization & Climate Risk Dashboard
Main Streamlit Application Entry Point
"""

import json
import pandas as pd
import streamlit as st

from engine.carbon_math import calculate_baseline_emissions
from components.sidebar import render_sidebar
from views.tab_baseline import render_tab_baseline
from views.tab_mitigation import render_tab_mitigation
from views.tab_climate_risk import render_tab_climate_risk

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
tab1, tab2, tab3 = st.tabs([
    "📊 Baseline Footprint", 
    "🌱 Decarbonization Simulator", 
    "☀️ Climate Stress-Test"
])

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