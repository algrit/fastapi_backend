from src.services.auth import AuthService


def test_create_jwt_token():
    data = {"id": 1}
    jwt_token = AuthService.create_jwt_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)
