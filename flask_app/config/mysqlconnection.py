import pymysql.cursors
import os
from dotenv import load_dotenv

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host=os.getenv('RDS_ENDPOINT'),
                                     user=os.getenv('RDS_USER'),
                                     password=os.getenv('RDS_PASSWORD'),
                                     db=db,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=False)
        self.connection = connection

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute("SET SQL_SAFE_UPDATES = 0")
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query)


                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close()
            # connect_to_mysql receives the database we're using and uses it to create an instance of MySQLConnection




def connect_to_mysql(db):
    return MySQLConnection(db)

