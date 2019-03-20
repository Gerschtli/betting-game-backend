import logging
import sys
from unittest.mock import Mock, patch

import app
from app.config import default as default_config


@patch('app.modules.register_blueprints')
@patch('app.errors.register_error_handler')
@patch('logging.basicConfig')
@patch('flask_migrate.Migrate', autospec=True)
@patch('app.jwt.jwt', autospec=True)
@patch('app.models.db')
@patch('flask.Flask', autospec=True)
def test_create_app(
        mock_flask: Mock,
        mock_db: Mock,
        mock_jwt: Mock,
        mock_migrate: Mock,
        mock_basic_config: Mock,
        mock_error_handler: Mock,
        mock_blueprints: Mock,
) -> None:
    mock_config = Mock('flask.Config', autospec=True)
    mock_config.from_object = Mock()
    mock_config.from_envvar = Mock()

    flask_instance = mock_flask.return_value
    flask_instance.config = mock_config

    mock_db.init_app = Mock()

    result = app.create_app()

    mock_flask.assert_called_once_with('app')
    mock_config.from_object.assert_called_once_with(default_config)
    mock_config.from_envvar.assert_called_once_with('APP_CONFIG_FILE')

    mock_db.init_app.assert_called_once_with(flask_instance)
    mock_jwt.init_app.assert_called_once_with(flask_instance)
    mock_migrate.assert_called_once_with(flask_instance, mock_db)

    mock_basic_config.assert_called_once_with(
        level=logging.DEBUG,
        stream=sys.stdout,
    )

    mock_error_handler.assert_called_once_with(flask_instance)
    mock_blueprints.assert_called_once_with(flask_instance)

    assert result == flask_instance
