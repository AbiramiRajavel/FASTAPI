from dbalchemy import  create_connection_pool
from sqlalchemy import  text
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import Column, Integer, String
base = declarative_base()

class User(base):
    __tablename__ = 'users' # __table__ or __tablename__
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)

def get_user_core():
    engine=create_connection_pool()
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users"))
            users = result.fetchone()
            for i in users:
                print(i)
    except Exception as e:
        print(f"Error fetching users: {e}")
    finally:
        conn.close()
        print("Connection closed",conn.closed)
            
def get_user_orm():
    engine=create_connection_pool()
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        users = session.query(User).all()
        for user in users:
            print(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}")
    except Exception as e:
        print(f"Error fetching users: {e}")
    finally:
        session.close()
        print("Session closed")

if __name__ == "__main__":
        get_user_core()
        get_user_orm()