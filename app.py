import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Telco Customer Churn Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e293b);
    color: white;
}
[data-testid="metric-container"] {
    background: #111827;
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_excel("dashboards.xlsx")

df = load_data()

st.title("Telco Customer Churn Analytics Dashboard")

# KPI Section
total_customers = len(df)
churn_customers = len(df[df["Churn Label"] == "Yes"])
churn_rate = (churn_customers / total_customers) * 100
avg_monthly = df["Monthly Charge"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Customers", total_customers)
c2.metric("Churn Customers", churn_customers)
c3.metric("Churn Rate", f"{churn_rate:.2f}%")
c4.metric("Avg Monthly Charge", f"${avg_monthly:.2f}")

tab1, tab2, tab3 = st.tabs(["Overview", "Customer Segments", "Revenue Insights"])

with tab1:
    churn = df["Churn Label"].value_counts().reset_index()
    churn.columns = ["Churn", "Count"]

    fig = px.pie(churn, names="Churn", values="Count", hole=0.45,
                 title="Customer Churn Distribution")
    st.plotly_chart(fig, use_container_width=True)

    contract = df.groupby("Contract")["CustomerID"].count().reset_index()
    contract.columns = ["Contract", "Customers"]

    fig2 = px.bar(contract, x="Contract", y="Customers",
                  title="Customers by Contract Type",
                  color="Contract")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    gender = df.groupby("Gender")["CustomerID"].count().reset_index()
    gender.columns = ["Gender", "Customers"]

    fig3 = px.bar(gender, x="Gender", y="Customers",
                  title="Customers by Gender",
                  color="Gender")
    st.plotly_chart(fig3, use_container_width=True)

    internet = df.groupby("Internet Type")["CustomerID"].count().reset_index()
    internet.columns = ["Internet Type", "Customers"]

    fig4 = px.bar(internet, x="Internet Type", y="Customers",
                  title="Internet Type Analysis",
                  color="Internet Type")
    st.plotly_chart(fig4, use_container_width=True)

with tab3:
    payment = df.groupby("Payment Method")["Monthly Charge"].mean().reset_index()

    fig5 = px.bar(payment,
                  x="Payment Method",
                  y="Monthly Charge",
                  title="Average Monthly Charges by Payment Method",
                  color="Payment Method")
    fig5.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig5, use_container_width=True)

    tenure = px.scatter(
        df,
        x="Tenure Months",
        y="Monthly Charge",
        color="Churn Label",
        title="Tenure vs Monthly Charges"
    )
    st.plotly_chart(tenure, use_container_width=True)

with st.expander("View Dataset"):
    st.dataframe(df, use_container_width=True)
