import sys
import os
import pytest
from unittest.mock import MagicMock, patch

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)



@pytest.fixture
def mock_db_connection(monkeypatch):
    """
    Fixture to mock the psycopg2 connection and cursor.

    """
    mock_cur = MagicMock()
    mock_conn = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cur
    mock_conn.cursor.return_value.__exit__.return_value = None

    with patch('psycopg2.connect', return_value=mock_conn) as mock_connect:

        monkeypatch.setattr("src.enter_data.setup_connection", lambda: {})
        
        monkeypatch.setattr("src.enter_data.get_env", lambda x: "dummy")
        monkeypatch.setattr("src.enter_data.setup_logging", MagicMock())

        yield mock_conn, mock_cur
