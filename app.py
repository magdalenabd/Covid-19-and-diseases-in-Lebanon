import streamlit as st
import pandas as pd
import numpy as np
import math
import random

# Set page title
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

# File path to your dataset
csv_path = r"C:\Users\magda\Desktop\dataset (1).csv"

# Load the dataset
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"File not found at path: {csv_path}")
    st.stop()

# Title & Intro
st.title("🦠 COVID-19 and Chronic Diseases Across  Different Regions In Lebanon")

st.markdown("""
Welcome to the **Lebanon COVID-19 Dashboard**, an interactive exploration of how COVID-19 cases intersect with chronic diseases across Lebanese regions.

This dashboard focuses on three chronic conditions:
- **Hypertension**
- **Cardiovascular Disease**
- **Diabetes**

Use the sidebar to adjust the case threshold and select specific chronic conditions. The visualizations will respond dynamically.
""")

# --- INTERACTIVE SLIDER ---
max_cases = int(df["Nb of Covid-19 cases"].max())
min_cases = int(df["Nb of Covid-19 cases"].min())

st.sidebar.header("🔎 Filters")
case_threshold = st.sidebar.slider("Minimum Number of COVID-19 Cases", min_value=min_cases, max_value=max_cases, value=min_cases)

filtered_df = df[df["Nb of Covid-19 cases"] >= case_threshold]

# --- PIE CHART SECTION ---
st.subheader(f"📊 Regions with ≥ {case_threshold} COVID-19 Cases")

if filtered_df.empty:
    st.warning("No regions meet this threshold.")
else:
    fig_pie = px.pie(
        filtered_df,
        values='Nb of Covid-19 cases',
        names='refArea',
        title=f'COVID-19 Case Distribution (Threshold ≥ {case_threshold})',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- CHRONIC DISEASE SELECTION ---
st.subheader("🏥 Focus on Chronic Conditions")

disease_options = [
    "Existence of chronic diseases - Hypertension",
    "Existence of chronic diseases - Cardiovascular disease ",
    "Existence of chronic diseases - Diabetes "
]
selected_diseases = st.sidebar.multiselect("Select Chronic Diseases to Visualize", disease_options, default=disease_options)

if selected_diseases:
    # Prepare the data
    grouped_df = df.groupby('refArea')[selected_diseases].sum().reset_index()
    grouped_df["Total"] = grouped_df[selected_diseases].sum(axis=1)
    grouped_df = grouped_df.sort_values(by="Total", ascending=False)

    # Stacked bar chart
    fig_bar = px.bar(
        grouped_df,
        y="refArea",
        x=selected_diseases,
        title="Chronic Disease Cases by Region",
        labels={"value": "Number of People", "refArea": "Region"},
        barmode="stack",
        orientation="h",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("""
    The chart above highlights how chronic conditions are distributed across regions.  
   
    """)
else:
    st.info("Please select at least one chronic disease from the sidebar.")

# --- Footer ---
st.markdown("""
---
🧑‍💻 **Developed by Magdalena Bodouris**

If you have any questions or feedback about this dashboard, feel free to reach out at magdalena.bodouris@yahoo.com
""")
