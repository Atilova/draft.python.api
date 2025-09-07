def test_true_is_true():
    result = print("Ok") or True

    assert result
