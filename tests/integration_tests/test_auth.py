from src.services.auth import AuthService


def test_encode_and_decode_jwt_payload():
    data = {"id": 1}
    jwt_token = AuthService.create_jwt_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService.decode_jwt_token(jwt_token)
    assert payload
    assert payload == data["id"]
