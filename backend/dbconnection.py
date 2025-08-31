
import psycopg2
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env filse
import os    

def get_db_connection():
    conn = None
    try: 
        conn = psycopg2.connect(
            host=os.getenv("postgres_host"),
            database=os.getenv("postgres_db"),
            user=os.getenv("postgres_user"),
            password=os.getenv("postgres_password"),
            port=os.getenv("postgres_port")
        )
        print("Database connection established")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
       
def get_user_details():
    con = get_db_connection()
    cursor=None
    try:
        if con is not None:
            cursor = con.cursor()
            script='''Select * from users;'''
            cursor.execute(script)
            rows = cursor.fetchall()
            print(rows)
            return rows
        return []
    except Exception as e:
        print(f"Error fetching user details: {e}")
        return []
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
            print("Database connection closed")

get_user_details()            