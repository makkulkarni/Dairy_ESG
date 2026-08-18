# Rules, Constraints & Mathematical Specifications

## 1. GHG Protocol Boundary & Formula Rules

### 1.1 Carbon Intensity Formula
$$\text{Carbon Intensity } (\text{kg CO}_2\text{e / kg milk}) = \frac{\text{Scope 1} + \text{Scope 2} + \text{Scope 3 Total Emissions } (\text{kg CO}_2\text{e})}{\text{Total Annual Raw Milk Procured } (\text{kg})}$$[cite: 1]

### 1.2 Global Warming Potentials (IPCC AR6 Standards)
* Methane ($\text{CH}_4$): $1\text{ kg } \text{CH}_4 = 28\text{ kg CO}_2\text{e}$[cite: 1]
* Nitrous Oxide ($\text{N}_2\text{O}$): $1\text{ kg } \text{N}_2\text{O} = 265\text{ kg CO}_2\text{e}$[cite: 1]

### 1.3 Scope Boundary Rules
* **Scope 1:** Direct diesel fuel burn ($\text{liters} \times 2.68\text{ kg CO}_2\text{e/L}$) + direct thermal fuel[cite: 1].
* **Scope 2:** Grid electricity ($\text{kWh} \times \text{Grid Emission Factor}$)[cite: 1].
* **Scope 3:** Enterprise smallholder farming ($\text{enteric} + \text{manure} + \text{feed}$) + inter-hub transport logistics ($\text{ton-km} \times \text{Transit Factor}$)[cite: 1].

---

## 2. Hard System Constraints

1. **Procurement Mass Balance Rule:**
   $$\sum (\text{Procurement Volume}_{\text{Region Zone}}) = \text{Total Target Enterprise Volume}$$[cite: 1]
   *Procurement percentages across Zone 1, Zone 2, and Zone 3 must always sum to exactly 100%.*

2. **2030 Decarbonization Target Rule:**
   $$\text{Target Intensity} = \text{Baseline Intensity} \times (1 - \text{Target Reduction Percentage})$$[cite: 1]
   *(Default Target = 30% reduction by 2030)*[cite: 1].

---

## 3. Physical Climate Stress Rules (THI Mechanism)

* **THI Equation:**
  $$\text{THI} = (1.8 \times T + 32) - (0.55 - 0.0055 \times RH) \times (1.8 \times T - 26)$$[cite: 1]
* **Heat Stress Threshold:** When $\text{THI} > 72$, milk productivity drops according to herd type[cite: 1]:
  * Cross-bred Cows: High yield sensitivity (up to 25% drop under extreme heat)[cite: 1].
  * Buffaloes: Moderate yield sensitivity (up to 12% drop under extreme heat)[cite: 1].
* **Herd Compensation Penalty:** If yield drops by $X\%$, total regional herd count must grow by $\frac{X}{1-X}\%$ to maintain overall milk supply volume, driving up total enteric methane emissions[cite: 1].