
# components/zip_benchmarker.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def run(df):
    st.markdown("## ZIP Code Client Benchmarker")
    st.markdown(
        "Enter a client ZIP code and their key return figures to see how they compare "
        "against all other filers in the same ZIP code and income tier. "
        "Data: IRS SOI 2021 Individual Income Tax ZIP Code Statistics."
    )

    col1, col2 = st.columns(2)
    with col1:
        zip_input = st.text_input("Client ZIP Code", value="21045", max_chars=5)
    with col2:
        agi_stub = st.selectbox(
            "Client AGI Bracket",
            [1, 2, 3, 4, 5, 6],
            format_func=lambda x: {
                1: "Under $25,000",
                2: "$25,000 - $50,000",
                3: "$50,000 - $75,000",
                4: "$75,000 - $100,000",
                5: "$100,000 - $200,000",
                6: "$200,000 or more",
            }[x],
        )

    client_agi = st.number_input("Client AGI ($)", min_value=0, value=75000, step=1000)
    client_tax = st.number_input("Client Federal Tax Paid ($)", min_value=0, value=8500, step=100)
    client_charitable = st.number_input("Client Charitable Contributions ($)", min_value=0, value=0, step=100)

    zip_data = df[(df["zipcode"] == zip_input.zfill(5)) & (df["agi_stub"] == agi_stub)]

    if zip_data.empty:
        st.warning(
            f"No IRS SOI data found for ZIP code {zip_input} in the selected AGI bracket. "
            "Try an adjacent bracket or a different ZIP."
        )
        return

    peer_avg_agi = zip_data["avg_agi"].values[0] if not pd.isna(zip_data["avg_agi"].values[0]) else 0
    peer_avg_tax = zip_data["avg_tax"].values[0] if not pd.isna(zip_data["avg_tax"].values[0]) else 0
    peer_eff_rate = zip_data["effective_rate"].values[0] if not pd.isna(zip_data["effective_rate"].values[0]) else 0
    peer_charitable = zip_data["avg_charitable"].values[0] if not pd.isna(zip_data["avg_charitable"].values[0]) else 0
    num_returns = zip_data["N1"].values[0]

    client_eff_rate = client_tax / client_agi if client_agi > 0 else 0

    st.markdown(f"### Results for ZIP {zip_input} -- {int(num_returns):,} returns in this bracket")

    metrics = ["AGI", "Federal Tax Paid", "Effective Tax Rate (%)", "Charitable Contributions"]
    client_vals = [client_agi, client_tax, client_eff_rate * 100, client_charitable]
    peer_vals = [peer_avg_agi, peer_avg_tax, peer_eff_rate * 100, peer_charitable]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Your Client", x=metrics, y=client_vals, marker_color="#1f3a5f"))
    fig.add_trace(go.Bar(name=f"ZIP {zip_input} Avg (IRS SOI)", x=metrics, y=peer_vals, marker_color="#a8c4e0"))
    fig.update_layout(
        barmode="group",
        title=f"Client vs. ZIP Code Peers -- {zip_input}",
        yaxis_title="Amount / Rate",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Key Observations")
    if client_eff_rate > peer_eff_rate * 1.1:
        st.warning(
            f"Client effective rate ({client_eff_rate:.1%}) is above the ZIP average "
            f"({peer_eff_rate:.1%}). Review deduction optimization."
        )
    elif client_eff_rate < peer_eff_rate * 0.9:
        st.success(
            f"Client effective rate ({client_eff_rate:.1%}) is below the ZIP average "
            f"({peer_eff_rate:.1%}). Return is well-optimized relative to peers."
        )
    else:
        st.info(
            f"Client effective rate ({client_eff_rate:.1%}) is in line with the ZIP average "
            f"({peer_eff_rate:.1%})."
        )

    if client_charitable > peer_charitable * 1.5 and client_charitable > 0:
        st.warning(
            f"Client charitable contributions (${client_charitable:,.0f}) are significantly "
            f"above the peer average (${peer_charitable:,.0f}). Ensure documentation is "
            "thorough -- this may elevate DIF score."
        )
