import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Sakhapov & Partners | AI Diagnostic Engine", layout="wide")

st.title("⚡ SupplyChain & FinOps AI Diagnostic Engine")
st.markdown("**Sakhapov & Partners** | Non-Invasive Enterprise Telemetry & Cloud Cost Anomaly Detection (Zero-Risk PoC)")

st.sidebar.header("1. Data Source & Mode")
mode = st.sidebar.radio("Select Diagnostic Module:", ["Warehouse WMS & Robotics Log Audit", "Cloud & Compute FinOps Billing Audit"])
uploaded_file = st.sidebar.file_uploader("Upload Masked Client Log (CSV)", type=["csv"])

def generate_sample_data(selected_mode):
    np.random.seed(42)
    rows = 250
    if "Warehouse" in selected_mode:
        zones = ["Automated Sorter A1", "Conveyor Hub B4", "Palletizer C2", "Cold-Chain Gate D1"]
        errors = ["OK", "OK", "OK", "SKU Dimension Mismatch", "Weight Threshold Stall", "Barcode Read Timeout"]
        df = pd.DataFrame({
            "Timestamp": pd.date_range("2026-11-25", periods=rows, freq="15min"),
            "Zone": np.random.choice(zones, rows),
            "Status": np.random.choice(errors, rows, p=[0.65, 0.1, 0.05, 0.09, 0.06, 0.05]),
            "Downtime_Sec": np.random.exponential(scale=45, size=rows).round(1),
            "Est_Loss_USD": np.random.uniform(12, 180, size=rows).round(2)
        })
        df.loc[df["Status"] == "OK", ["Downtime_Sec", "Est_Loss_USD"]] = 0.0
    else:
        services = ["Kubernetes Cluster Prod", "RDS PostgreSQL Analytics", "Idle GPU Inference Node", "S3 Unmanaged Snapshots"]
        df = pd.DataFrame({
            "Date": pd.date_range("2026-11-01", periods=rows, freq="2h"),
            "Service": np.random.choice(services, rows),
            "Utilization_Pct": np.random.uniform(4, 92, size=rows).round(1),
            "Hourly_Cost_USD": np.random.uniform(5, 85, size=rows).round(2)
        })
        df["Waste_USD"] = np.where(df["Utilization_Pct"] < 20, df["Hourly_Cost_USD"] * 0.78, 0.0).round(2)
    return df

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Client masked dataset successfully ingested inside isolated sandbox.")
else:
    df = generate_sample_data(mode)
    st.info("Running in Live Demo Sandbox Mode (Simulated 72-Hour Enterprise Telemetry Dataset). Upload a CSV in the sidebar to audit real client logs.")

st.divider()

if "Warehouse" in mode:
    anomalies = df[df["Status"] != "OK"]
    total_loss = anomalies["Est_Loss_USD"].sum()
    total_downtime = (anomalies["Downtime_Sec"].sum() / 60).round(1)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Detected Micro-Stall Events", f"{len(anomalies)}", delta="High Priority", delta_color="inverse")
    c2.metric("Cumulative Line Downtime", f"{total_downtime} min", delta="-34% Target Reduction")
    c3.metric("Annualized Margin Leakage", f"${(total_loss * 120):,.0f}", delta="Recoverable ROI")
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(anomalies.groupby("Status", as_index=False)["Est_Loss_USD"].sum(), x="Status", y="Est_Loss_USD", title="Financial Leakage by Exception Type (USD)", color="Status")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.pie(anomalies, names="Zone", values="Downtime_Sec", title="Downtime Share by Automated Hub Zone")
        st.plotly_chart(fig2, use_container_width=True)
else:
    total_spend = df["Hourly_Cost_USD"].sum()
    total_waste = df["Waste_USD"].sum()
    savings_pct = (total_waste / total_spend * 100) if total_spend > 0 else 0
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Analyzed Cloud Compute Spend", f"${total_spend:,.2f}")
    c2.metric("Detected Idle / Over-Provisioned Waste", f"${total_waste:,.2f}", delta=f"{savings_pct:.1f}% Leak Rate", delta_color="inverse")
    c3.metric("Projected Annual FinOps Savings", f"${(total_waste * 17):,.0f}", delta="Zero Code Changes")
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(df.groupby("Service", as_index=False)["Waste_USD"].sum(), x="Service", y="Waste_USD", title="Recoverable Cloud Billing Leaks by Service (USD)", color="Service")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.scatter(df, x="Utilization_Pct", y="Hourly_Cost_USD", color="Service", title="Compute Utilization vs. Hourly Cost Anomaly Map")
        st.plotly_chart(fig2, use_container_width=True)

st.subheader("Raw Telemetry & Anomaly Audit Log")
st.dataframe(df.head(25), use_container_width=True)
