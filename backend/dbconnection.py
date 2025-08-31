
import psycopg2
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env filse
import os    
import psycopg2.extras

def get_db_connection():
    try: 
        with psycopg2.connect(
            host=os.getenv("postgres_host"),
            database=os.getenv("postgres_db"),
            user=os.getenv("postgres_user"),
            password=os.getenv("postgres_password"),
            port=os.getenv("postgres_port")
        ) as conn:
            print("Database connection established")
            return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    finally:
        print("Connection closed",conn.closed)
def get_user_details():
    con = get_db_connection()
    try:
        if con is not None:
           with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                script='''Select * from users;'''
                cursor.execute(script)
                rows = cursor.fetchall()
                return rows
        return []
    except Exception as e:
        print(f"Error fetching user details: {e}")
        return []
    finally:
        con.close()
        print(con.closed)  # Check if connection is closed
        print(cursor.closed)

get_user_details()            