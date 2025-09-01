import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
password = os.getenv('PASS')
host = os.getenv('HOST')
user = os.getenv('USER')
db_name = os.getenv('DBNAME')
port = os.getenv('PORT')
if port is None:
    raise ValueError("Check .env file! PORT variable must not be None")
port = int(port)

pg_connection_dict = {
    'dbname': db_name,
    'user': user,
    'password': password,
    'port': port,
    'host': host
}

def remove_from_players(player_to_remove):
    if not player_to_remove:
        print("No players to remove.")
        return
    
    conn = None
    try:
        print(f'Removing {len(player_to_remove)} old guild members...')
        conn = psycopg2.connect(**pg_connection_dict)
        with conn.cursor() as cur:
            cur.executemany(
                "DELETE FROM players WHERE player_id = %s;",
                player_to_remove,
            )
            deleted_count = cur.rowcount
            print(f"Removed {deleted_count} old guild members after archiving")
            conn.commit()
            print("Done")
    except psycopg2.Error as db_error:
        print(f"Database error: {db_error}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()