# IRS Data Explorer -- Where Does America Pay Tax?

**A data analytics dashboard powered by real IRS Statistics of Income (SOI) public data.**

---

## What Is This?

The IRS Data Explorer visualizes the IRS Statistics of Income (SOI) Individual Income Tax ZIP Code
dataset -- the same data used by tax researchers, government agencies, and policy analysts -- to
surface meaningful patterns in how Americans across every income tier and geography file and pay
federal taxes.

This is not simulated data. Every number in this dashboard comes directly from the IRS.

---

## Why Does It Exist?

Tax professionals are expected to understand not just their client's return in isolation, but in
context. How does this client's effective rate compare to their neighbors? Which income brackets
drive EITC utilization? Where is charitable giving disproportionately high relative to income?

This tool answers those questions with the same source material a senior tax analyst would reference.

---

## The Three Views

### State Tax Map
An interactive choropleth map of the United States displaying effective tax rates, average AGI,
average federal tax paid, EITC utilization, and charitable contributions by state. Toggle between
metrics to explore the national distribution.

### ZIP Code Benchmarker
Enter any client ZIP code, AGI bracket, and key return figures. The tool instantly compares them
against the IRS-reported averages for every filer in that ZIP code and income tier. Flags deviations
that may indicate optimization opportunities or elevated audit risk relative to peers.

### Income Bracket Analysis
Examines how tax burdens, EITC utilization rates, and charitable giving patterns shift across the
six IRS AGI tiers. Surfaces the structural effects of the progressive rate schedule and phase-out
mechanics embedded in current law.

---

## What Does This Tell Us?

Effective tax rates rise with income but not linearly -- phase-outs, credit cliffs, and deduction
incentives create distinct behavioral patterns at each tier. EITC utilization collapses above $50K
as expected. Charitable contributions accelerate sharply at $200K+ where itemizing produces greater
marginal benefit. These are not academic observations -- they are the patterns that inform client
advisory conversations at every major accounting firm.

---

## Data Source

IRS Statistics of Income Division -- 2021 Individual Income Tax ZIP Code Data.
Published annually at: https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-zip-code-data-soi

Column definitions follow the IRS SOI Data Dictionary (21zpdoc.doc).

---

## Technical Stack

- Python -- data processing and metric computation
- Streamlit -- interactive dashboard
- Plotly -- choropleth maps, bar charts, comparative visualizations
- Pandas / NumPy -- data aggregation and transformation

---

*Built by Prakash Balasubramanian -- Mathematics and Statistics, UMBC | IRS VITA Certified Tax Preparer*
