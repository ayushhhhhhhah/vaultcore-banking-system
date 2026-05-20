import random
import sqlite3

from faker import Faker

fake = Faker()


# DATABASE CONNECTION

conn = sqlite3.connect("sqlite3 banking.db")

cursor = conn.cursor()


for i in range(100000):

    first_name = fake.first_name()

    middle_name = fake.first_name()

    last_name = fake.last_name()


    # UNIQUE EMAIL

    email = (
        f"{fake.user_name()}"
        f"{random.randint(1000,999999)}@gmail.com"
    )


    # UNIQUE PHONE

    phone = str(
        random.randint(
            6000000000,
            9999999999
        )
    )


    # PASSWORD

    password = "password123"


    # NO BCRYPT FOR FAST INSERT

    hashed_password = password


    try:

        # INSERT CUSTOMER

        cursor.execute(
            '''
            INSERT INTO customers
            (
                first_name,
                middle_name,
                last_name,
                email,
                phone,
                password
            )
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

        customer_id = cursor.lastrowid


        # RANDOM BALANCE

        balance = round(
            random.uniform(
                1000,
                500000
            ),
            2
        )


        # RANDOM ACCOUNT TYPE

        account_type = random.choice([
            "Savings",
            "Current"
        ])


        # INSERT ACCOUNT

        cursor.execute(
            '''
            INSERT INTO accounts
            (
                customer_id,
                branch_id,
                account_type,
                balance
            )
            VALUES (?, ?, ?, ?)
            ''',
            (
                customer_id,
                1,
                account_type,
                balance
            )
        )

    except Exception:

        continue


conn.commit()

conn.close()

print("Fake data inserted successfully")