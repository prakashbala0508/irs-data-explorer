
# components/income_brackets.py

import streamlit as st
import plotly.graph_objects as go


def run(df):
    st.markdown("## Income Bracket Deep Dive")
    st.markdown(
        "Analyze how tax burdens, EITC utilization, and charitable giving patterns "
        "shift across income tiers nationwide. Data: IRS SOI 2021."
    )

    agi_labels = {
        1: "Under $25K",
        2: "$25K-$50K",
        3: "$50K-$75K",
        4: "$75K-$100K",
        5: "$100K-$200K",
        6: "$200K+",
    }

    bracket_agg = (
        df[df["agi_stub"] > 0]
        .groupby("agi_stub")
        .agg(
            total_returns=("N1", "sum"),
            avg_effective_rate=("effective_rate", "mean"),
            avg_eitc_utilization=("eitc_utilization_rate", "mean"),
            avg_charitable=("avg_charitable", "mean"),
            avg_agi=("avg_agi", "mean"),
        )
        .reset_index()
    )
    bracket_agg["bracket"] = bracket_agg["agi_stub"].map(agi_labels)
    bracket_agg = bracket_agg.dropna()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=bracket_agg["bracket"],
        y=bracket_agg["avg_effective_rate"] * 100,
        marker_color="#1f3a5f",
        name="Effective Tax Rate (%)",
    ))
    fig1.update_layout(
        title="Average Effective Federal Tax Rate by Income Bracket -- IRS SOI 2021",
        yaxis_title="Effective Tax Rate (%)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
        height=380,
    )
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig2 = go.Figure(go.Bar(
            x=bracket_agg["bracket"],
            y=bracket_agg["avg_eitc_utilization"] * 100,
            marker_color="#2ecc71",
        ))
        fig2.update_layout(
            title="EITC Utilization Rate by Bracket (%)",
            yaxis_title="% of Returns Claiming EITC",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Arial", size=12),
            height=340,
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig3 = go.Figure(go.Bar(
            x=bracket_agg["bracket"],
            y=bracket_agg["avg_charitable"],
            marker_color="#8e44ad",
        ))
        fig3.update_layout(
            title="Average Charitable Contribution by Bracket ($)",
            yaxis_title="Average Amount ($)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Arial", size=12),
            height=340,
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### What This Tells Us")
    st.markdown(
        "Effective tax rates rise with income as expected under a progressive system, "
        "but the steepness of the progression and the drop-off in EITC utilization above "
        "the $50K tier reflects the phase-out schedules embedded in current law. "
        "Charitable contributions rise sharply at the $200K+ tier, consistent with the "
        "greater itemization incentive at higher marginal rates."
    )
