import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Telco Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("dashboards.xlsx")

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    rename_map = {
        "Customer_ID": "CustomerID",
        "customerID": "CustomerID",
        "MonthlyCharges": "Monthly_Charge",
        "Monthly_Charges": "Monthly_Charge",
        "Monthly_Charge": "Monthly_Charge",
        "Churn": "Churn_Label",
        "Churn_Label": "Churn_Label",
        "Tenure": "Tenure_Months",
        "tenure": "Tenure_Months",
        "Tenure_Months": "Tenure_Months",
        "InternetService": "Internet_Type",
        "Internet_Service": "Internet_Type",
        "Internet_Type": "Internet_Type",
        "PaymentMethod": "Payment_Method",
        "Payment_Method": "Payment_Method"
    }

    df = df.rename(columns=rename_map)

    if "CustomerID" not in df.columns:
        df["CustomerID"] = "Customer_" + (df.index + 1).astype(str)

    if "Churn_Label" not in df.columns:
        df["Churn_Label"] = "No"

    if "Monthly_Charge" not in df.columns:
        df["Monthly_Charge"] = 0

    if "Tenure_Months" not in df.columns:
        df["Tenure_Months"] = 0

    if "Contract" not in df.columns:
        df["Contract"] = "Unknown"

    if "Gender" not in df.columns:
        df["Gender"] = "Unknown"

    if "Internet_Type" not in df.columns:
        df["Internet_Type"] = "Unknown"

    if "Payment_Method" not in df.columns:
        df["Payment_Method"] = "Unknown"

    df["Monthly_Charge"] = pd.to_numeric(df["Monthly_Charge"], errors="coerce").fillna(0)
    df["Tenure_Months"] = pd.to_numeric(df["Tenure_Months"], errors="coerce").fillna(0)

    return df


df = load_data()

# ---------------- HEADER ----------------
st.title("Telco Customer Churn Analytics Dashboard")

st.markdown("""
This dashboard analyzes telecom customer churn behavior using **Python, Excel, Streamlit, and Plotly**.
It helps identify churn patterns, customer segments, contract behavior, payment trends, and revenue insights.
""")

# ---------------- KPIs ----------------
total_customers = len(df)
churn_customers = len(df[df["Churn_Label"].astype(str).str.lower().isin(["yes", "true", "1"])])
churn_rate = (churn_customers / total_customers) * 100 if total_customers > 0 else 0
avg_monthly = df["Monthly_Charge"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Churn Customers", churn_customers)
col3.metric("Churn Rate", f"{churn_rate:.2f}%")
col4.metric("Avg Monthly Charge", f"${avg_monthly:.2f}")

st.divider()

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs([
    "Overview",
    "Customer Segments",
    "Revenue Insights"
])

with tab1:
    st.subheader("Churn Overview")

    col1, col2 = st.columns(2)

    with col1:
        churn = df["Churn_Label"].value_counts().reset_index()
        churn.columns = ["Churn", "Count"]

        fig = px.pie(
            churn,
            names="Churn",
            values="Count",
            title="Customer Churn Distribution",
            hole=0.45
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        contract = df.groupby("Contract")["CustomerID"].count().reset_index()
        contract.columns = ["Contract", "Customers"]

        fig = px.bar(
            contract,
            x="Contract",
            y="Customers",
            title="Customers by Contract Type",
            color="Contract"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Customer Segments")

    col1, col2 = st.columns(2)

    with col1:
        gender = df.groupby("Gender")["CustomerID"].count().reset_index()
        gender.columns = ["Gender", "Customers"]

        fig = px.bar(
            gender,
            x="Gender",
            y="Customers",
            title="Customers by Gender",
            color="Gender"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        internet = df.groupby("Internet_Type")["CustomerID"].count().reset_index()
        internet.columns = ["Internet Type", "Customers"]

        fig = px.bar(
            internet,
            x="Internet Type",
            y="Customers",
            title="Internet Type Analysis",
            color="Internet Type"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Revenue Insights")

    payment = df.groupby("Payment_Method")["Monthly_Charge"].mean().reset_index()
    payment.columns = ["Payment Method", "Monthly Charge"]

    fig = px.bar(
        payment,
        x="Payment Method",
        y="Monthly Charge",
        title="Average Monthly Charges by Payment Method",
        color="Payment Method"
    )
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(
        df,
        x="Tenure_Months",
        y="Monthly_Charge",
        color="Churn_Label",
        title="Tenure vs Monthly Charges"
    )
    st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Dataset"):
    st.dataframe(df, use_container_width=True)

with st.expander("View Detected Column Names"):
    st.write(list(df.columns))