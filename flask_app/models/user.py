from flask_app.config.mysqlconnection import connect_to_mysql
from quart import session, flash

class User:
    DB = 'flighttracker'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    async def get_all(cls):
        query = 'SELECT * FROM users'
        results = await (cls.DB).query_db(query)
        user_data = []
        for row in results:
            user_dict = {
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'created_at': row['created_at']
            }
            user_data.append(user_dict)
        print(user_data)
        return user_data

    @classmethod
    async def get_one(cls, id):
        query = """
            SELECT * FROM users
            WHERE id = %(id)s"""
        results =  await connect_to_mysql(cls.DB).query_db(query,{"id": id})
        return cls(results[0])


    @classmethod
    async def create(cls, data):
        query = '''INSERT INTO users (name, email, password, created_at, updated_at) 
                   VALUES( %(name)s, %(email)s, %(password)s, NOW(), NOW());'''
        return await connect_to_mysql(cls.DB).query_db(query, data)

    @classmethod
    async def update(cls, data):
        query = """
            UPDATE users
            SET first_name = %(fname)s, email = %(email)s, updated_at = NOW()
            WHERE id = %(id)s;
        """
        results = await connect_to_mysql(cls.DB).query_db(query, data)
        return results

    @classmethod
    async def delete(cls, id):
        query = """
            DELETE FROM users
            WHERE id = %(id)s;
        """
        results = await connect_to_mysql(cls.DB).query_db(query, {'id':id})
        return results

    @classmethod
    async def get_by_email(cls, data):
        query = """
            SELECT email FROM users
            WHERE email = %(email)s;
        """
        result = await connect_to_mysql(cls.DB).query_db(query, {'email': data})
        return result

    @classmethod
    async def login(cls, data):
        query = """
            SELECT * FROM users
            WHERE email = %(email)s;
        """
        result = await connect_to_mysql(cls.DB).query_db(query, {'email': data})
        return result
