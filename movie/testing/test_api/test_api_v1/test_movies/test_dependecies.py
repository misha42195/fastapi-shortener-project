from api.api_v1.movies.dependecies import UNSAVE_METHODS


def test_unsave_methods_doesnt_contain_save_methods() -> None:
    assert not {"GET", "HEAD", "OPTIONS"} & UNSAVE_METHODS
