import urllib.request


def test_true_is_true():
    result = print("Ok") or True

    with urllib.request.urlopen("http://nginx") as response:
        status = response.status
        data = response.read().decode("utf-8")

    print("Status code: ", status)
    print("Response body: ", data)

    assert result
