
import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

passw = os.getenv("PASSWORD_DB")


async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="lesson1_db",
            password=passw
        )
        return conn

    except Exception as error:
        print(f"Database connection error: {error}")


async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(100),
                full_name VARCHAR(100),
                balance INT DEFAULT 100,
                telegram_id VARCHAR(99),
                created_at TIMESTAMP DEFAULT NOW(),
                is_active BOOLEAN DEFAULT TRUE
            );

            CREATE TABLE IF NOT EXISTS history_tranz (
                history_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(user_id),
                descriptions VARCHAR(100),
                type_of_tranz VARCHAR(30),
                sum BIGINT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

        print("Table created successfully")
    except Exception as error:
        print(f"Table created error: {error}")

    finally:
        await conn.close()
