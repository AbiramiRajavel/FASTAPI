
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text, MetaData, Table, Column, Integer, String, select
import os
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

metaData=MetaData()
base =declarative_base()
def create_connection_pool():
    try:
        url = URL.create(
            "postgresql",
            host=os.getenv("postgres_host"),
            database=os.getenv("postgres_db"),
            username=os.getenv("postgres_user"),
            password=os.getenv("postgres_password"),
            port=os.getenv("postgres_port")
        )
        print(url)
        engine = create_engine(url,pool_size=1)
        print(f"Initial pool size: {engine.pool.size()}")
        return engine
    except Exception as e:
        print("Error connecting to the database:", e)
        return None
    finally:
        print('ccc',engine.pool.status()) 
   

def insert_user():
    engine=create_connection_pool()
    with engine.connect() as conn:
        insert_stmt = text("INSERT INTO users (name, age) VALUES (:name, :age)")
        conn.execute(insert_stmt, {"name": "Alice", "age": 11})
        conn.commit()   
        print(conn.closed)
    print(conn.closed)

def generate_customer_table():
   customer_table = Table(
    'Customer',
    metaData,
    Column('id', Integer, primary_key=True),
    Column('name', String(50))
   )
   engine=create_connection_pool()
   metaData.create_all(engine)   
   insert_data=customer_table.insert().values(id=1, name="John Doe")
   with engine.connect() as conn:
        exists_stmt = select(customer_table.c.id).where(customer_table.c.id == 1)
        existing_row = conn.execute(exists_stmt).fetchone()
        if not existing_row:
            conn.execute(insert_data)
            print("Table created and data inserted")
        conn.commit()


class User2(base):
    __tablename__ = 'users2' # __table__ or __tablename__
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)



def generate_table_orm():
    engine=create_connection_pool()
    base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    session=Session()
    user=User2(name="Jane Doe", email="jane@example.com")
    session.add(user)
    session.commit()

if __name__ == "__main__":
        generate_customer_table()
        generate_table_orm()
        insert_user()