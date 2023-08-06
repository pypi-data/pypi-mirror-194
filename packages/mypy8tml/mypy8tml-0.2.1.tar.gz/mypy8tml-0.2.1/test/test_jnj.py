from mypy_8tml import MyPy8TML


class Test:

    def test_jnj(self):
        html = MyPy8TML()
        html.jnj('test')
        assert html.generate() == '{test}\n'

    def test_jnj_expretion(self):
        html = MyPy8TML()
        html.jnj_expretion('test')
        assert html.generate() == '{{ test }}\n'

    def test_jnj_comand(self):
        html = MyPy8TML()
        html.jnj_comand('test')
        assert html.generate() == '{% test %}\n'

    def test_jnj_coment(self):
        html = MyPy8TML()
        html.jnj_coment('test')
        assert html.generate() == '{# test #}\n'

    def test_jnj_elif(self):
        html = MyPy8TML()
        html.jnj_elif('test')
        assert html.generate() == '{% elif test %}\n'

    def test_jnj_else(self):
        html = MyPy8TML()
        html.jnj_else()
        assert html.generate() == '{% else %}\n'

    def test_jnj_endif(self):
        html = MyPy8TML()
        html.jnj_endif()
        assert html.generate() == '{% endif %}\n'

    def test_jnj_if(self):
        html = MyPy8TML()
        html.jnj_if('test')
        assert html.generate() == '{% if test %}\n'

    def test_extends_temp(self):
        html = MyPy8TML()
        html.jnj_extends_temp('test')
        assert html.generate() == '{% extends test %}\n'

    def test_include_temp(self):
        html = MyPy8TML()
        html.jnj_include_temp('test')
        assert html.generate() == '{% include test %}\n'

    def test_jnj_add_bootstrap(self):
        html = MyPy8TML()
        jnj = '{%bootstrat%}\n{{ super() }}\n{{ bootstrap.load_css() }}\n{{ bootstrap.load_js() }}\n{% endblock %}\n'
        html.jnj_add_bootstrap()
        assert html.generate() == jnj