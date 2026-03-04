import psycopg2

def init_db():
    conn = psycopg2.connect(host="localhost", database="voting_db", user="user", password="password")
    cur = conn.cursor()
    
    # Create Tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            candidate_id VARCHAR(255) PRIMARY KEY,
            candidate_name VARCHAR(255),
            party_affiliation VARCHAR(255)
        );
    """)
    
    # Add Sample Candidates
    candidates = [
        ('1', 'Candidate A', 'The Tech Party'),
        ('2', 'Candidate B', 'The Data Alliance'),
        ('3', 'Candidate C', 'The AI Union')
    ]
    
    for c in candidates:
        cur.execute("INSERT INTO candidates VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", c)
    
    conn.commit()
    print("✅ Database Initialized with 3 Candidates!")
    cur.close()
    conn.close()

if __name__ == "__main__":
    init_db()