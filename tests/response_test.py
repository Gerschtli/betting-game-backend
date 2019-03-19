from http import HTTPStatus

from app.response import no_content


def test_no_content() -> None:
    response = no_content()

    assert response.data == b''
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.headers.get('Content-Type') == 'text/plain; charset=utf-8'
