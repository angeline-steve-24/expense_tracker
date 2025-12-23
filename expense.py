import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💰 Expense Tracker with Visuals")

# Upload CSV
uploaded_file = st.file_uploader("Upload Expense CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Clean data
    df["Date"] = pd.to_datetime(df["Date"])
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df.dropna(inplace=True)

    st.subheader("📊 Raw Data")
    st.dataframe(df)

    # Budget input
    budget = st.number_input("Set Monthly Budget", min_value=0)

    total_expense = df["Amount"].sum()
    st.metric("Total Expenses", f"₹{total_expense}")

    if budget > 0 and total_expense > budget:
        st.error("⚠ Budget Exceeded!")

    # Group by category
    category_summary = df.groupby("Category")["Amount"].sum()

    st.subheader("📈 Expenses by Category")
    fig1, ax1 = plt.subplots()
    category_summary.plot(kind="bar", ax=ax1)
    st.pyplot(fig1)

    st.subheader("🥧 Expense Distribution")
    fig2, ax2 = plt.subplots()
    category_summary.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

    # Export to Excel
    excel_file = "expense_report.xlsx"
    df.to_excel(excel_file, index=False)
    st.download_button("📥 Download Excel Report", open(excel_file, "rb"))
