import random
import sqlite3
from faker import Faker
from datetime import datetime

fake = Faker()

conn = sqlite3.connect(
    "database/production.db"
)

cursor = conn.cursor()

for i in range(100):

    account_id = random.randint(1, 10)

    transaction_type = random.choice([
        "Deposit",
        "Withdraw"
    ])

    amount = round(
        random.uniform(500, 200000),
        2
    )

    # GENERATE RANDOM TRANSACTION TIME
    transaction_time = fake.date_time_this_month()

    current_hour = transaction_time.hour

    # DEFAULT NORMAL TRANSACTION
    fraud_flag = 1
    fraud_reason = "Normal transaction"

    # LARGE TRANSACTION
    if amount > 100000:

        fraud_flag = 2

        fraud_reason = (
            "Large transaction detected"
        )

    # NIGHT TRANSACTION
    elif 1 <= current_hour <= 5:

        fraud_flag = 3

        fraud_reason = (
            "Night time suspicious transaction"
        )

    cursor.execute(
        '''
        INSERT INTO transactions
        (
            account_id,
            transaction_type,
            amount,
            fraud_flag,
            fraud_reason,
            time_of_transactions
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (
            account_id,
            transaction_type,
            amount,
            fraud_flag,
            fraud_reason,
            transaction_time
        )
    )

    print(
        f"Inserted transaction {i + 1}"
    )

conn.commit()

conn.close()

print("Fake transactions inserted")