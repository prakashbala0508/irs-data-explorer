
# utils/data_loader.py
# Loads and preprocesses IRS SOI ZIP code data.
# Source: IRS Statistics of Income Division, 2021 Individual Income Tax ZIP Code Data
# Column definitions: https://www.irs.gov/pub/irs-soi/21zpdoc.doc

import pandas as pd
import streamlit as st
import os

AGI_LABELS = {
    1: "Under $25,000",
    2: "$25,000 - $50,000",
    3: "$50,000 - $75,000",
    4: "$75,000 - $100,000",
    5: "$100,000 - $200,000",
    6: "$200,000 or more",
}

STATE_CODES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
}


@st.cache_data(show_spinner="Loading IRS SOI data...")
def load_data() -> pd.DataFrame:
    """
    Loads the IRS SOI 2021 ZIP code CSV, selects key analytical columns,
    computes derived metrics, and returns a clean DataFrame.
    All column names follow the IRS SOI data dictionary (21zpdoc.doc).
    """
    path = os.path.join(os.path.dirname(__file__), "..", "data", "irs_soi_2021_zip.csv")
    df = pd.read_csv(path, dtype={"zipcode": str})

    df["zipcode"] = df["zipcode"].str.zfill(5)
    df["agi_label"] = df["agi_stub"].map(AGI_LABELS)
    df["state_name"] = df["STATE"].map(STATE_CODES)

    df["avg_agi"] = df["A00100"] / df["N1"].replace(0, pd.NA) * 1000
    df["avg_tax"] = df["A10300"] / df["N1"].replace(0, pd.NA) * 1000
    df["effective_rate"] = (df["A10300"] / df["A00100"].replace(0, pd.NA)).clip(0, 1)
    df["avg_charitable"] = df["A17000"] / df["N1"].replace(0, pd.NA) * 1000
    df["eitc_utilization_rate"] = df["N59660"] / df["N1"].replace(0, pd.NA)
    df["avg_eitc"] = df["A59660"] / df["N59660"].replace(0, pd.NA) * 1000

    return df
