# Project Implementation Phases

## Phase 1: Core Setup & Mathematical Engine Architecture
* Setup repository structure and standard Python dependencies (`streamlit`, `pandas`, `plotly`, `numpy`).
* Build module `engine/carbon_math.py` containing deterministic functions for Scope 1, 2, and 3 baseline calculations[cite: 1].
* Unit test baseline outputs against verified Indian smallholder cooperative defaults[cite: 1].

## Phase 2: Streamlit Dashboard UI & Baseline Visualization (Tab 1)
* Build app shell `app.py` with custom CSS styling and sidebar parameters[cite: 1].
* Implement Metric Cards (Total Annual CO₂e, Scope 3 %, Baseline Intensity)[cite: 1].
* Construct Tab 1 with an interactive Plotly Scope breakdown donut chart and regional procurement dataframes[cite: 1].

## Phase 3: Decarbonization Lever Simulation Engine (Tab 2)
* Implement `engine/mitigation.py` modeling reduction factors for ration balancing, solar BMCs, and manure digesters[cite: 1].
* Build Tab 2 slider controls and dynamic Plotly Waterfall / Abatement Trajectory chart[cite: 1].
* Integrate target tracker KPI card (Pass/Fail status indicator for the 30% reduction goal)[cite: 1].

## Phase 4: IPCC Climate Risk & Sourcing Optimization (Tab 3)
* Implement `engine/climate_risk.py` modeling THI yield penalties across SSP1-2.6, SSP2-4.5, and SSP5-8.5 scenarios[cite: 1].
* Build Tab 3 regional sourcing allocation sliders and transport penalty calculator[cite: 1].
* Render dual-axis plot comparing summer yield loss vs. escalating carbon intensity[cite: 1].

## Phase 5: Verification, Polish & Deployment
* Perform end-to-end user sanity testing across edge-case parameter values.
* Add documentation expanders detailing formulas and emission factor references.
* Deploy application to Streamlit Community Cloud.