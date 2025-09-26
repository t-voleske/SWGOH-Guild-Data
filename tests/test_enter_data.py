import pytest
from unittest.mock import MagicMock
from src.enter_data import (
    enter_players,
    enter_gp_logs,
    enter_player_check,
    enter_tickets,
    enter_raid_score_log,
    enter_player_archive,
    enter_tb_data,
)
import psycopg2


@pytest.mark.parametrize(
    "func, table_name, data, expected_sql",
    [
        (
            enter_players,
            "players",
            [("1", "player1", 1000, "guild1", "2023-01-01")],
            "INSERT INTO players (player_id, nickname, total_gp, guild_id, last_activity_time) VALUES (%s, %s, %s, %s, %s);",
        ),
        (
            enter_gp_logs,
            "gp_history",
            [("1", 1000)],
            "INSERT INTO gp_history (player_id, total_gp, timestamp) VALUES (%s, %s, NOW());",
        ),
        (
            enter_player_check,
            "players_roster_checks",
            [("True", "True", "False", "True", "True", "1")],
            "INSERT INTO players_roster_checks (all_jkck_reqs_7_star, jkck_unlocked, jkck_r7, cere_r7, jkck_skill_levels_done, player_id) VALUES (%s, %s, %s, %s, %s, %s);",
        ),
        (
            enter_tickets,
            "ticket_log",
            [("1", 100)],
            "INSERT INTO ticket_log (player_id, created_at, tickets_lost) VALUES (%s, NOW(), %s);",
        ),
        (
            enter_raid_score_log,
            "raid_score_log",
            [("1", 100000, 0.95)],
            "INSERT INTO raid_score_log (player_id, raid_score, percent_of_avg) VALUES (%s, %s, %s);",
        ),
        (
            enter_player_archive,
            "players_archive",
            [("1", "player1", 1000, "guild1")],
            "INSERT INTO players_archive (player_id, nickname, total_gp, guild_id) VALUES (%s, %s, %s, %s);",
        ),
        (
            enter_tb_data,
            "tb_import",
            [("player1", 10000, 5, 5, 1.0, 0)],
            "INSERT INTO tb_import (nickname, total_territory_points, total_waves_completed, total_missions_attempted, wave_completion_ratio, phases_missed) VALUES (%s, %s, %s, %s, %s, %s);",
        ),
    ],
)
def test_data_insertion_success(mock_db_connection, func, table_name, data, expected_sql):
    """
    Each function successfully inserts data into the correct table.
    Correct SQL query and data used, connection is committed and closed.
    """
    mock_conn, mock_cur = mock_db_connection
    func(data)
    mock_cur.executemany.assert_called_once_with(expected_sql, data)
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

@pytest.mark.parametrize(
    "func, data, exception_type",
    [
        (enter_players, [("1", "player1", 1000, "guild1", "2023-01-01")], psycopg2.IntegrityError),
        (enter_gp_logs, [("1", 1000)], psycopg2.Error),
        (enter_player_check, [("True", "True", "False", "True", "True", "1")], psycopg2.Error),
        (enter_tickets, [("1", 100)], psycopg2.IntegrityError),
        (enter_raid_score_log, [("1", 100000, 0.95)], psycopg2.Error),
        (enter_player_archive, [("1", "player1", 1000, "guild1")], psycopg2.Error),
        (enter_tb_data, [("player1", 10000, 5, 5, 1.0, 0)], psycopg2.IntegrityError),
    ],
)
def test_data_insertion_failure(mock_db_connection, func, data, exception_type):
    """
    Each function handles database errors correctly.
    Connection is rolled back and closed on error.
    """
    mock_conn, mock_cur = mock_db_connection
    mock_cur.executemany.side_effect = exception_type("Mocked error")
    func(data)
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()

def test_enter_player_archive_no_data(mock_db_connection):
    """
    Case: enter_player_archive with no data.
    """
    mock_conn, mock_cur = mock_db_connection
    enter_player_archive([])
    mock_cur.executemany.assert_not_called()
    mock_conn.commit.assert_not_called()
    mock_conn.close.assert_not_called()

def test_enter_tb_data_no_data(mock_db_connection):
    """
    Case: enter_tb_data with no data.
    """
    mock_conn, mock_cur = mock_db_connection
    enter_tb_data([])
    mock_cur.executemany.assert_not_called()
    mock_conn.commit.assert_not_called()
    mock_conn.close.assert_not_called()
