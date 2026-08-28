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
    st.header("Dairy Enterprise Carbon Reduction Strategy")
    st.caption("How operational choices, cow nutrition, and herd efficiency drive our 2030 sustainability goals.")
    st.markdown("---")
    
    # SECTION 1: EXECUTIVE KPI CARDS
    st.subheader("🎯 Enterprise Operational Baseline")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Daily Milk Target</div>
            <div class="metric-value">2.0M Liters</div>
            <div class="metric-desc">~2.06 Million kg of processed milk per day (751.8M kg/year).</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Active Herd Needed</div>
            <div class="metric-value">333,333 Cows</div>
            <div class="metric-desc">Based on current average yield of 6 Liters/cow per day.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Annual Methane Burps</div>
            <div class="metric-value">20,000 Tons</div>
            <div class="metric-desc">Produced by cows during natural digestive fermentation.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">2030 Reduction Goal</div>
            <div class="metric-value">30% Drop</div>
            <div class="metric-desc">Targeting 1.309 kg carbon/kg milk (down from 1.870 kg).</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # SECTION 2: WHERE DOES THE CARBON COME FROM? (PLAIN LANGUAGE BREAKDOWN)
    st.subheader("🔍 Where Does Our Carbon Footprint Come From?")
    st.markdown("Instead of complicated reporting codes, we divide our footprint into **3 real-world operational sources**:")
    
    c_src1, c_src2, c_src3 = st.columns(3)
    
    with c_src1:
        st.markdown("""
        ### 1. Factory & Generator Fuel
        **Share of Problem: ~0.7%**
        * **What it is:** Diesel burned on-site in backup generators at village cooling units and plant heating boilers.
        * **Usage:** Uses ~$0.005\\text{ Liters of diesel}$ per kg of milk processed.
        * **Takeaway:** Important for operations, but minor in total emissions impact.
        """)
        
    with c_src2:
        st.markdown("""
        ### 2. Purchased Grid Power
        **Share of Problem: ~1.5%**
        * **What it is:** Electricity bought from the grid to power milk chillers, pasteurizers, and cold storage units.
        * **Usage:** Consumes ~$0.04\\text{ kWh}$ of grid electricity per kg of milk.
        * **Takeaway:** Factory efficiency is valuable, but cannot solve the overall footprint alone.
        """)
        
    with c_src3:
        st.markdown("""
        ### 3. Cows & Farm Operations
        **Share of Problem: ~97.8%**
        * **What it is:** Cow digestion burps, manure pit storage, and milk tanker transport.
        * **Usage:** Generates ~$1.816\\text{ kg of carbon equivalent}$ per kg of milk.
        * **Takeaway:** Nearly 98% of our entire footprint comes directly from on-farm livestock.
        """)

    st.markdown("---")

    # SECTION 3: THE HERD MATH & FEED SOLUTION STORY CARD
    st.subheader("💡 The Solution: How Better Cattle Feed Cuts the Herd & Methane")
    
    st.markdown("""
    Cows need energy just to stay alive (maintain body heat, walk, and breathe). 
    On **unbalanced feed**, a cow spends **75% of its energy surviving**, leaving only 25% to produce milk ($6\\text{ L/day}$). 
    When we provide **balanced feed**, the cow's survival cost stays the same, but milk yield jumps to **$10\\text{ L/day}$**.
    """)

    card_col1, card_col2 = st.columns(2)
    
    with card_col1:
        st.error("**CURRENT BASELINE (Unbalanced Feed)**")
        st.markdown("""
        * **Daily Milk Yield:** $6\\text{ Liters per cow}$
        * **Active Herd Needed:** **333,333 Cows** ($\frac{2,000,000\\text{ L}}{6\\text{ L/cow}}$)
        * **Burp Methane:** **20,000 Tonnes of Methane gas / year**
        * **Result:** A massive active herd burping gas continuously to meet our delivery target.
        """)
        
    with card_col2:
        st.success("**IMPROVED FEED SCENARIO (Balanced Nutrition)**")
        st.markdown("""
        * **Daily Milk Yield:** $10\\text{ Liters per cow}$
        * **Active Herd Needed:** **200,000 Cows** ($\frac{2,000,000\\text{ L}}{10\\text{ L/cow}}$)
        * **Burp Methane:** **12,000 Tonnes of Methane gas / year**
        * **Result:** Fulfill the exact same 2M Liter milk contract with **133,333 FEWER cows** ($40\\%$ reduction).
        """)

    st.markdown("""
    <div class="highlight-box">
        <strong>🔑 Key Takeaway for Business Leaders:</strong> Improving feed quality doesn't just cut methane burps—it dramatically reduces the total number of animals needed to hit our daily 2 Million Liter target. Fewer cows mean fewer burps, lower farm costs, and a massive drop in carbon footprint.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # SECTION 4: THE 3 ACTIONABLE DECARBONIZATION LEVERS
    st.subheader("🚀 Operational Interventions to Hit Our 30% Target")
    
    l_col1, l_col2, l_col3 = st.columns(3)
    
    with l_col1:
        st.markdown("**1. Feed Rationing & Additives**")
        st.caption("Focus: Smallholder Farms")
        st.markdown("""
        Distribute feed optimization software and dietary supplements to farmers.
        * **Impact:** Cuts enteric methane burps by up to **15%** and raises per-cow milk yields.
        """)
        
    with l_col2:
        st.markdown("**2. Solar Chilling Centers**")
        st.caption("Focus: Rural Collection Points")
        st.markdown("""
        Install rooftop solar PV and battery power at village Bulk Milk Coolers (BMCs).
        * **Impact:** Replaces up to **60%** of diesel generator and grid power emissions.
        """)
        
    with l_col3:
        st.markdown("**3. Village Manure Digesters**")
        st.caption("Focus: Farmer Cooperatives")
        st.markdown("""
        Build simple covered digesters to capture raw manure gas for clean cooking fuel.
        * **Impact:** Captures up to **60%** of escaping manure methane gas.
        """)

    st.info("💡 **Next Steps:** Select **'📊 Baseline Footprint'** above to explore current regional emissions, or open **'🌱 Decarbonization Simulator'** to adjust intervention adoption sliders.")
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
