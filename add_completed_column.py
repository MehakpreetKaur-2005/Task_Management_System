from app import app, db
import sqlite3

def add_completed_column():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/todo.db')  # Adjust path if needed
    cursor = conn.cursor()
    
    # Check if the column already exists
    cursor.execute("PRAGMA table_info(todo)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'completed' not in columns:
        print("Adding 'completed' column to todo table...")
        # Add the completed column with a default value of False (0)
        cursor.execute("ALTER TABLE todo ADD COLUMN completed BOOLEAN DEFAULT 0")
        conn.commit()
        print("Column added successfully!")
    else:
        print("The 'completed' column already exists.")
    
    conn.close()

if __name__ == "__main__":
    with app.app_context():
        add_completed_column()
