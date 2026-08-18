# Memory Bank & Context Record

## 1. Domain Context & Core Terminology
* **Cooperative Dairy Enterprise:** Procurement structure sourcing raw milk from millions of rural smallholders (typically 2–5 animals per household)[cite: 1].
* **Carbon Intensity:** Key ESG performance metric calculated as total enterprise greenhouse gas emissions divided by total raw milk processed ($kg CO_2e / kg milk$)[cite: 1].
* **Scope 3 Dominance:** Over 85%-92% of enterprise emissions are upstream on-farm emissions outside direct operational control[cite: 1].
* **Temperature-Humidity Index (THI):** Combined environmental metric measuring heat stress impact on livestock productivity[cite: 1].

## 2. Default Baseline Data Parameters

```json
{
  "enterprise_default": {
    "daily_volume_liters": 20000000,
    "target_reduction_pct": 30.0,
    "grid_ef_kg_co2e_kwh": 0.716,
    "tanker_ef_kg_co2e_tonkm": 0.11
  },
  "regional_zones": {
    "zone_1_west": {
      "name": "Western Hub (Gujarat/Rajasthan)",
      "baseline_intensity": 2.25,
      "herd_mix": {"buffalo": 0.50, "crossbred": 0.35, "indigenous": 0.15}
    },
    "zone_2_north": {
      "name": "Northern Belt (Punjab/Haryana/UP)",
      "baseline_intensity": 1.98,
      "herd_mix": {"buffalo": 0.35, "crossbred": 0.55, "indigenous": 0.10}
    },
    "zone_3_south": {
      "name": "Southern/Central (Karnataka/MH)",
      "baseline_intensity": 2.10,
      "herd_mix": {"buffalo": 0.40, "crossbred": 0.40, "indigenous": 0.20}
    }
  }
}

## 3. Analytical Assumptions & DecisionsThird-Party Disclosures: 
The application follows GHG Protocol Corporate and Agricultural guidance for auditability[cite: 1].
Standardized Units: All final emissions metrics are normalized to $kg CO_2e / kg milk$ processed[cite: 1].
IPCC AR6 Compliance: Uses 100-year GWP values ($CH_4 = 28$, $N_2O = 265$)[cite: 1].