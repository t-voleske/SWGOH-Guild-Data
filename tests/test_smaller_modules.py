"""
Testing file for files:
api_request.py
remove_data.py
log_tickets.py

"""

import pytest
import psycopg2
from unittest.mock import Mock, patch, ANY

from src.api_request import post_request
from src.remove_data import remove_from_players
from src.log_tickets import is_around_reset_time
# from src.csv_import import get_guild_random


class TestApiRequest:


    def test_successful_post_guild(self, mocker):
        mock_setup_logging: Mock = mocker.patch("src.api_request.setup_logging")
        mock_post: Mock = mocker.patch("src.api_request.requests.post")

        url = "https://test.api/endpoint"
        data = {"payload": {"guildId": "Guild_Id"}}
        expected_response = {"guild": {"member": ["m1", "m2", "m3"]}}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_post.return_value = mock_response

        result = post_request(url, data)

        assert result == expected_response
        mock_post.assert_called_once_with(url, json=data, timeout=30)
        mock_setup_logging.assert_called_once()


    def test_failed_post(self, mocker):
        mock_setup_logging: Mock = mocker.patch("src.api_request.setup_logging")
        mock_post: Mock = mocker.patch("src.api_request.requests.post")

        url = "https://test.api/endpoint"
        data = {"payload": {}}


        mock_response: Mock = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        result = post_request(url, data)

        assert result is None
        mock_post.assert_called_once_with(url, json=data, timeout=30)
        mock_setup_logging.assert_called_once()
        assert mock_response.status_code == 400


class TestRemoveData:

    @staticmethod
    @pytest.fixture
    def mock_db():
        mock_conn: Mock = Mock()
        mock_cursor: Mock = Mock()

        # Create context manager for cursor
        mock_cursor_manager = Mock()
        mock_cursor_manager.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor_manager.__exit__ = Mock(return_value=None)

        mock_conn.cursor.return_value = mock_cursor_manager

        return mock_conn, mock_cursor
    

    def test_remove_from_players_successful_one(self, mock_db):
        mock_conn, mock_cursor = mock_db

        with (
            patch("src.remove_data.psycopg2.connect") as mock_connect, 
            patch("src.remove_data.logger") as mock_logger
        ):
            mock_connect .return_value = mock_conn
            mock_cursor.rowcount = 1

            remove_from_players(("player_1",))

            mock_cursor.executemany.assert_called_once_with(
                "DELETE FROM players WHERE player_id = %s;",
                ("player_1",)
            )
            mock_conn.commit.assert_called_once()
            mock_logger.info.assert_any_call("Removed %s old guild members", 1)


    def test_remove_from_players_successful_multiple(self, mock_db):
        mock_conn, mock_cursor = mock_db

        with (
            patch("src.remove_data.psycopg2.connect") as mock_connect, 
            patch("src.remove_data.logger") as mock_logger
        ):
            mock_connect .return_value = mock_conn
            mock_cursor.rowcount = 3

            remove_from_players(("player_1","player_2","player_3",))

            mock_cursor.executemany.assert_called_once_with(
                "DELETE FROM players WHERE player_id = %s;",
                ("player_1","player_2","player_3",)
            )
            mock_conn.commit.assert_called_once()
            mock_logger.info.assert_any_call("Removed %s old guild members", 3)


    def test_remove_from_players_no_edits(self, mock_db):
        mock_conn, mock_cursor = mock_db

        with (
            patch("src.remove_data.psycopg2.connect") as mock_connect, 
            patch("src.remove_data.logger") as mock_logger
        ):
            mock_connect .return_value = mock_conn
            mock_cursor.rowcount = 0

            remove_from_players(())

            mock_cursor.assert_not_called()
            mock_conn.commit.assert_not_called()
            mock_logger.info.assert_any_call("No players to remove.")

    def test_remove_from_players_db_error(self, mock_db):
        mock_conn, mock_cursor = mock_db

        with (
            patch("src.remove_data.psycopg2.connect") as mock_connect,
            patch("src.remove_data.logger") as mock_logger
        ):
            mock_connect.return_value = mock_conn
            
            mock_cursor.executemany.side_effect = psycopg2.Error("Simulated DB error")

            remove_from_players(("player_1",))


            mock_conn.rollback.assert_called_once()
            mock_conn.close.assert_called_once()
            mock_logger.error.assert_called_once_with(
                "Database error: %s", ANY
            )
            mock_conn.commit.assert_not_called() # should not be called


class TestAroundResetTime:


    @staticmethod
    @pytest.fixture
    def mock_time():
        mock_current_time: Mock = Mock()
        mock_time_in_2_minutes: Mock = Mock()

        return mock_current_time, mock_time_in_2_minutes
    
    #test_successful_time_check(mock_time)