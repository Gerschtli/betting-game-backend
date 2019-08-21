import uuid
from unittest.mock import Mock, patch

from app.uuid import generate


@patch('uuid.uuid4')
def test_generate(mock_uuid: Mock) -> None:
    mock_uuid.return_value = 'uuid'

    assert generate() == 'uuid'
