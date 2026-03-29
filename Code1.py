import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("📱 Telemedicine App Users Growth & Load Analysis")

# Sidebar Inputs (Sensitivity Analysis)
st.sidebar.header("📊 Input Parameters")

initial_users = st.sidebar.slider("Initial Users", 100, 10000, 500)
growth_rate = st.sidebar.slider("Growth Rate (%)", 1, 50, 10)
days = st.sidebar.slider("Number of Days", 10, 180, 60)
max_capacity = st.sidebar.slider("Max Daily Capacity", 500, 20000, 5000)
marketing_boost = st.sidebar.slider("Marketing Boost (%)", 0, 50, 10)

# Growth Model
user_data = []
users = initial_users

for day in range(days):
    # Apply growth
    users = users * (1 + growth_rate / 100)
    
    # Marketing effect every 10 days
    if day % 10 == 0 and day != 0:
        users += users * (marketing_boost / 100)
    
    user_data.append(users)

# Convert to DataFrame
df = pd.DataFrame({
    "Day": np.arange(1, days + 1),
    "Active Users": user_data
})

# Simulate Appointments (assume 30% users book appointments)
df["Daily Appointments"] = df["Active Users"] * 0.3

# Peak Load Detection
peak_day = df["Daily Appointments"].idxmax()
peak_value = df["Daily Appointments"].max()

# Show Data
st.subheader("📋 Data Table")
st.write(df)

# Plot Graph
st.subheader("📈 Growth & Load Graph")

plt.figure()
plt.plot(df["Day"], df["Active Users"], label="Active Users")
plt.plot(df["Day"], df["Daily Appointments"], label="Appointments")
plt.axhline(y=max_capacity, linestyle='--', label="Max Capacity")

plt.xlabel("Days")
plt.ylabel("Users / Appointments")
plt.legend()

st.pyplot(plt)

# Peak Info
st.subheader("⚡ Peak Load Analysis")
st.write(f"📅 Peak Day: {peak_day + 1}")
st.write(f"📊 Peak Appointments: {int(peak_value)}")

# Capacity Warning
if peak_value > max_capacity:
    st.error("⚠️ Capacity Exceeded! System may crash or slow down.")
else:
    st.success("✅ System is within safe capacity.")
