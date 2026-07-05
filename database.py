import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                user_id INTEGER PRIMARY KEY,
                background TEXT DEFAULT 'Sunset',
                frame TEXT DEFAULT 'No Frame',
                padding INTEGER DEFAULT 40,
                radius INTEGER DEFAULT 15
            )
        ''')
        await db.commit()

async def register_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.execute("INSERT OR IGNORE INTO settings (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def update_setting(user_id: int, column: str, value: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(f"UPDATE settings SET {column} = ? WHERE user_id = ?", (value, user_id))
        await db.commit()

async def get_user_settings(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT background, frame, padding, radius FROM settings WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"background": row[0], "frame": row[1], "padding": row[2], "radius": row[3]}
            return {"background": "Sunset", "frame": "No Frame", "padding": 40, "radius": 15}

