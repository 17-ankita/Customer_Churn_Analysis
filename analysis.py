import pandas as pd

df = pd.read_excel("dashboards.xlsx")

print("=" * 60)
print("TELCO CUSTOMER CHURN ANALYSIS")
print("=" * 60)

print("\nDataset Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

total_customers = len(df)
churn_customers = len(df[df["Churn Label"] == "Yes"])
churn_rate = churn_customers / total_customers * 100

print("\nTotal Customers:", total_customers)
print("Churn Customers:", churn_customers)
print(f"Churn Rate: {churn_rate:.2f}%")

contract = df.groupby("Contract").agg(
    Customers=("CustomerID", "count"),
    Avg_Monthly_Charge=("Monthly Charge", "mean")
).reset_index()

print("\nContract Analysis")
print(contract)

internet = df.groupby("Internet Type").agg(
    Customers=("CustomerID", "count"),
    Avg_Charge=("Monthly Charge", "mean")
).reset_index()

print("\nInternet Type Analysis")
print(internet)

payment = df.groupby("Payment Method").agg(
    Customers=("CustomerID", "count"),
    Avg_Charge=("Monthly Charge", "mean")
).reset_index()

print("\nPayment Method Analysis")
print(payment)
