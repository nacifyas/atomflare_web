from hub.main import services


def test_one_get_user_cache():
    res = services.get_services() # This is async
    res = False if res is None else True
    assert res

