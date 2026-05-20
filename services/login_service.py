from flask_jwt_extended import create_access_token
from database.db import get_db_connection


def login_user(email, password):

    conn = get_db_connection()

    customer = conn.execute(
        '''
        SELECT *
        FROM customers
        WHERE email = ?
        ''',
        (email,)
    ).fetchone()

    conn.close()

    if customer is None:

        return {
            "error": "Invalid email"
        }, 401

    if password != customer['password']:

        return {
            "error": "Invalid password"
        }, 401

    access_token = create_access_token(
        identity=str(customer['customer_id'])
    )

    return {
        "message": "Login successful",
        "access_token": access_token
    }, 200