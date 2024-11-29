import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os
import psycopg2

# Load environment variables from .env file
load_dotenv(".env")

# Get database credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "postgresql_db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME") 
print(DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
# Ensure all required variables are present
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("One or more required environment variables are missing.")

# Construct the SQLAlchemy DATABASE_URL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = sql.create_engine(DATABASE_URL)
Base = declarative.declarative_base()
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a psycopg2-compatible connection string by removing "+psycopg2"
psycopg2_compatible_url = DATABASE_URL.replace("postgresql+psycopg2", "postgresql")

try:
    # Connect to the default 'postgres' database to manage the creation of your database
    connection = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT)  # Ensure DB_PORT is an integer
    )
    connection.autocommit = True
    cursor = connection.cursor()
    
    # Check if the database exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
    exists = cursor.fetchone()
    
    if not exists:
        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database {DB_NAME} created successfully.")
    else:
        print(f"Database {DB_NAME} already exists.")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"Error creating database: {e}")

# Create tables in the database
Base.metadata.create_all(engine)

def get_db():
    """
    Provides a database session for use in the application.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
