
import pandas as pd
import streamlit as st
import altair as alt

# Load your final database
file_path = 'HSI_Funders_Database_Final.xlsx'
df = pd.read_excel(file_path)

# Streamlit App Setup
st.set_page_config(page_title="Health Systems Innovation Venture Funding", layout="wide")

# Layout for centered logo and title
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.write("")
with col2:
    st.image('HSPH_HSIL_logo_horiz_RGB.png', width=500)
    st.markdown("<h1 style='text-align: center;'>Health Systems Innovation Venture Funding</h1>", unsafe_allow_html=True)
with col3:
    st.write("")

# Sidebar Filters
st.sidebar.header("Filter Options")

country_filter = st.sidebar.multiselect(
    "Select Country:",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)

funding_type_filter = st.sidebar.multiselect(
    "Select Funding Type:",
    options=df["Funding type"].unique(),
    default=df["Funding type"].unique()
)

name_search = st.sidebar.text_input("Search by Funder Name:")

# Filter the data
filtered_df = df[
    (df["Country"].isin(country_filter)) &
    (df["Funding type"].isin(funding_type_filter))
]

if name_search:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(name_search, case=False, na=False)]

# Display Data
st.subheader(f"Showing {len(filtered_df)} Funders")
st.dataframe(filtered_df, use_container_width=True)

# Bar Chart: Funders by Country
st.subheader("Funders by Country")
country_chart = (
    alt.Chart(filtered_df)
    .mark_bar()
    .encode(
        x=alt.X("count():Q", title="Number of Funders"),
        y=alt.Y("Country:N", sort="-x"),
        tooltip=["Country", "count():Q"]
    )
    .properties(height=400)
)
st.altair_chart(country_chart, use_container_width=True)

# Pie Chart: Funders by Funding Type
st.subheader("Funders by Funding Type")
funding_chart = (
    alt.Chart(filtered_df)
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta(field="Name", aggregate="count"),
        color=alt.Color(field="Funding type"),
        tooltip=["Funding type", "count(Name):Q"]
    )
)
st.altair_chart(funding_chart, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built by Health Systems Innovation Lab, Harvard University, 2025 ©")
