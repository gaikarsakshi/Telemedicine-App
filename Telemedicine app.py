import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("📱 Telemedicine App Users Growth & Load Analysis")

# Sidebar Inputs
st.sidebar.header("📊 Input Parameters")

initial_users = st.sidebar.slider("Initial Users", 100, 500, 200)
growth_rate = st.sidebar.slider("Growth Rate (%)", 1, 20, 5)
days = st.sidebar.slider("Number of Days", 10, 80, 60)
max_capacity = st.sidebar.slider("Max Daily Capacity", 100, 500, 300)
marketing_boost = st.sidebar.slider("Marketing Boost (%)", 0, 30, 10)
carrying_capacity = st.sidebar.slider("Max User Limit", 500, 2000, 1000)

# Growth Model (Controlled Growth)
user_data = []
users = initial_users

for day in range(days):
    # Logistic Growth
    users = users + (growth_rate/100) * users * (1 - users / carrying_capacity)

    # Marketing boost every 10 days
    if day % 10 == 0 and day != 0:
        users += users * (marketing_boost / 100)

    # Limit users
    users = min(users, carrying_capacity)

    user_data.append(users)

# DataFrame
df = pd.DataFrame({
    "Day": np.arange(1, days + 1),
    "Active Users": np.round(user_data)
})

# Appointments (30%)
df["Daily Appointments"] = (df["Active Users"] * 0.3).astype(int)

# Peak Load
peak_day = df["Daily Appointments"].idxmax()
peak_value = df["Daily Appointments"].max()

# Show Data
st.subheader("📋 Data Table")
st.write(df)

# ------------------ GRAPH 1 ------------------
st.subheader("📈 Active Users Growth")

plt.figure()
plt.plot(df["Day"], df["Active Users"], label="Active Users")
plt.xlabel("Days")
plt.ylabel("Users")
plt.title("Active Users Growth")
plt.grid(True)
plt.legend()

st.pyplot(plt)

# ------------------ GRAPH 2 ------------------
st.subheader("📊 Daily Appointments Load")

plt.figure()
plt.plot(df["Day"], df["Daily Appointments"], label="Appointments")
plt.axhline(y=max_capacity, linestyle='--', label="Max Capacity")
plt.xlabel("Days")
plt.ylabel("Appointments")
plt.title("Appointments vs Capacity")
plt.grid(True)
plt.legend()

st.pyplot(plt)

# Peak Info
st.subheader("⚡ Peak Load Analysis")
st.write(f"📅 Peak Day: {peak_day + 1}")
st.write(f"📊 Peak Appointments: {int(peak_value)}")

# Capacity Check
if peak_value > max_capacity:
    st.error("⚠️ Capacity Exceeded! System may slow down.")
else:
    st.success("✅ System is within safe capacity.")
