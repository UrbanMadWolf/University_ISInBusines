import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def create_database():
    print("Creating database...")
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost"
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("CREATE DATABASE financial_analysis")
        cur.close()
        conn.close()
        print("Database created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

def init_database():
    print("Initializing database...")
    try:
        from app.db.init_db import init_db
        from app.db.session import SessionLocal
        db = SessionLocal()
        init_db(db)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Install requirements
    install_requirements()
    
    # Create database
    create_database()
    
    # Initialize database
    init_database()
    
    print("Setup completed successfully!") 