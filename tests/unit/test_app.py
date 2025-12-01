import os
import tempfile
import pytest
from app.app import app, init_db, DB_PATH

@pytest.fixture
def client(tmp_path, monkeypatch):
    # use a temporary DB file for tests
    tmp_db = tmp_path / "test.db"
    monkeypatch.setenv("FLASK_ENV", "testing")
    # point DB_PATH in module to tmp_db
    from importlib import reload
    import app.app as appmod
    appmod.DB_PATH = str(tmp_db)
    appmod.init_db()
    appmod.app.config['TESTING'] = True
    with appmod.app.test_client() as client:
        yield client

def test_index_loads(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Submit a Message' in rv.data

def test_submit_message(client):
    rv = client.post('/submit', data={'username':'unit','message':'hello unit'}, follow_redirects=True)
    assert b'Message submitted' in rv.data
    rv2 = client.get('/')
    assert b'hello unit' in rv2.data
