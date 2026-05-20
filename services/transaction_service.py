from database.db import get_db_connection


# GET ALL TRANSACTIONS OF LOGGED-IN USER
def get_all_transactions(logged_in_customer_id):

    conn = get_db_connection()

    transactions = conn.execute(
        '''
        SELECT transactions.*
        FROM transactions
        JOIN accounts
        ON transactions.account_id = accounts.account_id
        WHERE accounts.customer_id = ?
        ''',
        (logged_in_customer_id,)
    ).fetchall()

    conn.close()

    return [dict(transaction) for transaction in transactions]


# CREATE NEW TRANSACTION
def create_new_transaction(
    logged_in_customer_id,
    account_id,
    transaction_type,
    amount
):

    conn = get_db_connection()

    try:

        account = conn.execute(
            '''
            SELECT *
            FROM accounts
            WHERE account_id = ?
            ''',
            (account_id,)
        ).fetchone()

        if account is None:

            return {
                "error": "Account not found"
            }

        # OWNERSHIP VALIDATION
        if account['customer_id'] != logged_in_customer_id:

            return {
                "error": "Unauthorized access to this account"
            }

        if amount <= 0:

            return {
                "error": "Amount must be greater than zero"
            }

        conn.execute(
            '''
            INSERT INTO transactions
            (account_id, transaction_type, amount)
            VALUES (?, ?, ?)
            ''',
            (
                account_id,
                transaction_type,
                amount
            )
        )

        conn.commit()

        return {
            "message": "Transaction created successfully"
        }

    except Exception as e:

        conn.rollback()

        return {
            "error": str(e)
        }

    finally:

        conn.close()


# DEPOSIT MONEY
def deposit_money(
    logged_in_customer_id,
    account_id,
    amount
):

    conn = get_db_connection()

    try:

        account = conn.execute(
            '''
            SELECT * 
            FROM accounts
            WHERE account_id = ?
            ''',
            (account_id,)
        ).fetchone()

        if account is None:

            return {
                "error": "Account does not exist"
            }

        # OWNERSHIP VALIDATION
        if account['customer_id'] != logged_in_customer_id:

            return {
                "error": "Unauthorized access to this account"
            }

        if amount <= 0:

            return {
                "error": "Amount must be greater than zero"
            }

        # UPDATE ACCOUNT BALANCE
        conn.execute(
            '''
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_id = ?
            ''',
            (amount, account_id)
        )

        # INSERT TRANSACTION HISTORY
        conn.execute(
            '''
            INSERT INTO transactions
            (account_id, transaction_type, amount)
            VALUES (?, ?, ?)
            ''',
            (account_id, 'Deposit', amount)
        )

        conn.commit()

        return {
            "message": "Deposit successful"
        }

    except Exception as e:

        conn.rollback()

        return {
            "error": str(e)
        }

    finally:

        conn.close()


# TRANSFER FUNDS
def transfer_funds(
    logged_in_customer_id,
    sender_account_id,
    receiver_account_id,
    amount
):

    conn = get_db_connection()

    try:

        sender = conn.execute(
            '''
            SELECT * 
            FROM accounts
            WHERE account_id = ?
            ''',
            (sender_account_id,)
        ).fetchone()

        receiver = conn.execute(
            '''
            SELECT * 
            FROM accounts
            WHERE account_id = ?
            ''',
            (receiver_account_id,)
        ).fetchone()

        if sender is None:

            return {
                "error": "Sender account does not exist"
            }

        if receiver is None:

            return {
                "error": "Receiver account not found"
            }

        # OWNERSHIP VALIDATION
        if sender['customer_id'] != logged_in_customer_id:

            return {
                "error": "Unauthorized access to this account"
            }

        if amount <= 0:

            return {
                "error": "Amount must be greater than zero"
            }

        if sender['balance'] < amount:

            return {
                "error": "Insufficient balance"
            }

        # SUBTRACT MONEY
        conn.execute(
            '''
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_id = ?
            ''',
            (amount, sender_account_id)
        )

        # ADD MONEY
        conn.execute(
            '''
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_id = ?
            ''',
            (amount, receiver_account_id)
        )

        # WITHDRAW HISTORY
        conn.execute(
            '''
            INSERT INTO transactions
            (account_id, transaction_type, amount)
            VALUES (?, ?, ?)
            ''',
            (sender_account_id, 'Withdraw', amount)
        )

        # DEPOSIT HISTORY
        conn.execute(
            '''
            INSERT INTO transactions
            (account_id, transaction_type, amount)
            VALUES (?, ?, ?)
            ''',
            (receiver_account_id, 'Deposit', amount)
        )

        conn.commit()

        return {
            "message": "Transfer successful"
        }

    except Exception as e:

        conn.rollback()

        return {
            "error": str(e)
        }

    finally:

        conn.close()


# WITHDRAW MONEY
def withdraw_any_funds(
    logged_in_customer_id,
    account_id,
    amount
):

    conn = get_db_connection()

    try:

        account = conn.execute(
            '''
            SELECT *
            FROM accounts
            WHERE account_id = ?
            ''',
            (account_id,)
        ).fetchone()

        if account is None:

            return {
                "error": "Account not found"
            }

        # OWNERSHIP VALIDATION
        if account['customer_id'] != logged_in_customer_id:

            return {
                "error": "Unauthorized access to this account"
            }

        if amount <= 0:

            return {
                "error": "Amount must be greater than zero"
            }

        if account['balance'] < amount:

            return {
                "error": "Insufficient balance"
            }

        # UPDATE BALANCE
        conn.execute(
            '''
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_id = ?
            ''',
            (amount, account_id)
        )

        # INSERT TRANSACTION
        conn.execute(
            '''
            INSERT INTO transactions
            (account_id, transaction_type, amount)
            VALUES (?, ?, ?)
            ''',
            (account_id, 'Withdraw', amount)
        )

        conn.commit()

        return {
            "message": "Withdraw successful"
        }

    except Exception as e:

        conn.rollback()

        return {
            "error": str(e)
        }

    finally:

        conn.close()