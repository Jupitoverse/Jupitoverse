"""Fix team members status to Active"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'data', 'database', 'people_skills.db')
print(f'Connecting to: {db_path}')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current status
cursor.execute('SELECT id, name, status FROM team_members')
members = cursor.fetchall()
print(f'Found {len(members)} team members:')
for m in members:
    print(f'  {m}')

# Update all members to Active
cursor.execute("UPDATE team_members SET status = 'Active' WHERE status != 'Active'")
updated = cursor.rowcount
print(f'\nUpdated {updated} members to Active status')

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM team_members WHERE status = 'Active'")
active_count = cursor.fetchone()[0]
print(f'Active members now: {active_count}')

conn.close()
print('\nDone!')
