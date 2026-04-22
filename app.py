
# app.py -- IRS Data Explorer

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "utils"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "components"))

from data_loader import load_data
import state_view
import zip_benchmarker
import income_brackets

st.set_page_config(
    page_title="IRS Data Explorer",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <div style="background-color:#1f3a5f;padding:24px 32px 16px 32px;border-radius:8px;margin-bottom:24px;">
        <h1 style="color:white;margin:0;font-family:Arial;font-size:28px;">IRS Data Explorer</h1>
        <p style="color:#a8c4e0;margin:6px 0 0 0;font-size:14px;">
        Where Does America Pay Tax? &middot; Powered by IRS Statistics of Income Division (SOI) 2021 Data
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "This dashboard uses real, publicly available IRS Statistics of Income data -- "
    "the same dataset used by tax researchers, government agencies, and academic institutions -- "
    "to surface patterns in how Americans across every income tier and ZIP code file and pay federal taxes."
)

df = load_data()

tab1, tab2, tab3 = st.tabs(["State Tax Map", "ZIP Code Benchmarker", "Income Bracket Analysis"])

with tab1:
    state_view.run(df)
with tab2:
    zip_benchmarker.run(df)
with tab3:
    income_brackets.run(df)

st.markdown(
    """
    <div style="margin-top:40px;padding:12px;background:#f4f6f9;border-radius:6px;font-size:11px;color:#888;">
    Data source: IRS Statistics of Income Division -- 2021 Individual Income Tax ZIP Code Data.
    Published annually at irs.gov/statistics. All figures represent aggregated, anonymized tax return data.
    </div>
    """,
    unsafe_allow_html=True,
)
