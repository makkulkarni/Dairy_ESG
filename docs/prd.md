# Product Requirements Document (PRD)

## 1. Executive Summary & Objective
Large-scale dairy cooperatives operate at a unique nexus of commercial scale and hyper-fragmented supply chains. Over 85% to 92% of an enterprise's carbon footprint resides in Scope 3 upstream milk sourcing across millions of smallholder farmers. 

The goal of this application is to build an interactive, data-driven Streamlit decision-support dashboard that enables sustainability leads, executive teams, and supply chain analysts to:
1. Measure baseline Scope 1, 2, and 3 GHG emissions following GHG Protocol and IPCC agricultural guidelines.
2. Stress-test physical climate risks (heat stress, drought) across IPCC Shared Socioeconomic Pathways (SSPs)[cite: 1].
3. Simulate multi-lever decarbonization strategies to hit a target **30% reduction in carbon intensity (kg CO₂e / kg milk) by 2030**[cite: 1].

---

## 2. Core User Stories
* **As an ESG / Sustainability Officer**, I want to view dynamic carbon intensity metrics ($kg CO_2e / kg milk$) broken down by Scope 1, 2, and 3 so that I can report auditable baseline disclosures under ISSB S2 and EU CSRD[cite: 1].
* **As a Supply Chain Strategist**, I want to adjust regional procurement shares (West, North, South) and model IPCC climate warming scenarios so that I can evaluate heat-stress yield losses against tanker transit carbon costs[cite: 1].
* **As an Operations Executive**, I want interactive toggle controls for mitigation levers (ration balancing, solar BMCs, manure digesters) so that I can visualize an optimal pathway to hit our 2030 target[cite: 1].

---

## 3. Key Feature Requirements

### 3.1 Baseline GHG Accounting Engine
* Support custom inputs for daily processing volume (default: 20M Liters/day)[cite: 1].
* Scope 1: Processing plant thermal burn, diesel backup generator usage at Bulk Milk Coolers (BMCs), and captive fleets[cite: 1].
* Scope 2: Purchased grid electricity using state/national grid factors (default: $0.716\text{ kg CO}_2\text{e/kWh}$)[cite: 1].
* Scope 3: Enterprise enteric fermentation ($CH_4$), manure management ($CH_4, N_2O$), feed cultivation ($N_2O$), and transport logistics[cite: 1].

### 3.2 IPCC Climate Risk Stress-Testing
* Incorporate three IPCC pathways: **SSP1-2.6 (+1.5°C)**, **SSP2-4.5 (+2.7°C)**, and **SSP5-8.5 (+4.4°C)**[cite: 1].
* Temperature-Humidity Index (THI) yield penalty calculation for values exceeding 72[cite: 1].
* Yield crash compensation logic: calculate additional herd sizes required to maintain target milk throughput[cite: 1].

### 3.3 Decarbonization Lever Simulator
* **Ration Balancing & Feed Additives:** 10%–15% enteric methane reduction[cite: 1].
* **Village BMC Solarization:** Eliminates BMC diesel backup generator run hours and grid power reliance[cite: 1].
* **Anaerobic Manure Digesters:** Up to 60% reduction in Scope 3 manure management emissions[cite: 1].
* **Geographic Sourcing Reallocation:** Dynamic procurement shifting between Western, Northern, and Southern hubs[cite: 1].

---

## 4. Non-Functional Requirements
* **Response Time:** Reactive visual updates in Streamlit under 500 ms upon slider adjustment.
* **Auditability:** Clear mathematical formulas exposed in UI tooltips/expander sections.
* **Portability:** Single standalone Python codebase deployable on local Python environments, Streamlit Community Cloud, or Docker containers.