from unittest.mock import Mock, patch

from jsonschema import ValidationError, validators

from app.errors import InputValidationError, SchemaValidationError
from app.validator import validate_input, validate_schema


@patch('app.request.get_json')
def test_validate_input(mock_get_json: Mock) -> None:
    called = False

    mock_get_json.return_value = {
        'key1': 'value1',
        'key2': 'value2',
    }

    matcher1 = Mock('app.validator.Matcher', autospec=True)
    matcher1.validate = Mock(return_value=[])
    matcher2 = Mock('app.validator.Matcher', autospec=True)
    matcher2.validate = Mock(return_value=[])

    @validate_input({
        'key1': matcher1,
        'key2': matcher2,
    })
    def function(arg1: str, arg2: int) -> int:
        nonlocal called
        called = True

        assert arg1 == 'string'
        assert arg2 == 23

        return 6

    assert function('string', arg2=23) == 6

    mock_get_json.assert_called_once_with()
    matcher1.validate.assert_called_once_with('value1', 'key1')
    matcher2.validate.assert_called_once_with('value2', 'key2')


@patch('app.request.get_json')
def test_validate_input_with_error(mock_get_json: Mock) -> None:
    mock_get_json.return_value = {
        'key1': 'value1',
        'key2': 'value2',
    }

    matcher1 = Mock('app.validator.Matcher', autospec=True)
    matcher1.validate = Mock(return_value=[{'error': 1}, {'error': 2}])
    matcher2 = Mock('app.validator.Matcher', autospec=True)
    matcher2.validate = Mock(return_value=[{'error': 3}])

    @validate_input({
        'key1': matcher1,
        'key2': matcher2,
    })
    def function() -> None:
        pass

    try:
        function()
    except Exception as e:
        assert isinstance(e, InputValidationError)
        assert e.errors == [{'error': 1}, {'error': 2}, {'error': 3}]
    else:
        assert False, 'should throw exception'

    mock_get_json.assert_called_once_with()
    matcher1.validate.assert_called_once_with('value1', 'key1')
    matcher2.validate.assert_called_once_with('value2', 'key2')


@patch('app.request.get_json')
def test_validate_schema(mock_get_json: Mock) -> None:
    called = False

    mock_validator = Mock('jsonschema.validators.Draft7Validator', autospec=True)
    validators.Draft7Validator = mock_validator

    validator_instance = mock_validator.return_value
    validator_instance.iter_errors = Mock(return_value=iter([]))

    mock_get_json.return_value = {
        'key1': 'value1',
        'key2': 'value2',
    }

    @validate_schema({
        'properties': {
            'name': 'value',
        }
    })
    def function(arg1: str, arg2: int) -> int:
        nonlocal called
        called = True

        assert arg1 == 'string'
        assert arg2 == 23

        return 6

    mock_validator.assert_called_once_with({
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'additionalProperties': False,
        'properties': {
            'name': 'value',
        }
    })

    assert function('string', arg2=23) == 6

    mock_get_json.assert_called_once_with()
    validator_instance.iter_errors.assert_called_once_with({
        'key1': 'value1',
        'key2': 'value2',
    })


@patch('app.request.get_json')
def test_validate_schema_with_error(mock_get_json: Mock) -> None:
    error = ValidationError('msg')

    mock_validator = Mock('jsonschema.validators.Draft7Validator', autospec=True)
    validators.Draft7Validator = mock_validator

    validator_instance = mock_validator.return_value
    validator_instance.iter_errors = Mock(return_value=iter([error]))

    mock_get_json.return_value = {
        'key1': 'value1',
        'key2': 'value2',
    }

    @validate_schema({
        'properties': {
            'name': 'value',
        }
    })
    def function() -> None:
        pass

    mock_validator.assert_called_once_with({
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'additionalProperties': False,
        'properties': {
            'name': 'value',
        }
    })

    try:
        function()
    except Exception as e:
        assert isinstance(e, SchemaValidationError)
        assert e.errors == [error]
    else:
        assert False, 'should throw exception'

    mock_get_json.assert_called_once_with()
    validator_instance.iter_errors.assert_called_once_with({
        'key1': 'value1',
        'key2': 'value2',
    })
