from database import get_connection


def trial_balance():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT a.name,
               SUM(l.debit) AS debit,
               SUM(l.credit) AS credit
        FROM accounts a
        LEFT JOIN ledger l ON a.id = l.account_id
        GROUP BY a.id
        ORDER BY a.name
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def ledger_report(account_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT date, debit, credit, description
        FROM ledger
        WHERE account_id = ?
        ORDER BY date
        """,
        (account_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
