import bcrypt

from flask_jwt_extended import create_access_token

from database.db import get_db_connection

from services.email_service import send_login_email



def login_customer(email, password):

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

    # CUSTOMER NOT FOUND
    if customer is None:

        return {
            "error": "Customer not found"
        }, 404

    stored_password = customer["password"]

    # PASSWORD CHECK
    password_correct = bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password.encode("utf-8")
    )

    if not password_correct:

        return {
            "error": "Invalid password"
        }, 401

    #send_login_email(
        receiver_email=customer["email"]
   # )

    # JWT TOKEN
    access_token = create_access_token(
        identity=str(customer["customer_id"])
    )

    return {

        "message": "Login successful",

        "token": access_token,

        "customer": {

            "customer_id": customer["customer_id"],
            "first_name": customer["first_name"],
            "email": customer["email"]

        }

    }, 200