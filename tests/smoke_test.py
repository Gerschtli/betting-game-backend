from app import app


def test_function() -> None:
    assert 1 == 1


def test_app() -> None:
    assert app is not None
