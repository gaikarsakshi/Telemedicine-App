# Telemedicine-App
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Telemedicine Dashboard", layout="wide")

# ---------- Custom Styling ----------
st.markdown("""
    <style>
    .metric-box {
        background-color: #f5f7fa;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.title("📱 Telemedicine Analytics Dashboard")
st.markdown("Real-time simulation of **User Growth, Appointments & System Load**")

# ---------- Sidebar ----------
st.sidebar.header("⚙️ Controls")

DAYS = st.sidebar.slider("Days", 100, 365, 365)
BASE_USERS = st.sidebar.number_input("Initial Users", 50, 1000, 200)

growth_rate = st.sidebar.slider("Growth Rate (%/day)", 0.1, 1.0, 0.4) / 100
marketing_boost = st.sidebar.slider("Marketing Boost (%)", 5, 50, 15) / 100
churn_rate = st.sidebar.slider("Churn Rate (%)", 0.0, 1.0, 0.2) / 100

APPOINTMENTS_PER_USER = st.sidebar.slider("Appointments/User", 0.1, 1.0, 0.6)
MAX_CAPACITY = st.sidebar.slider("Max Capacity", 100, 1000, 500)

MARKETING_DAYS = [60, 150, 240, 310]
PEAK_SEASONS = [30, 180, 270, 355]

# ---------- Simulation ----------
def simulate(growth_rate, marketing_boost, churn_rate):
    users, appointments, load = [], [], []
    active = BASE_USERS

    for day in range(DAYS):
        boost = marketing_boost if day in MARKETING_DAYS else 0
        seasonal = 1.25 if day in PEAK_SEASONS else 1.0

        active = active * (1 + growth_rate + boost - churn_rate)
        active = min(active, MAX_CAPACITY / APPOINTMENTS_PER_USER)

        appt = min(active * APPOINTMENTS_PER_USER * seasonal, MAX_CAPACITY)

        users.append(active)
        appointments.append(appt)
        load.append((appt / MAX_CAPACITY) * 100)

    return np.array(users), np.array(appointments), np.array(load)

u1, a1, l1 = simulate(growth_rate, marketing_boost, churn_rate)
u2, a2, l2 = simulate(growth_rate * 1.5, marketing_boost * 2, churn_rate * 0.8)

# ---------- KPI Section ----------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Final Users", int(u1[-1]))
col2.metric("📅 Peak Appointments", int(max(a1)))
col3.metric("⚡ Peak Load", f"{max(l1):.1f}%")
col4.metric("🚨 Days > 80%", int(np.sum(l1 > 80)))

# ---------- Charts ----------
st.subheader("📈 Trends")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    ax.plot(u1, label="Baseline")
    ax.plot(u2, linestyle='--', label="Aggressive")
    ax.set_title("User Growth")
    ax.legend()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    ax.plot(a1, label="Baseline")
    ax.plot(a2, linestyle='--', label="Aggressive")
    ax.axhline(MAX_CAPACITY, linestyle='dashed', label="Capacity")
    ax.set_title("Appointments")
    ax.legend()
    st.pyplot(fig)

# Load Chart
fig, ax = plt.subplots()
ax.plot(l1, label="Baseline")
ax.plot(l2, linestyle='--', label="Aggressive")
ax.axhline(80, linestyle='dashed', label="Risk Level")
ax.set_title("System Load (%)")
ax.legend()
st.pyplot(fig)

# ---------- Sensitivity ----------
st.subheader("📊 Sensitivity Analysis")

growth_rates = np.linspace(0.001, 0.008, 8)
peak_loads = [max(simulate(gr, marketing_boost, churn_rate)[2]) for gr in growth_rates]

fig, ax = plt.subplots()
ax.plot(growth_rates * 100, peak_loads, marker='o')
ax.set_xlabel("Growth Rate (%)")
ax.set_ylabel("Peak Load (%)")
st.pyplot(fig)
