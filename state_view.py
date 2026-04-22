
# components/state_view.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def run(df):
    st.markdown("## State-Level Tax Analysis")
    st.markdown(
        "Aggregated from IRS SOI 2021 ZIP code data. Each metric represents the "
        "weighted average across all ZIP codes within the selected state."
    )

    metric = st.selectbox(
        "Select Metric to Visualize by State",
        [
            "Effective Tax Rate",
            "Average AGI",
            "Average Federal Tax Paid",
            "EITC Utilization Rate",
            "Average Charitable Contribution",
        ],
    )

    metric_map = {
        "Effective Tax Rate": "effective_rate",
        "Average AGI": "avg_agi",
        "Average Federal Tax Paid": "avg_tax",
        "EITC Utilization Rate": "eitc_utilization_rate",
        "Average Charitable Contribution": "avg_charitable",
    }

    col = metric_map[metric]

    state_agg = (
        df[df["agi_stub"] > 0]
        .groupby("STATE")[col]
        .mean()
        .reset_index()
        .rename(columns={"STATE": "state", col: "value"})
        .dropna()
    )

    fig = px.choropleth(
        state_agg,
        locations="state",
        locationmode="USA-states",
        color="value",
        scope="usa",
        color_continuous_scale="Blues",
        title=f"{metric} by State -- IRS SOI 2021",
        labels={"value": metric},
    )
    fig.update_layout(
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### State Rankings")
    state_agg_sorted = state_agg.sort_values("value", ascending=False).head(15)
    fig2 = go.Figure(go.Bar(
        x=state_agg_sorted["state"],
        y=state_agg_sorted["value"],
        marker_color="#1f3a5f",
    ))
    fig2.update_layout(
        title=f"Top 15 States -- {metric}",
        yaxis_title=metric,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12),
        height=380,
    )
    st.plotly_chart(fig2, use_container_width=True)
