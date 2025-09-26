"""
Testing file for:
    api_request.py
    remove_data.py
    log_tickets.py
    csv_import.py
"""
from datetime import datetime, time
import os
import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
import pytest
import psycopg2
from unittest.mock import Mock, patch, ANY, call

from src.api_request import post_request
from src.remove_data import remove_from_players
import src.log_tickets as log_tickets
import src.csv_import as csv_import


class TestApiRequest:
    """
    Unit tests for the api_request.py module
    """

    def test_successful_post_guild(self, mocker):
        """
        Tests a successful POST request returning guild member data
        """
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
        """
        Tests handling of a failed POST request (non-200 status code)
        """
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

    @pytest.fixture
    def mock_env_vars(self):
        """
        Mocks environment variables for database connection
        """
        env_vars = {
            'PASS': 'password',
            'HOST': 'test_host',
            'USER': 'test_user',
            'DBNAME': 'test_db',
            'PORT': '1235'

        }
        with patch.dict(os.environ, env_vars):
            yield env_vars


    @pytest.fixture
    def mock_db(self):
        """
        Mocks the database connection and cursor
        """
        mock_conn: Mock = Mock()
        mock_cursor: Mock = Mock()

        mock_cursor_manager = Mock()
        mock_cursor_manager.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor_manager.__exit__ = Mock(return_value=None)

        mock_conn.cursor.return_value = mock_cursor_manager

        return mock_conn, mock_cursor
    

    def test_remove_from_players_successful_one(self, mock_db, mock_env_vars):
        """
        Tests removing a single player successfully
        """
        load_dotenv()
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


    def test_remove_from_players_successful_multiple(self, mock_db, mock_env_vars):
        """
        Tests removing multiple players successfully
        """
        load_dotenv()
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


    def test_remove_from_players_no_edits(self, mock_db, mock_env_vars):
        """
        Tests the scenario where no rows are affected (no players removed)
        """
        load_dotenv()
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

    def test_remove_from_players_db_error(self, mock_db, mock_env_vars):
        """
        Tests handling of a database error during the removal process
        """
        load_dotenv()
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
            mock_conn.commit.assert_not_called()


