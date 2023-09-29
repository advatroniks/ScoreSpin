from src.api_v1.auth.hash_password import get_password_hash


def test_hash_password():
    plain_password = '123'
    lol = (get_password_hash(plain_password))
    print(lol)
    assert plain_password != lol