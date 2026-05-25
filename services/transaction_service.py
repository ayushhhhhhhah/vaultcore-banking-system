from faker import Faker
from database.db import get_db_connection
from datetime import datetime
from services.email_service import send_transaction_email
from services.email_service import send_fraud_alert_email
fake = Faker()

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

        customer = conn.execute(
            '''
            SELECT customers.email
            FROM customers
            JOIN accounts
            ON customers.customer_id = accounts.customer_id
            WHERE accounts.account_id = ?
            ''',
            (account_id,)
        ).fetchone()

        send_transaction_email(
            revicer_email= customer['email'],
            transaction_type= transaction_type,
            amount = amount
        )

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
    FRAUD_TRANSACTION_LIMIT = 10000
    FRAUD_TRANSACTION_LIMIT_LESS = 10000
    fraud_flag = 0
    fraud_reason = ""
    transaction_time = fake.date_time_this_month()

    if amount > FRAUD_TRANSACTION_LIMIT:
        fraud_flag = 2
        fraud_reason = "Large transaction detected"

    if amount < FRAUD_TRANSACTION_LIMIT_LESS:
        fraud_flag = 1
        fraud_reason = "Normal transaction"

    current_hour = transaction_time.hour

    if 1 <= current_hour <= 5:
        fraud_flag = 3
        fraud_reason = "Night time payment suspicious transaction"

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
            (account_id, transaction_type, amount,fraud_flag,fraud_reason,time_of_transaction)
            VALUES (?, ?, ? , ? , ? , ?)
            ''',
            (sender_account_id, 'Withdraw', amount , fraud_flag , fraud_reason , transaction_time)
        )

        # DEPOSIT HISTORY
        conn.execute(
            '''
            INSERT INTO transactions
            (account_id, transaction_type, amount , fraud_flag , fraud_reason, time_of_transaction)
            VALUES (?, ?, ?, ? , ? ,?)
            ''',
            (receiver_account_id, 'Deposit', amount , fraud_flag , fraud_reason ,transaction_time)
        )

        conn.commit()

        customer = conn.execute(
            '''
            SELECT customers.email
            FROM customers
            JOIN accounts
            ON customers.customer_id = accounts.customer_id
            WHERE accounts.account_id = ?
            ''',
            (sender_account_id,)
        ).fetchone()

        if customer:

            send_transaction_email(
                receiver_email=customer['email'],
                transaction_type="Transfer",
                amount=amount
            )

        else:

            print("Customer email not found")

        send_fraud_alert_email(
            receiver_email=customer['email'],
            fraud_reason=fraud_reason,
            amount = amount
        )

        return {
            "message": "Transfer successful",
            "fraud_flag": fraud_flag,
            "fraud_reason": fraud_reason
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

