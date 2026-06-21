import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Hospital Readmission Dashboard",
    page_icon="🏥",
    layout="wide"
)

df = pd.read_csv("Hospital_Readmission_Cleaned.csv")

# Title
st.title("🏥 30-Day Hospital Readmission Dashboard")
st.markdown(
    "This dashboard analyzes 30-day hospital readmissions using demographic, clinical, and admission-related factors."
)

st.divider()

# creating sidebar
st.sidebar.header("Filters")
# creating gender filter
gender=st.sidebar.multiselect("Select Gender", options=df["Gender"].unique(),
    default=df["Gender"].unique())

insurance = st.sidebar.multiselect(
    "Select Insurance Type",
    options=df["Insurance_Type"].unique(),
    default=df["Insurance_Type"].unique()
)

admission = st.sidebar.multiselect(
    "Select Admission Type",
    options=df["Admission_Type"].unique(),
    default=df["Admission_Type"].unique()
)

filtered_df = df[
    (df["Gender"].isin(gender)) &
    (df["Insurance_Type"].isin(insurance)) &
    (df["Admission_Type"].isin(admission))
]

# Creating KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    # st.metric("Total Patients", len(df))
    st.metric("Total Patients", len(filtered_df))


with col2:
    readmission_rate = filtered_df["Readmitted_Within_30_Days"].mean()*100
    st.metric("Readmission Rate", f"{readmission_rate:.2f}%")

with col3:
    st.metric("Avg LOS", round(filtered_df["Length_of_Stay"].mean(),2))

with col4:
    st.metric("Avg Severity", round(filtered_df["Severity_Score"].mean(),2))

with col5:
    st.metric("Avg Comorbidity", round(filtered_df["Comorbidity_Index"].mean(),2))

st.subheader("Patient Records")
st.dataframe(filtered_df)

st.subheader("Readmission Rate by Insurance Type")


insurance_readmission = (
    filtered_df.groupby("Insurance_Type")["Readmitted_Within_30_Days"]
    .mean()
    .reset_index()
)

fig = px.bar(
    insurance_readmission,
    x="Insurance_Type",
    y="Readmitted_Within_30_Days",
    
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Readmission Rate by Severity Score")
severity_readmission = (
    filtered_df.groupby("Severity_Score")["Readmitted_Within_30_Days"]
    .mean()
    .reset_index()
)

fig = px.line(
    severity_readmission,
    x="Severity_Score",
    y="Readmitted_Within_30_Days",
    
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Readmission Rate by Diagnosis")

diag = (
    filtered_df.groupby("Primary_Diagnosis_Group")["Readmitted_Within_30_Days"]
    .mean()
    .reset_index()
)

fig1 = px.bar(
    diag,
    x="Primary_Diagnosis_Group",
    y="Readmitted_Within_30_Days",
    color="Primary_Diagnosis_Group"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Readmission Rate by Insurance Type")

ins = (
    filtered_df.groupby("Insurance_Type")["Readmitted_Within_30_Days"]
    .mean()
    .reset_index()
)

fig2 = px.pie(
    ins,
    names="Insurance_Type",
    values="Readmitted_Within_30_Days"
)

st.plotly_chart(fig2, use_container_width=True)