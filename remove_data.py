import os
import psycopg2
from dotenv import load_dotenv
from helper_functions import check_none


load_dotenv()
password : str = check_none(os.getenv('PASS'), 'Error: Check .env file. PASS should not be None')
host : str = check_none(os.getenv('HOST'), 'Error: Check .env file. HOST should not be None')
user : str = check_none(os.getenv('USER'), 'Error: Check .env file. USER should not be None')
db_name : str = check_none(os.getenv('DBNAME'), 'Error: Check .env file. DBNAME should not be None')
port : int = int(check_none(os.getenv('PORT'), 'Error: Check .env file. PORT should not be None'))

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