import random
import sqlite3
import bcrypt

from faker import Faker

fake = Faker()


# DATABASE CONNECTION

conn = sqlite3.connect("database/production.db")

cursor = conn.cursor()


# INSERT BRANCH IF NOT EXISTS

cursor.execute(
    '''
    INSERT OR IGNORE INTO branches
    (
        branch_id,
        branch_name,
        city
    )
    VALUES (?, ?, ?)
    ''',
    (
        1,
        "Main Branch",
        "Mumbai"
    )
)


# OPTIONAL: CLEAR OLD DATA

cursor.execute("DELETE FROM accounts")
cursor.execute("DELETE FROM customers")


# RESET AUTO INCREMENT IDS

cursor.execute(
    "DELETE FROM sqlite_sequence WHERE name='customers'"
)

cursor.execute(
    "DELETE FROM sqlite_sequence WHERE name='accounts'"
)


# GENERATE FAKE USERS

for i in range(100):

    try:

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


        # HASH PASSWORD

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")


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


        print(f"Inserted customer {customer_id}")


    except Exception as e:

        print("ERROR:", e)


conn.commit()

conn.close()

print("Fake data inserted successfully")