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

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_guild():
    

    conn = None
    try:
        print('Reading from guild table...')
        conn = psycopg2.connect(**pg_connection_dict)
        print(conn)
        with conn.cursor() as cur:
                cur.execute("SELECT * FROM guild;")
                rows = cur.fetchall()

                print("\n--- Guild ---")
                for row in rows:
                    print(
                        f"guild_id: {row[0]}, guild_name: {row[1]}"
                    )
                print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_players(guild_id):
    conn = None
    try:
        print('Reading from players table WHERE player part of guild')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                cur.execute("SELECT * FROM players WHERE guild_id::text = %s ORDER BY nickname DESC;", (guild_id,))
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_roster_check():

    conn = None
    try:
        print('Reading from players_roster_checks...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                cur.execute("SELECT * FROM players_roster_checks;")
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_tickets_weekly():

    conn = None
    try:
        print('Reading from tickets_aggregated_weekly view...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                cur.execute("SELECT * FROM tickets_aggregated_weekly;")
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_tickets_monthly():

    conn = None
    try:
        print('Reading from tickets_aggregated_monthly view...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                cur.execute("SELECT * FROM tickets_aggregated_monthly;")
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_zeffo_readiness():

    conn = None
    try:
        print('Reading from zeffo_readiness view...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                cur.execute("SELECT * FROM zeffo_readiness;")
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_guild_members():

    conn = None
    try:
        print('Reading from guild_members view...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                cur.execute("SELECT * FROM guild_members;")
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_last_login():

    conn = None
    try:
        print('Reading from last_login table...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                cur.execute("SELECT * FROM last_login;")
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_players_data():

    conn = None
    try:
        print('Reading from players_data table ...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                cur.execute("SELECT * FROM players_data ORDER BY nickname ASC;")
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_raid_performance_special():

    conn = None
    try:
        print('Reading raid_performance view...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                cur.execute("SELECT p.player_id, p.nickname, rp.score AS score, rp.percent_of_average AS percent_of_average FROM players p LEFT JOIN raid_performance rp ON p.nickname = rp.nickname WHERE guild_id::text = 'Xyw6K1R1SOazMbS94TX7fw'::text;")
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_member_points():

    conn = None
    try:

        print('Reading member_points view...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:

                cur.execute("SELECT * FROM member_points ORDER BY nickname ASC;")                
                rows = cur.fetchall()
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()