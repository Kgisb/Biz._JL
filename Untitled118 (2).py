import pandas as pd
import streamlit as st

# Load data from Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=908334443"
try:
    df = pd.read_csv(sheet_url)
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Validate if AC_Name column exists
if 'AC_Name' not in df.columns:
    st.error("Column 'AC_Name' not found in the dataset. Please check the data source.")
    st.stop()

# Streamlit App
st.title("Interactive AC_Name Filter")

# Display dropdown to select an AC_Name
selected_ac = st.selectbox("Select an AC_Name:", df['AC_Name'].dropna().unique())

# Filter data based on the selected AC_Name
filtered_data = df[df['AC_Name'] == selected_ac]

# Display filtered data
st.subheader(f"Data for AC_Name: {selected_ac}")
st.dataframe(filtered_data)

# Summarize the filtered data
if not filtered_data.empty:
    st.subheader("Summary of Selected AC Data")
    summary = {
        "Total Target (Cash-in)": filtered_data.filter(like="Target (Cash-in)").sum().sum(),
        "Total Achieved (Cash-in)": filtered_data.filter(like="Achv (Cash-in)").sum().sum(),
        "Total Target (Enrl)": filtered_data.filter(like="Target (Enrl)").sum().sum(),
        "Total Achieved (Enrl)": filtered_data.filter(like="Achv (Enrl)").sum().sum(),
        "Total Target (Self. Gen. Deal)": filtered_data.filter(like="Target (Self. Gen. Deal)").sum().sum(),
        "Total Achieved (Self. Gen. Deal)": filtered_data.filter(like="Achv (Self. Gen. Deal)").sum().sum(),
    }
    summary_df = pd.DataFrame([summary])
    st.table(summary_df)
else:
    st.warning("No data available for the selected AC_Name.")
