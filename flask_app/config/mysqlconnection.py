import aiomysql
import os
from dotenv import load_dotenv
load_dotenv()


class MySQLConnection:
    def __init__(self, db):
        self.db = db
        self.pool = None

    async def create_pool(self):
        self.pool = await aiomysql.create_pool(
            host=os.getenv('RDS_ENDPOINT'),
            user=os.getenv('RDS_USER'),
            password=os.getenv('RDS_PASSWORD'),
            db=self.db,
            charset='utf8mb4',
            cursorclass=aiomysql.DictCursor,
            autocommit=False
        )

    async def query_db(self, query: str, data: dict = None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute('SET SQL_SAFE_UPDATES = 0')
                    if data:
                        await cursor.execute(query, data)
                    else:
                        await cursor.execute(query)
                    print("Running Query:", query)

                    if query.lower().find("insert") >= 0:
                        await conn.commit()
                        return cursor.lastrowid
                    elif query.lower().find("select") >= 0:
                        result = await cursor.fetchall()
                        return result
                    else:
                        await conn.commit()
                except Exception as e:
                    print("Something went wrong", e)
                    return False
                finally:
                    await conn.ensure_closed()




def connect_to_mysql(db):
    return MySQLConnection(db)