class TestLogTickets(unittest.TestCase):

    def test_is_around_reset_time(self):
        """
        Tests the reset time checking logic with various scenarios
        """
        reset_t = time(18, 30, 0)
        
        # Scenario 1: Within the 2-minute window (should be True)
        now_in_window = datetime(2023, 1, 1, 18, 28, 1)
        self.assertTrue(log_tickets.is_around_reset_time(reset_t, now=now_in_window))
        
        # Scenario 2: Exactly at reset time (should be True)
        now_at_reset = datetime(2023, 1, 1, 18, 30, 0)
        self.assertTrue(log_tickets.is_around_reset_time(reset_t, now=now_at_reset))

        # Scenario 3: Outside the window, too early (should be False)
        now_too_early = datetime(2023, 1, 1, 18, 27, 59)
        self.assertFalse(log_tickets.is_around_reset_time(reset_t, now=now_too_early))

        # Scenario 4: Outside the window, too late (should be False)
        now_too_late = datetime(2023, 1, 1, 18, 30, 1)
        self.assertFalse(log_tickets.is_around_reset_time(reset_t, now=now_too_late))

        # Scenario 5: Edge case crossing midnight
        reset_t_midnight = time(0, 0, 30)
        now_crossing_midnight = datetime(2023, 1, 1, 23, 58, 31)
        self.assertTrue(log_tickets.is_around_reset_time(reset_t_midnight, now=now_crossing_midnight))


    @patch('src.log_tickets.enter_tickets')
    @patch('src.log_tickets.post_request')
    @patch('src.log_tickets.is_around_reset_time')
    @patch('src.log_tickets.read_guild')
    @patch('src.log_tickets.os.getenv')
    def test_process_ticket_log_successful_path(
        self, mock_getenv, mock_read_guild, mock_is_reset, mock_post, mock_enter_tickets
    ):
        """
        Tests the main logic with a successful run for one guild
        """
        mock_getenv.return_value = "http://api-url.com"
        mock_read_guild.return_value = [("G1", "Test Guild", time(19, 0))]
        mock_is_reset.return_value = True
        
        mock_api_data = {
            "guild": {
                "member": [
                    {
                        "playerId": "P1_FULL",
                        "memberContribution": [{"type": 2, "currentValue": 600}]
                    },
                    {
                        "playerId": "P2_PARTIAL",
                        "memberContribution": [{"type": 2, "currentValue": 500}]
                    },
                    {
                        "playerId": "P3_ZERO",
                        "memberContribution": [{"type": 2, "currentValue": 0}]
                    }
                ]
            }
        }
        mock_post.return_value = mock_api_data

        log_tickets.process_ticket_log()

        mock_post.assert_called_once()
        expected_tickets_to_log = [("P2_PARTIAL", 100), ("P3_ZERO", 600)]
        
        mock_enter_tickets.assert_called_once()
        self.assertIsInstance(mock_enter_tickets.call_args[0][0], list)
        self.assertCountEqual(mock_enter_tickets.call_args[0][0], expected_tickets_to_log)


    @patch('src.log_tickets.enter_tickets')
    @patch('src.log_tickets.post_request')
    @patch('src.log_tickets.is_around_reset_time')
    @patch('src.log_tickets.read_guild')
    @patch('src.log_tickets.os.getenv')
    def test_process_ticket_log_not_reset_time(
        self, mock_getenv, mock_read_guild, mock_is_reset, mock_post, mock_enter_tickets
    ):
        """
        Tests that guilds are skipped if it's not their reset time
        """

        mock_getenv.return_value = "http://api-url.com"
        mock_read_guild.return_value = [("G1", "Test Guild", time(19, 0))]
        mock_is_reset.return_value = False

        log_tickets.process_ticket_log()

        mock_post.assert_not_called()
        mock_enter_tickets.assert_not_called()
        

    @patch('src.log_tickets.enter_tickets')
    @patch('src.log_tickets.post_request')
    @patch('src.log_tickets.is_around_reset_time')
    @patch('src.log_tickets.read_guild')
    @patch('src.log_tickets.os.getenv')
    def test_process_ticket_log_multiple_guilds_one_active(
        self, mock_getenv, mock_read_guild, mock_is_reset, mock_post, mock_enter_tickets
    ):
        """
        Tests processing multiple guilds where only one is at its reset time
        """
        mock_getenv.return_value = "http://api-url.com"
        mock_read_guild.return_value = [
            ("G1", "Active Guild", time(19, 0)),
            ("G2", "Inactive Guild", time(20, 0))
        ]

        mock_is_reset.side_effect = [True, False]
        mock_post.return_value = {"guild": {"member": []}}

        log_tickets.process_ticket_log()

        mock_is_reset.assert_has_calls([
            call(time(19, 0)),
            call(time(20, 0))
        ])
        mock_post.assert_called_once()
        
        mock_enter_tickets.assert_not_called()


import unittest
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock, call

# Add the parent directory to the path to allow importing from `src`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module after the path is set
import src.csv_import as csv_import


