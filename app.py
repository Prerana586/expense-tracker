import streamlit as st
from llm import parse_expense, generate_insights
from storage import init_db, save_expense, fetch_all
from analytics import summarize, alert_overspend

init_db()

st.title("💰 Smart Expense Tracker")

# Add Expense Section
st.header("Add Expense")
text = st.text_input("Describe your expense in plain English",
                     placeholder="e.g. Spent 12.50 on lunch yesterday")

if st.button("Add Expense"):
    if text:
        with st.spinner("Parsing with AI..."):
            try:
                expense = parse_expense(text)
                save_expense(expense)
                st.success(f"✓ Saved ${expense['amount']:.2f} • {expense['category']} • {expense['date']}")
            except Exception as e:
                st.error(f"Could not parse: {e}")
    else:
        st.warning("Please enter an expense description.")

st.divider()

# Summary Section
st.header("📊 Summary")
expenses = fetch_all()

if not expenses:
    st.info("No expenses yet. Add some above!")
else:
    summary = summarize(expenses)

    # Metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"${summary['total_spent']:.2f}")
    col2.metric("Expenses", summary['expense_count'])
    col3.metric("Top Category", summary['top_category'].title())

    # Alert
    alert = alert_overspend(summary)
    if alert:
        st.warning(alert)

    # Category table
    st.subheader("By Category")
    import pandas as pd
    df = pd.DataFrame(
        [(k.title(), f"${v:.2f}") for k, v in
         sorted(summary["by_category"].items(), key=lambda x: -x[1])],
        columns=["Category", "Amount"]
    )
    st.table(df)

    # Monthly chart
    if summary["by_month"]:
        st.subheader("Monthly Spending")
        monthly_df = pd.DataFrame(
            list(summary["by_month"].items()),
            columns=["Month", "Amount"]
        )
        st.bar_chart(monthly_df.set_index("Month"))

    # AI Insights
    st.subheader("🤖 AI Insights")
    if st.button("Generate Insights"):
        with st.spinner("Analyzing your expenses..."):
            insights = generate_insights(summary)
            st.write(insights)

    # Expense history
    st.subheader("All Expenses")
    history_df = pd.DataFrame(expenses)
    st.dataframe(history_df[["date","category","description","amount"]], hide_index=True)