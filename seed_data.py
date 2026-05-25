import random
import sqlite3
import bcrypt
from faker import Faker


def seed_fake_data():

    fake = Faker()

    conn = sqlite3.connect(
        "database/production.db"
    )

    cursor = conn.cursor()

    # remaining code here


if __name__ == "__main__":
    seed_fake_data()