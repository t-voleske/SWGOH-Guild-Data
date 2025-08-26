import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


password = os.getenv('PASS')
host = os.getenv('HOST')
user = os.getenv('USER')


pg_connection_dict = {
    'dbname': 'guild_data',
    'user': user,
    'password': password,
    'port': 5432,
    'host': host
}

def read_guild():

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**pg_connection_dict)
        print(conn)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM guild;")
                rows = cur.fetchall()

                print("\n--- Guild ---")
                for row in rows:
                    print(
                        f"guild_id: {row[0]}, guild_name: {row[1]}"
                    )
                print("--------------------\n")
                return rows[0][0]

    except Exception as e:
        print("Connection failed.")
        print(e)

def read_players():
    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...read_players()')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM players WHERE guild_id::text = 'Xyw6K1R1SOazMbS94TX7fw'::text ORDER BY nickname DESC;")
                rows = cur.fetchall()

                #print("\n--- Players ---")
                #for row in rows:
                    #print(
                        #f"Nickname: {row[1]}, total_gp: {row[2]}"
                    #)
                #print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)

def read_roster_check():

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM players_roster_checks;")
                rows = cur.fetchall()

                #print("\n--- Players ---")
                #for row in rows:
                    #print(
                        #f"Nickname: {row[1]}, total_gp: {row[2]}"
                    #)
                #print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)

def read_raid_performance():

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM raid_performance;")
                rows = cur.fetchall()

                #print("\n--- Players ---")
                #for row in rows:
                    #print(
                        #f"Nickname: {row[1]}, total_gp: {row[2]}"
                    #)
                #print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)

def read_tickets_weekly():

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM tickets_aggregated_weekly;")
                rows = cur.fetchall()

                #print("\n--- Players ---")
                #for row in rows:
                    #print(
                        #f"Nickname: {row[1]}, total_gp: {row[2]}"
                    #)
                #print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)


def read_tickets_monthly():

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM tickets_aggregated_monthly;")
                rows = cur.fetchall()

                #print("\n--- Players ---")
                #for row in rows:
                    #print(
                        #f"Nickname: {row[1]}, total_gp: {row[2]}"
                    #)
                #print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)

def read_zeffo_readiness():

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM zeffo_readiness;")
                rows = cur.fetchall()

                #print("\n--- Players ---")
                #for row in rows:
                    #print(
                        #f"Nickname: {row[1]}, total_gp: {row[2]}"
                    #)
                #print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)

def read_guild_members():

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM guild_members;")
                rows = cur.fetchall()

                #print("\n--- Players ---")
                #for row in rows:
                    #print(
                        #f"Nickname: {row[1]}, total_gp: {row[2]}"
                    #)
                #print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)

def read_last_login():

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM last_login;")
                rows = cur.fetchall()

                #print("\n--- Players ---")
                #for row in rows:
                    #print(
                        #f"Nickname: {row[1]}, total_gp: {row[2]}"
                    #)
                #print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)

def read_players_data():

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Fetch all rows from the books table
                cur.execute("SELECT * FROM players_data;")
                rows = cur.fetchall()

                #print("\n--- Players ---")
                #for row in rows:
                    #print(
                        #f"Nickname: {row[1]}, total_gp: {row[2]}"
                    #)
                #print("--------------------\n")
                return rows

    except Exception as e:
        print("Connection failed.")
        print(e)