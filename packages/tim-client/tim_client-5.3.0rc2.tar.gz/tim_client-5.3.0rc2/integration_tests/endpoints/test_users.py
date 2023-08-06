from tim import Tim


def test_users(client: Tim):
    result = client.users.details_user()

    assert result is not None
