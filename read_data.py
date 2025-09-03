import os
import psycopg2
from dotenv import load_dotenv
from helper_functions import check_none


load_dotenv()
password: str = check_none(
    os.getenv("PASS"), "Error: Check .env file. PASS should not be None"
)
host: str = check_none(
    os.getenv("HOST"), "Error: Check .env file. HOST should not be None"
)
user: str = check_none(
    os.getenv("USER"), "Error: Check .env file. USER should not be None"
)
db_name: str = check_none(
    os.getenv("DBNAME"), "Error: Check .env file. DBNAME should not be None"
)
port: int = int(
    check_none(os.getenv("PORT"), "Error: Check .env file. PORT should not be None")
)

pg_connection_dict = {
    "dbname": db_name,
    "user": user,
    "password": password,
    "port": port,
    "host": host,
}


def read_guild():
    conn = None
    try:
        print("Reading from guild table...")
        conn = psycopg2.connect(**pg_connection_dict)
        print(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM guild;")
            rows = cur.fetchall()

            print("\n--- Guild ---")
            for row in rows:
                print(f"guild_id: {row[0]}, guild_name: {row[1]}")
            print("--------------------\n")
            return rows

    except psycopg2.Error as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


def read_players_raw():
    conn = None
    try:
        print("Reading all entries of players table")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM players ORDER BY nickname DESC;")
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


def read_players(guild_id):
    conn = None
    try:
        print("Reading from players table WHERE player part of guild")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM players WHERE guild_id::text = %s ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
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
        print("Reading from players_roster_checks...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM players_roster_checks;")
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_tickets_weekly(guild_id):
    conn = None
    try:
        print("Reading from tickets_aggregated_weekly view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT taw.nickname AS nickname, taw.tickets_lost AS tickets_lost, "
                "taw.days_tickets_lost AS days_tickets_lost, taw.full_days_lost AS full_days_lost "
                "FROM players p "
                "LEFT JOIN tickets_aggregated_weekly taw "
                "ON p.nickname = taw.nickname "
                "WHERE guild_id = %s ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_tickets_monthly(guild_id):
    conn = None
    try:
        print("Reading from tickets_aggregated_monthly view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT tam.nickname AS nickname, tam.tickets_lost AS tickets_lost, "
                "tam.days_tickets_lost AS days_tickets_lost, tam.full_days_lost AS full_days_lost "
                "FROM players p "
                "LEFT JOIN tickets_aggregated_monthly tam "
                "ON p.nickname = tam.nickname "
                "WHERE guild_id = %s ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
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
        print("Reading from zeffo_readiness view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM zeffo_readiness;")
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def read_guild_members(guild_id):
    conn = None
    try:
        print("Reading from guild_members view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM guild_members WHERE guild_id::text = %s ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
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
        print("Reading from last_login table...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM last_login;")
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


def read_players_data(guild_id):
    conn = None
    try:
        print("Reading from players_data table ...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM players_data WHERE nickname IN (SELECT nickname FROM players WHERE guild_id = %s) ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


def read_raid_performance_by_guild(guild_id):
    conn = None
    try:
        print("Reading raid_performance view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT p.player_id, p.nickname, rp.score AS score, rp.percent_of_average AS percent_of_average FROM players p LEFT JOIN raid_performance rp ON p.nickname = rp.nickname WHERE guild_id::text = %s;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


def read_member_points(guild_id):
    conn = None
    try:
        print("Reading member_points view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM member_points WHERE nickname IN (SELECT nickname FROM players WHERE guild_id = %s) ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()
