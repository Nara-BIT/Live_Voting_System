import streamlit as st
import psycopg2
import pandas as pd
import time

# Page Configuration
st.set_page_config(page_title="Live Election Dashboard", page_icon="🗳️", layout="wide")
st.title("🗳️ Real-Time Election Dashboard")
st.markdown("Watch the votes stream in live! The dashboard refreshes automatically.")

# Fetch Live Data from Postgres
def get_live_data():
    # Connect to the local Postgres container
    conn = psycopg2.connect(
        host="localhost", 
        database="voting_db", 
        user="user", 
        password="password", 
        port="5432"
    )
    
    # Join candidates table with vote_results table
    query = """
    SELECT 
        c.candidate_name AS "Candidate", 
        c.party_affiliation AS "Party", 
        COALESCE(v.count, 0) AS "Total Votes"
    FROM candidates c
    LEFT JOIN vote_results v ON c.candidate_id = v.candidate_id
    ORDER BY "Total Votes" DESC
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Get the data
df = get_live_data()

# Create Visuals
col1, col2 = st.columns([1, 2])

with col1:
    st.dataframe(df, hide_index=True, use_container_width=True)

with col2:
    st.bar_chart(data=df, x="Candidate", y="Total Votes", use_container_width=True)

# Auto-refresh the dashboard every 2 seconds
time.sleep(2)
st.rerun()