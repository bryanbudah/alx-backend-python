import aiosqlite
import asyncio

# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        await cursor.close()
        return users  # ✅ Must use return

# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        older_users = await cursor.fetchall()
        await cursor.close()
        return older_users  # ✅ Must use return

# Run both queries concurrently
async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    # ✅ Print results outside the async functions
    print("All users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)

# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
