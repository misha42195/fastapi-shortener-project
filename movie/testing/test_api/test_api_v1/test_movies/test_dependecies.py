from api.api_v1.movies.dependecies import UNSAVE_METHODS


class TestUnsaveMethod:
    def test_method_doesnt_contain_save_methods(self) -> None:
        save_methods = {"GET", "HEAD", "OPTIONS"}
        assert not save_methods & UNSAVE_METHODS

    def test_method_are_all_uppercase(self) -> None:
        assert all(method.isupper() for method in UNSAVE_METHODS)
