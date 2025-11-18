"""
Quick database migration to add missing columns
"""
import sqlite3

db_path = "agents.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add missing columns to agents table
try:
    cursor.execute("ALTER TABLE agents ADD COLUMN tier TEXT DEFAULT 'worker'")
    print("[OK] Added tier column")
except sqlite3.OperationalError as e:
    print(f"Tier column may already exist: {e}")

try:
    cursor.execute("ALTER TABLE agents ADD COLUMN description TEXT")
    print("[OK] Added description column")
except sqlite3.OperationalError as e:
    print(f"Description column may already exist: {e}")

try:
    cursor.execute("ALTER TABLE agents ADD COLUMN capabilities TEXT")
    print("[OK] Added capabilities column")
except sqlite3.OperationalError as e:
    print(f"Capabilities column may already exist: {e}")

try:
    cursor.execute("ALTER TABLE agents ADD COLUMN last_active TIMESTAMP")
    print("[OK] Added last_active column")
except sqlite3.OperationalError as e:
    print(f"Last_active column may already exist: {e}")

# Create chat_sessions table if it doesn't exist
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id TEXT PRIMARY KEY,
            agent_id INTEGER NOT NULL,
            messages TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    """)
    print("[OK] Created chat_sessions table")
except sqlite3.OperationalError as e:
    print(f"Chat sessions table error: {e}")

# Create documents table if it doesn't exist
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            mime_type TEXT,
            agent_id INTEGER,
            uploaded_by TEXT,
            chunk_count INTEGER DEFAULT 0,
            processed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    """)
    print("[OK] Created documents table")
except sqlite3.OperationalError as e:
    print(f"Documents table error: {e}")

conn.commit()
conn.close()

print("\n[SUCCESS] Database migration complete!")
