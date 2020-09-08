from starlette import status
from starlette.testclient import TestClient

from run_server import app


client = TestClient(app)


def test_hello_world():
    response = client.get("/hello")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "Hello, world!"}
