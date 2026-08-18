"""
Charts Component
Generates Plotly charts for Scope breakdowns, Waterfall abatement, and Climate Stress.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any


def create_scope_donut_chart(baseline_data: Dict[str, Any]) -> go.Figure:
    """
    Generates a donut chart displaying Scope 1, Scope 2, and Scope 3 proportions.
    """
    labels = ["Scope 1 (Direct Fuels)", "Scope 2 (Purchased Power)", "Scope 3 (Upstream Farm & Transport)"]
    values = [
        baseline_data["scope1_tco2e"],
        baseline_data["scope2_tco2e"],
        baseline_data["scope3_tco2e"]
    ]
    
    colors = ["#2B6CB0", "#CBD5E0", "#1A365D"]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors),
        textinfo="label+percent",
        insidetextorientation="radial"
    )])
    
    fig.update_layout(
        title="<b>GHG Footprint Breakdown by Scope</b>",
        showlegend=False,
        margin=dict(t=40, b=20, l=20, r=20),
        height=320
    )
    return fig


def create_abatement_waterfall(baseline_tco2e: float, mitigation_results: Dict[str, Any]) -> go.Figure:
    """
    Generates a waterfall chart showing carbon reductions step-by-step.
    """
    fig = go.Figure(go.Waterfall(
        name="Abatement Pathway",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=[
            "Baseline Footprint",
            "Ration Balancing",
            "Solar BMCs",
            "Manure Digesters",
            "Target Footprint"
        ],
        textposition="outside",
        text=[
            f"{baseline_tco2e:,.0f}",
            f"-{mitigation_results['ration_abatement_tco2e']:,.0f}",
            f"-{mitigation_results['solar_abatement_tco2e']:,.0f}",
            f"-{mitigation_results['digester_abatement_tco2e']:,.0f}",
            f"{mitigation_results['mitigated_total_tco2e']:,.0f}"
        ],
        y=[
            baseline_tco2e,
            -mitigation_results["ration_abatement_tco2e"],
            -mitigation_results["solar_abatement_tco2e"],
            -mitigation_results["digester_abatement_tco2e"],
            mitigation_results["mitigated_total_tco2e"]
        ],
        connector={"line": {"color": "#CBD5E0"}},
        decreasing={"marker": {"color": "#38A169"}},
        totals={"marker": {"color": "#1A365D"}}
    ))
    
    fig.update_layout(
        title="<b>2030 Decarbonization Abatement Waterfall (tCO₂e)</b>",
        showlegend=False,
        margin=dict(t=40, b=20, l=20, r=20),
        height=380,
        yaxis_title="Annual tCO₂e"
    )
    return fig


def create_climate_risk_chart(scenarios_df, selected_code: str) -> go.Figure:
    """
    Generates a bar chart comparing carbon intensity escalation across IPCC SSP scenarios.
    """
    colors = ["#CBD5E0" if code != selected_code else "#C53030" for code in scenarios_df["scenario_code"]]
    
    fig = go.Figure(data=[
        go.Bar(
            x=scenarios_df["scenario_name"],
            y=scenarios_df["crossbred_yield_loss_pct"],
            marker_color=colors,
            text=[f"{val:.1f}% Yield Loss" for val in scenarios_df["crossbred_yield_loss_pct"]],
            textposition="auto"
        )
    ])
    
    fig.update_layout(
        title="<b>Crossbred Cow Summer Yield Loss (%) by IPCC Pathway</b>",
        yaxis_title="Yield Penalty (%)",
        xaxis_title="IPCC SSP Pathway",
        margin=dict(t=40, b=20, l=20, r=20),
        height=320
    )
    return fig