from tim import Tim


def test_licenses(client: Tim):
    result = client.licenses.details_license()

    assert result is not None
