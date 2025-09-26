import unittest
import psycopg2
from unittest.mock import patch, MagicMock, call
from datetime import datetime


import src.read_data as read_data

class TestReadData(unittest.TestCase):
    """
    Tests for database reading functions in read_data.py
    """

    @patch('src.read_data.get_env')
    def test_setup_connection(self, mock_get_env):
        """
        Tests that setup_connection correctly builds the connection dictionary
        """

        env_vars = {
            "PASS": "test_password",
            "HOST": "test_host",
            "USER": "test_user",
            "DBNAME": "test_db",
            "PORT": "1234"
        }
        mock_get_env.side_effect = lambda key: env_vars[key]
        
        expected_dict = {
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_password",
            "port": 1234,
            "host": "test_host",
        }
        
        self.assertEqual(read_data.setup_connection(), expected_dict)
        mock_get_env.assert_has_calls([
            call("PASS"), call("HOST"), call("USER"), call("DBNAME"), call("PORT")
        ])

    def test_get_valid_order_parameter(self):
        """
        Tests the SQL injection prevention for order parameters
        """
        # Valid parameter
        self.assertEqual(read_data.get_valid_order_parameter('nickname ASC'), 'nickname ASC')

        # Another valid parameter
        self.assertEqual(read_data.get_valid_order_parameter('total_gp DESC'), 'total_gp DESC')

        # Invalid parameter (should return default)
        self.assertEqual(read_data.get_valid_order_parameter('DROP TABLE users;'), 'nickname ASC')
        
    def test_get_valid_timeframe_parameter(self):
        """
        Tests the SQL injection prevention for timeframe parameters
        """
        # Valid parameters
        self.assertEqual(read_data.get_valid_timeframe_parameter('two_weeks'), 'two_weeks')
        self.assertEqual(read_data.get_valid_timeframe_parameter('month'), 'month')

        # Invalid parameter (should return default)
        self.assertEqual(read_data.get_valid_timeframe_parameter('year'), 'nickname ASC')


    @patch('src.read_data.psycopg2.connect')
    @patch('src.read_data.setup_connection')
    def test_make_sql_query_single_success(self, mock_setup_connection, mock_connect):
        """
        Tests a successful database query execution
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("player1",), ("player2",)]

        sql_query_str = "SELECT nickname FROM players;"
        query_source = "players"
        result = read_data.make_sql_query_single(sql_query_str, query_source)

        self.assertEqual(result, [("player1",), ("player2",)])
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(sql_query_str)
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()
    

    @patch('src.read_data.psycopg2.connect')
    @patch('src.read_data.setup_connection')
    def test_make_sql_query_single_no_data(self, mock_setup_connection, mock_connect):
        """
        Tests a query that returns no rows
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        sql_query_str = "SELECT * FROM guild WHERE guild_id = 'invalid_id';"
        query_source = "guild"
        result = read_data.make_sql_query_single(sql_query_str, query_source)
        
        self.assertEqual(result, [])
        mock_connect.assert_called_once()
        mock_conn.close.assert_called_once()
    

    @patch('src.read_data.psycopg2.connect', side_effect=psycopg2.Error("Connection failed"))
    @patch('src.read_data.setup_connection')
    def test_make_sql_query_single_connection_error(self, mock_setup_connection, mock_connect):
        """
        Tests error handling for a failed database connection
        """
        result = read_data.make_sql_query_single("SELECT * FROM guild;", "guild")
        self.assertEqual(result, [])
        mock_connect.assert_called_once()

    @patch('src.read_data.make_sql_query_single')
    def test_read_guild(self, mock_make_sql_query_single):
        """
        Tests the read_guild function calls the underlying function correctly
        """
        expected_data = [("G1", "Guild Alpha", "18:00:00")]
        mock_make_sql_query_single.return_value = expected_data
        
        result = read_data.read_guild()
        
        self.assertEqual(result, expected_data)
        mock_make_sql_query_single.assert_called_once_with("SELECT * FROM guild;", "guild")

    @patch('src.read_data.make_sql_query_single')
    def test_read_players(self, mock_make_sql_query_single):
        """
        Tests the read_players function with a specific guild ID
        """
        guild_id = "123"
        expected_data = [("p1", "Player One"), ("p2", "Player Two")]
        mock_make_sql_query_single.return_value = expected_data
        
        result = read_data.read_players(guild_id)
        
        self.assertEqual(result, expected_data)
        mock_make_sql_query_single.assert_called_once_with(
            "SELECT * FROM players WHERE guild_id::text = %s ORDER BY nickname DESC;", 
            "players", 
            (guild_id,)
        )


    @patch('src.read_data.get_valid_order_parameter', return_value='nickname ASC')
    @patch('src.read_data.make_sql_query_single')
    def test_read_players_data_valid_order(self, mock_make_sql, mock_get_valid_order):
        """
        Tests read_players_data with a valid order string
        """
        guild_id = 'test_guild'
        order_str = 'nickname ASC'
        mock_make_sql.return_value = [('p1',), ('p2',)]
        
        result = read_data.read_players_data(guild_id, order_str)
        
        mock_get_valid_order.assert_called_once_with(order_str)
        mock_make_sql.assert_called_once()
        query_str = mock_make_sql.call_args[0][0]
        self.assertIn("ORDER BY nickname ASC", query_str)
        self.assertEqual(result, [('p1',), ('p2',)])


    @patch('src.read_data.get_valid_order_parameter', return_value='tickets_lost_week ASC')
    @patch('src.read_data.make_sql_query_single')
    def test_read_tickets_weekly(self, mock_make_sql, mock_get_valid_order):
        """
        Tests read_tickets_weekly with a valid order string
        """
        guild_id = 'test_guild'
        order_str = 'tickets_lost_week ASC'
        mock_make_sql.return_value = [('p1', 100, 2, 1), ('p2', 0, 0, 0)]
        
        result = read_data.read_tickets_weekly(guild_id, order_str)
        
        mock_get_valid_order.assert_called_once_with(order_str)
        mock_make_sql.assert_called_once()
        query_str = mock_make_sql.call_args[0][0]
        self.assertIn("ORDER BY tickets_lost_week ASC", query_str)
        self.assertEqual(result, [('p1', 100, 2, 1), ('p2', 0, 0, 0)])


    @patch('src.read_data.make_sql_query_single')
    def test_get_guild_from_nickname_found(self, mock_make_sql_query_single):
        """
        Tests getting a guild name from a nickname when the player is found
        """
        mock_make_sql_query_single.return_value = [("Test Guild",)]
        
        result = read_data.get_guild_from_nickname("test_player")
        
        self.assertEqual(result, "Test Guild")
        mock_make_sql_query_single.assert_called_once()


    @patch('src.read_data.make_sql_query_single')
    def test_get_guild_from_nickname_not_found(self, mock_make_sql_query_single):
        """
        Tests getting a guild name from a nickname when the player is not found
        """
        mock_make_sql_query_single.return_value = []
        
        result = read_data.get_guild_from_nickname("nonexistent_player")
        
        self.assertEqual(result, "")
        mock_make_sql_query_single.assert_called_once()


    @patch('src.read_data.get_valid_order_parameter', return_value='total_waves_completed DESC')
    @patch('src.read_data.make_sql_query_single')
    def test_get_last_tb_data_ordered(self, mock_make_sql, mock_get_valid_order):
        """
        Tests get_last_tb_data_ordered with a valid order
        """
        guild_id = 'test_guild'
        order_str = 'total_waves_completed DESC'
        mock_make_sql.return_value = [('p1', 1000, 10, 5, 0.5, 0, datetime(2023, 1, 1))]
        
        result = read_data.get_last_tb_data_ordered(guild_id, order_str)
        
        mock_get_valid_order.assert_called_once_with(order_str)
        mock_make_sql.assert_called_once()
        query_str = mock_make_sql.call_args[0][0]
        self.assertIn("ORDER BY total_waves_completed DESC", query_str)
        self.assertEqual(result, [('p1', 1000, 10, 5, 0.5, 0, datetime(2023, 1, 1))])


    @patch('src.read_data.get_valid_order_parameter', return_value='score_difference DESC')
    @patch('src.read_data.get_valid_timeframe_parameter', return_value='two_weeks')
    @patch('src.read_data.make_sql_query_single')
    def test_read_raid_progression(self, mock_make_sql, mock_get_valid_timeframe, mock_get_valid_order):
        """
        Tests read_raid_progression with a valid timeframe and order
        """
        guild_id = 'test_guild'
        timeframe = 'two_weeks'
        order_str = 'score_difference DESC'
        mock_make_sql.return_value = [('p1', 'success', 100), ('p2', 'fail', -50)]
        
        result = read_data.read_raid_progression(guild_id, timeframe, order_str)

        mock_get_valid_timeframe.assert_called_once_with(timeframe)
        mock_get_valid_order.assert_called_once_with(order_str)
        mock_make_sql.assert_called_once()
        query_str = mock_make_sql.call_args[0][0]
        self.assertIn("raid_progression_two_weeks", query_str)
        self.assertIn("ORDER BY score_difference DESC", query_str)
        self.assertEqual(result, [('p1', 'success', 100), ('p2', 'fail', -50)])
        