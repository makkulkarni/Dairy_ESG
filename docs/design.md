# UI/UX & Design Specification

## 1. Visual Theme & Color Palette
The interface follows an enterprise executive aesthetic utilizing clean light-mode cards with high contrast:
* **Primary Brand Color:** `#1A365D` (Deep Navy)[cite: 1]
* **Secondary Brand Color:** `#2B6CB0` (Slate Blue)[cite: 1]
* **Accent & Warning Color:** `#C53030` (Muted Crimson - Heat/Risk)[cite: 1]
* **Success Color:** `#38A169` (Forest Green - Mitigation Target Met)[cite: 1]
* **Background Shading:** `#F7FAFC` (Light Gray/Blue Neutral)[cite: 1]

---

## 2. Layout Structure

### 2.1 Sidebar Panel
* **Enterprise Setup Expander:**
  * Processing Volume Slider (`5M` to `50M` Liters/day, default: `20M`)[cite: 1].
  * 2030 Carbon Target Slider (`10%` to `50%`, default: `30%`)[cite: 1].
* **Emission Factor Controls Expander:**
  * Grid Emission Factor Input (`kg CO₂e / kWh`, default: `0.716`)[cite: 1].
  * Tanker Logistics Factor Input (`kg CO₂e / ton-km`, default: `0.11`)[cite: 1].
* **Global Climate Scenario Selector:** Radio selection (`Baseline`, `SSP1-2.6`, `SSP2-4.5`, `SSP5-8.5`)[cite: 1].

### 2.2 Main Dashboard Tabs
* **Tab 1: 📊 Baseline Footprint & Disclosures**
  * Row 1: 3 Column KPI Summary Cards (Total CO₂e, Scope 3 Share %, Current Carbon Intensity)[cite: 1].
  * Row 2: Donut Chart (Emissions by Scope) + Table (Regional Baseline Profiles)[cite: 1].
* **Tab 2: 🌱 Decarbonization Simulator**
  * Left Column: Interactive sliders for Ration Balancing (0-100%), Solar BMCs (0-100%), Manure Digesters (0-100%)[cite: 1].
  * Right Column: Plotly Waterfall Chart tracking step-by-step carbon abatement down to 2030 target[cite: 1].
* **Tab 3: ☀️ Climate Stress-Test & Sourcing**
  * Row 1: Dual-axis plot (Summer Yield Loss % vs. Carbon Intensity Escalation)[cite: 1].
  * Row 2: Regional Re-allocation Sliders (West % / North % / South %) with live transport carbon penalty trade-off calculator[cite: 1].