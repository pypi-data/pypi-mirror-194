import os
from mypy_8tml import MyPy8TML


class TestWith:

    def test_with_context_generates_a_file(self):
        with MyPy8TML(file_name='index.html', path='test/templates/') as index:
            index.p['test']()
        assert 'index.html' in os.listdir('test/templates/')
        os.remove('test/templates/index.html')

    def test_with_context_generates_a_file_withopu_path(self):
        with MyPy8TML(file_name='test/templates/index.html') as index:
            index.p['test']()
        assert 'index.html' in os.listdir('test/templates/')
        os.remove('test/templates/index.html')

    def test_if_with_generates_coerent_code(self):
        with MyPy8TML(file_name='index.html', path='test/templates/') as index:
            index.p['test']()
        with open('test/templates/index.html', 'rt') as arq:
            assert index.generate() == arq.read()
        os.remove('test/templates/index.html')



