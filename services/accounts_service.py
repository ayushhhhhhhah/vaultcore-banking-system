from database.db import get_db_connection


# GET ALL ACCOUNTS OF LOGGED-IN USER
def get_all_accounts(logged_in_customer_id):

    conn = get_db_connection()

    accounts = conn.execute(
        '''
        SELECT *
        FROM accounts
        WHERE customer_id = ?
        ''',
        (logged_in_customer_id,)
    ).fetchall()

    conn.close()

    return [dict(account) for account in accounts]


# GET SPECIFIC ACCOUNT
def get_account_byid(
    logged_in_customer_id,
    account_id
):

    conn = get_db_connection()

    account = conn.execute(
        '''
        SELECT *
        FROM accounts
        WHERE account_id = ?
        ''',
        (account_id,)
    ).fetchone()

    conn.close()


    if account is None:

        return {
            "error": "Account not found"
        }

    # OWNERSHIP VALIDATION
    if account['customer_id'] != logged_in_customer_id:

        return {
            "error": "Unauthorized access to this account"
        }

    return dict(account)


# CREATE NEW ACCOUNT
def create_account_newaccount(
    customer_id,
    branch_id,
    account_type,
    balance
):

    conn = get_db_connection()

    try:

        # VALIDATION
        if balance < 0:

            return {
                "error": "Balance cannot be negative"
            }

        conn.execute(
            '''
            INSERT INTO accounts
            (customer_id, branch_id, account_type, balance)
            VALUES (?, ?, ?, ?)
            ''',
            (
                customer_id,
                branch_id,
                account_type,
                balance
            )
        )

        conn.commit()

        return {
            "message": "Account created successfully"
        }

    except Exception as e:

        conn.rollback()

        return {
            "error": str(e)
        }

    finally:

        conn.close()