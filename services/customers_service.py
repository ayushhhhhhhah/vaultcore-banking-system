import sqlite3
import bcrypt
from database.db import get_db_connection


# GET LOGGED-IN CUSTOMER ONLY
def get_all_customers(logged_in_customer_id):

    conn = get_db_connection()

    customers = conn.execute(
        '''
        SELECT *
        FROM customers
        WHERE customer_id = ?
        ''',
        (logged_in_customer_id,)
    ).fetchall()

    conn.close()

    customer_list = []

    for customer in customers:

        customer_dict = dict(customer)

        # REMOVE PASSWORD FROM RESPONSE
        customer_dict.pop('password', None)

        customer_list.append(customer_dict)

    return customer_list


# ADD NEW CUSTOMER
def add_new_customer(
        first_name,
        middle_name,
        last_name,
        email,
        phone,
        password
):

    conn = get_db_connection()

    try:

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        conn.execute(
            '''
            INSERT INTO customers
            (first_name, middle_name, last_name, email, phone, password)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                first_name,
                middle_name,
                last_name,
                email,
                phone,
                hashed_password
            )
        )

        conn.commit()

        #send_signup_email(email)

        return {
            "message": "Customer Added Successfully"
        }

    except sqlite3.IntegrityError:

        conn.rollback()

        return {
            "error": "Phone number or email already exists"
        }

    except Exception as e:

        conn.rollback()

        return {
            "error": str(e)
        }

    finally:

        conn.close()


# GET SPECIFIC CUSTOMER
def get_specific_customer(customer_id):

    conn = get_db_connection()

    customer = conn.execute(
        '''
        SELECT *
        FROM customers
        WHERE customer_id = ?
        ''',
        (customer_id,)
    ).fetchone()

    conn.close()

    if customer is None:

        return {
            "error": "Customer Not Found"
        }

    customer_dict = dict(customer)

    # REMOVE PASSWORD
    customer_dict.pop('password', None)

    return customer_dict


# UPDATE CUSTOMER
def update_specific_customer(
        first_name,
        middle_name,
        last_name,
        email,
        phone,
        password,
        customer_id
):

    conn = get_db_connection()

    try:

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        conn.execute(
            '''
            UPDATE customers
            SET
                first_name = ?,
                middle_name = ?,
                last_name = ?,
                email = ?,
                phone = ?,
                password = ?
            WHERE customer_id = ?
            ''',
            (
                first_name,
                middle_name,
                last_name,
                email,
                phone,
                hashed_password,
                customer_id
            )
        )

        conn.commit()

        return {
            "message": "Customer Updated Successfully"
        }

    except sqlite3.IntegrityError:

        conn.rollback()

        return {
            "error": "Phone number or email already exists"
        }

    except Exception as e:

        conn.rollback()

        return {
            "error": str(e)
        }

    finally:

        conn.close()


# DELETE CUSTOMER
def delete_specific_customer(customer_id):

    conn = get_db_connection()

    try:

        conn.execute(
            '''
            DELETE FROM customers
            WHERE customer_id = ?
            ''',
            (customer_id,)
        )

        conn.commit()

        return {
            "message": "Customer Deleted Successfully"
        }

    except Exception as e:

        conn.rollback()

        return {
            "error": str(e)
        }

    finally:

        conn.close()

def change_customer_password(
        customer_id,
        old_password,
        new_password
):
    conn = get_db_connection()

    customer = conn.execute(
        '''
        SELECT *
        FROM customers
        WHERE customer_id = ?
        ''',(customer_id)
    ).fetchone()

    if customer is None:
        conn.close()

        return {
            "error": "Customer Not Found"
        }
    stored_password = customer['password']

    password_correct = bcrypt.checkpw(
        old_password.encode('utf-8'),
        stored_password.encode('utf-8')
    )

    if not password_correct:
        conn.close()
        return {
            "error": "Password Not Correct"
        }

    hashed_new_password = bcrypt.hashpw(
        new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    conn.execute(
        '''
        UPDATE customers
        SET password = ?
        WHERE customer_id = ?
        ''',
        (
            hashed_new_password,
            customer_id
        )
    )
    conn.commit()

    conn.close()

    return {
        "message": "Password changed successfully"
    }
