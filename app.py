import streamlit as st
from datetime import date
from database import init_db, get_connection
import reports

st.set_page_config(page_title="Tally-like ERP")

# initialize database
init_db()

st.title("Tally-like ERP")

page = st.sidebar.selectbox("Navigate", ["Accounts", "Transactions", "Reports"])

if page == "Accounts":
    st.header("Manage Accounts")
    with st.form("add_account"):
        name = st.text_input("Account Name")
        acc_type = st.selectbox(
            "Account Type",
            ["Asset", "Liability", "Income", "Expense", "Equity"],
        )
        submitted = st.form_submit_button("Add")
    if submitted and name:
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO accounts (name, type) VALUES (?, ?)",
                (name, acc_type),
            )
            conn.commit()
            st.success("Account added")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()
    conn = get_connection()
    accounts = conn.execute(
        "SELECT id, name, type FROM accounts ORDER BY name"
    ).fetchall()
    conn.close()
    if accounts:
        st.subheader("Existing Accounts")
        st.table(accounts)
    else:
        st.info("No accounts yet.")

elif page == "Transactions":
    st.header("Record Transaction")
    conn = get_connection()
    accounts = conn.execute(
        "SELECT id, name FROM accounts ORDER BY name"
    ).fetchall()
    conn.close()
    if accounts:
        account_map = {f"{a['name']}": a["id"] for a in accounts}
        with st.form("txn"):
            acct_name = st.selectbox("Account", list(account_map.keys()))
            date_val = st.date_input("Date", date.today())
            debit = st.number_input("Debit", min_value=0.0, step=0.01)
            credit = st.number_input("Credit", min_value=0.0, step=0.01)
            desc = st.text_input("Description")
            submitted = st.form_submit_button("Save")
        if submitted:
            conn = get_connection()
            conn.execute(
                "INSERT INTO ledger (date, account_id, debit, credit, description) VALUES (?,?,?,?,?)",
                (date_val.isoformat(), account_map[acct_name], debit, credit, desc),
            )
            conn.commit()
            conn.close()
            st.success("Transaction saved")
    else:
        st.info("Create accounts first.")

elif page == "Reports":
    st.header("Reports")
    report_type = st.selectbox("Report", ["Trial Balance", "Ledger"])
    if report_type == "Trial Balance":
        rows = reports.trial_balance()
        if rows:
            st.table(rows)
        else:
            st.info("No data")
    elif report_type == "Ledger":
        conn = get_connection()
        accounts = conn.execute(
            "SELECT id, name FROM accounts ORDER BY name"
        ).fetchall()
        conn.close()
        if accounts:
            account_map = {f"{a['name']}": a["id"] for a in accounts}
            acct_name = st.selectbox("Account", list(account_map.keys()))
            rows = reports.ledger_report(account_map[acct_name])
            if rows:
                st.table(rows)
            else:
                st.info("No entries for account")
        else:
            st.info("No accounts found")
