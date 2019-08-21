from unittest.mock import Mock

from flask import Flask

from app.config import get


def test_get(app: Flask) -> None:
    with app.app_context():  # type: ignore
        app.config = Mock()
        app.config.get = Mock(return_value='value')  # type: ignore

        assert get('key') == 'value'

        app.config.get.assert_called_once_with('key')  # type: ignore
