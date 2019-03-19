from unittest.mock import Mock, patch

from app import request


@patch('flask.request')
def test_get_json(mock_request: Mock) -> None:
    mock_request.get_json = Mock(return_value=1)

    assert request.get_json() == 1