class TestCSVImport(unittest.TestCase):
    """
    Unit tests for the csv_import.py module
    """

    def setUp(self):
        """
        Setup a mock CSV import path for the tests
        """
        self.mock_csv_path = "/mock/csv/folder/"

    # Patch the global variable directly.
    @patch('src.csv_import.csv_import_folder_filepath', '/mock/csv/folder/')
    @patch('src.csv_import.get_guild_from_nickname')
    @patch('src.csv_import.enter_tb_data')
    @patch('src.csv_import.pd.read_csv')
    @patch('pathlib.Path.rename')
    def test_import_tb_data_success(self, mock_rename, mock_read_csv, mock_enter_tb_data, mock_get_guild_from_nickname):
        """
        Tests the successful import and processing of a valid TB data CSV.
        """
        # Mock the CSV file content as a pandas DataFrame
        mock_data = {
            "Name": ["player1", "player2", "player3"],
            "Total Territory Points": [1000, 2000, 3000],
            "Combat Waves_P1": [5, 6, 7],
            "Combat Attempts_P1": [5, 6, 7],
            "Combat Waves_P2": [3, 4, 5],
            "Combat Attempts_P2": [3, 4, 5],
            "Deployed GP_P1": [1, 1, 1],
            "Deployed GP_P2": [1, 1, 0]
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_csv.return_value = mock_df

        mock_get_guild_from_nickname.side_effect = ["Guild A"] * 10
        
        with patch('numpy.random.randint', return_value=np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 0])):
            # Run the function to be tested
            csv_import.import_tb_data()
            
            # Verify the CSV was read correctly
            mock_read_csv.assert_called_once_with(
                f"{self.mock_csv_path}tb_data.csv",
                encoding="utf-8",
                sep=",",
                header=0,
            )
            
            # Check if the data was processed correctly before being passed to enter_tb_data
            expected_list = [
                ['player1', 1000, 8, 8, 0.5, 0],
                ['player2', 2000, 10, 10, 0.5, 0],
                ['player3', 3000, 12, 12, 0.5, 1]
            ]
            mock_enter_tb_data.assert_called_once_with(expected_list)
            
            # Check if the file was renamed correctly
            mock_rename.assert_called_once()
            
            # Correctly access the single positional argument
            new_path = mock_rename.call_args[0][0] 
            
            self.assertIn(f"{self.mock_csv_path}tb_data_imported_", new_path)
            self.assertIn("_Guild A.csv", new_path)

    @patch('src.csv_import.csv_import_folder_filepath', '/mock/csv/folder/')
    @patch('src.csv_import.pd.read_csv', side_effect=pd.errors.EmptyDataError)
    @patch('src.csv_import.enter_tb_data')
    def test_import_tb_data_empty_file(self, mock_enter_tb_data, mock_read_csv):
        csv_import.import_tb_data()
        mock_read_csv.assert_called_once()
        mock_enter_tb_data.assert_not_called()
        
    @patch('src.csv_import.csv_import_folder_filepath', '/mock/csv/folder/')
    @patch('src.csv_import.pd.read_csv', side_effect=FileNotFoundError)
    @patch('src.csv_import.enter_tb_data')
    def test_import_tb_data_file_not_found(self, mock_enter_tb_data, mock_read_csv):
        csv_import.import_tb_data()
        mock_read_csv.assert_called_once()
        mock_enter_tb_data.assert_not_called()

    @patch('src.csv_import.get_guild_from_nickname', return_value="Guild A")
    @patch('src.csv_import.np.random.randint', return_value=np.array([0, 0, 0]))
    def test_get_guild_random_single_guild(self, mock_randint, mock_get_guild):
        input_list = [["player1"], ["player2"], ["player3"]]
        guild_name = csv_import.get_guild_random(input_list)
        self.assertEqual(guild_name, "Guild A")
        mock_get_guild.assert_has_calls([call("player1")] * 3)

    @patch('src.csv_import.get_guild_from_nickname', side_effect=["Guild A", "Guild A", "Guild B", "Guild A", "Guild B", "Guild A", "Guild B", "Guild B", "Guild B", "Guild B"])
    @patch('src.csv_import.np.random.randint', return_value=np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    def test_get_guild_random_multiple_guilds(self, mock_randint, mock_get_guild):
        input_list = [["p1"], ["p2"], ["p3"], ["p4"], ["p5"], ["p6"], ["p7"], ["p8"], ["p9"], ["p10"]]
        guild_name = csv_import.get_guild_random(input_list)
        self.assertEqual(guild_name, "Guild B")