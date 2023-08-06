import pytest
from mypy_8tml import MyPy8TML


class Test:

    def test_error_content_kind__getitem__(self):
        with pytest.raises(ValueError):
            html = MyPy8TML()
            assert html.p['test', 'test']

    def test_error_content_wrong_type_(self):
        with pytest.raises(TypeError):
            html = MyPy8TML()
            assert html.p['test':'test']

    def test_empty_error(self):
        with pytest.raises(ValueError):
            html = MyPy8TML()
            assert html['test', 'in']
