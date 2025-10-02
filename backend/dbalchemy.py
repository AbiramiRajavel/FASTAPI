
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text, MetaData, Table, Column, Integer, String, select
import os
from sqlalchemy.orm import declarative_base, sessionmaker
from .table_schemas import base, User,User2  # Import the base and User model

load_dotenv()

metaData=MetaData()
# Create a single engine instance
_engine = None

def create_connection_pool():
    global _engine
    if _engine is not None:
        return _engine
        
    try:
        url = URL.create(
            "postgresql",
            host=os.getenv("postgres_host"),
            database=os.getenv("postgres_db"),
            username=os.getenv("postgres_user"),
            password=os.getenv("postgres_password"),
            port=os.getenv("postgres_port")
        )
        _engine = create_engine(
            url,
            pool_size=5,  # Increased pool size
            max_overflow=10,  # Allow up to 10 connections beyond pool_size
            pool_timeout=30,  # Wait up to 30 seconds for a connection
            pool_recycle=1800  # Recycle connections after 30 minutes
        )
        return _engine
    except Exception as e:
        raise Exception(f"Error connecting to the database: {str(e)}")

# Create a single SessionMaker
SessionLocal = None

def get_db():
    global SessionLocal
    if SessionLocal is None:
        engine = create_connection_pool()
        SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

def generate_table_orm():
    engine=create_connection_pool()
    base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    session=Session()
    user=User2(name="Jane Doe", email="jane@example.com")
    session.add(user)
    session.commit()

def create_tables():
    """Create all tables defined in table_schemas"""
    engine = create_connection_pool()
    base.metadata.create_all(bind=engine)
    print("All tables created successfully")

if __name__ == "__main__":
    create_tables()  # This will create the User table
    generate_customer_table()
    generate_table_orm()
    insert_user()