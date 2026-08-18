# Technical Architecture Document

## 1. System Overview Blueprint
┌─────────────────────────────────────────────────────────────────────────────┐
│                             STREAMLIT FRONTEND                              │
└──────────────────────────────────────┬──────────────────────────────────────┘
│
┌─────────────────────────┬─────────┴─────────┬─────────────────────────┐
▼                         ▼                   ▼                         ▼
Sidebar Controls        Tab 1: Baseline     Tab 2: Mitigation       Tab 3: Climate Risk
• Daily Volume          • Metric Cards      • Lever Sliders         • SSP Selector
• Reduction Target      • Scope Donut Chart • Abatement Waterfall   • Regional Heatmaps
• Factors Overrides     • Region Table      • Target Status Card    • Sourcing Allocator
└─────────────────────────┼───────────────────┼─────────────────────────┘
│                   │
▼                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ANALYTICAL ENGINE                              │
│  ┌─────────────────────────┐ ┌───────────────────────┐ ┌───────────────────┐│
│  │  GHG Accounting Core    │ │ Climate Yield Module  │ │ Optimization Core ││
│  │  (Scope 1, 2, 3 Math)   │ │  (THI Penalty Logic)  │ │ (Transport vs Farm││
│  └─────────────────────────┘ └───────────────────────┘ └───────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
---

## 2. Technical Tech Stack

| Component | Choice / Specification | Purpose |
| :--- | :--- | :--- |
| **Framework** | Python 3.10+ / Streamlit | Rapid interactive web UI and reactive layout state management[cite: 1]. |
| **Data Processing** | Pandas, NumPy | Vectorized baseline carbon calculations, matrix multiplication, and regional operations[cite: 1]. |
| **Data Visualization** | Plotly Express / Graph Objects | Interactive donut charts, abatement curves, and dual-axis climate scenario plots[cite: 1]. |
| **Deployment** | Streamlit Cloud / Docker | Lightweight containerized deployment environment. |

---

## 3. Data Flow Architecture

* **User Input & Session State Initialization:** Streamlit sidebar populates Session State with baseline milk processing volume, grid carbon intensity, transit distance, and target reduction %[cite: 1].
* **Analytical Engine Execution:**
  * `calculate_baseline_emissions()` computes absolute annual emissions ($tCO_2e$) and baseline carbon intensity ($kg CO_2e / kg milk$)[cite: 1].
  * `apply_mitigation_levers()` calculates incremental carbon abatement across selected active sliders[cite: 1].
  * `stress_test_climate_risk()` evaluates Temperature-Humidity Index (THI) yield degradation based on the chosen IPCC scenario and recalculates Scope 3 emissions[cite: 1].
* **UI Rendering:** Plotly objects render updated graphics reactively across Dashboard tabs[cite: 1].