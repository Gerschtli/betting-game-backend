import os
import time

import pytest
from flask import Flask

os.environ['TZ'] = 'Europe/Berlin'
time.tzset()


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app
