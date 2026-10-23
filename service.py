
from connection import *

async def created_user(username, full_name, balance, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
            INSERT INTO users (username,full_name,balance,telegram_id) VALUES 
            ($1, $2, $3, $4)
                            """, username, full_name, balance, str(telegram_id))
    except Exception as error:
        print(f"Created user error: {error}")
    finally:
        if conn:
            await conn.close()


async def get_user(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
            SELECT * FROM users where telegram_id = $1
                            """, str(telegram_id))
        return user
    except Exception as error:
        print(f"Get user error: {error}")
    finally:
        if conn:
            await conn.close()



async def get_users():
    try:
        conn = await connection_db()
        users = await conn.fetch("""
            SELECT * FROM users
                            """)
        return users
    except Exception as error:
        print(f"Get users error: {error}")
    finally:
        if conn:
            await conn.close()



async def get_history(telegram_id):
    try:
        conn = await connection_db()
        transactions = await conn.fetch("""
            SELECT transactions.*
            FROM transactions
            JOIN users ON transactions.user_id = users.id
            WHERE users.telegram_id = $1
            ORDER BY transactions.id DESC
        """, str(telegram_id))
        return transactions
    except Exception as error:
        print(f"Get history error: {error}")
    finally:
        if conn:
            await conn.close()



async def update_balance(telegram_id, amount, operation):
    conn = await connection_db()
    try:
        user = await conn.fetchrow("""
            select * FROM users where telegram_id = $1
        """, str(telegram_id))

        if user:
            balance = user["balance"]
            if operation == "deposit":
                balance += amount
            elif operation == "withdraw":
                balance -= amount

            await conn.execute("""
                UPDATE users SET balance = $1 WHERE telegram_id = $2
            """, balance, str(telegram_id))
    finally:
        await conn.close()