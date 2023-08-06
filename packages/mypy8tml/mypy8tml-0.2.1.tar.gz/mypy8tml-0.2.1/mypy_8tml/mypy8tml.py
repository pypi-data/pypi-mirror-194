class MyPy8TML:
    """ Generete html using comands on  python """
    def __init__(self, file_name: str = None, path: str = None):
        self._html: str = ''
        self._close: list = []
        self._final_atribut: str = None
        self._file_name: str = file_name
        self._path: str = path

    def __add__(self, other: str):
        """ Add a string into a html """
        self._html += other
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Creates a html file with code when's with ends """
        if self._path:
            self.to_html(self._file_name, path=self._path)
        else:
            self.to_html(self._file_name, path='')

    def __enter__(self):
        """ Starts with returning self """
        return self

    def __getitem__(self, item: str or tuple[str, str] or object):
        """
        getitem used in this case to add content inside or out of a tag
        :param item:            Any string or a tuple (str, 'in' or 'out')
        :argument item[1]:      if == 'in' put the content inside a tag if == 'out' contents go out
        """
        self._verify_html()
        if type(item) == tuple:
            content, kind = item
            if kind == 'in':
                return self.in_content(content)
            elif kind == 'out':
                return self.content(content)
            else:
                raise ValueError(f'kind {kind} doesent exist!')
        elif type(item) == str:
            return self.content(str(item))
        try:
            item._is_self()
            return self[item.generate()]
        except Exception:
            raise TypeError(f'This method dont suports {type(item)}')

    def __call__(self, times: int = 1, inline: str = '-'):
        if self._get_final_atribut():
            self.downline(times)
            return self
        else:
            self.simple_down(times)
            return self

    @staticmethod
    def _is_self():
        """ Method to checks if class is MyPy8TML """
        return True

    def generate(self) -> str:
        """ This method generetes the html final code. """
        self._verify_html()
        return self._html + '\n'.join(self._close[::-1])

    def content(self, content: str):
        """ Add content to main html code """
        self._html += content
        return self

    def set_filename(self, name: str):
        """ Set the name of output file """
        self._file_name: str = name
        return self

    def _verify_html(self) -> None:
        """ Verify if the hmtl was empty """
        if len(self._html) == 0:
            raise ValueError('Your html was empty.')

    def _verify_if_are_close(self) -> None:
        """ Verify if html was closed """
        return self._html[-2:] == '/>'

    def _get_final_atribut(self):
        """ Get final attribute from html code """
        if len(self._close) > 0:
            return self._final_atribut == self._close[-1].replace('/', '')
        return False

    def in_content(self, content: str):
        """
        Puts content inside a tag
        :param content:     any kind of content ex: class='just-a-class'
        :return:            self
        """
        self._verify_html()
        if self._verify_if_are_close():
            self._html = self._html[:-2]
            self._html += f' {content} />'
            return self
        else:
            self._html = self._html[:-1]
            self._html += f' {content} >'
            return self

    def downline(self, times: int = 1):
        """
        This method allows to close a tag
        :param times:               Number of tags that you want to go down in a code
                                    if negative close tag inline
        :return:                    self
        """
        self._verify_html()
        if times > 0:
            for time in range(times):
                content = self._close.pop(-1)
                self._html += f'{content}\n'
        else:
            times = times * -1
            for time in range(times):
                content = self._close.pop(-1)
                self._html += f'{content}'
        return self

    def simple_down(self, times: int = 1):
        """
        This method allows to just jump for next line
        :param times:           Number of tags that you want to go down in a code
                                if negative close tag inline
        :return: self
        """
        if times > 0:
            for time in range(times):
                self._html += f'\n'
        else:
            times = times * -1
            for times in range(times):
                self._html += f'\n'
        return self

    def _tag(self, tag, is_open: bool = True):
        """
        A generic method to a simple tag
        :param tag:         name of tag exemple <body>
        :type tag:          str
        :param is_open:     if the tag needs to be closed
        :type is_open:      bool
        :return: self
        """
        clean_tag = tag.replace('<', '').replace('>', '')
        self._html += tag
        self._final_atribut = tag
        if is_open:
            self._close.append(f'</{clean_tag}>')

    # Tags HTML

    @property
    def header(self):
        self._tag("<header>", is_open=True)
        return self

    @property
    def div(self):
        self._tag("<div>", is_open=True)
        return self

    @property
    def h1(self):
        self._tag("<h1>", is_open=True)
        return self

    @property
    def h2(self):
        self._tag("<h2>", is_open=True)
        return self

    @property
    def h3(self):
        self._tag("<h3>", is_open=True)
        return self

    @property
    def h4(self):
        self._tag("<h4>", is_open=True)
        return self

    @property
    def h5(self):
        self._tag("<h5>", is_open=True)
        return self

    @property
    def h6(self):
        self._tag("<h6>", is_open=True)
        return self

    @property
    def p(self):
        self._tag("<p>", is_open=True)
        return self

    @property
    def a(self):
        self._tag( "<a>", is_open=True )
        return self

    @property
    def strong(self):
        self._tag( "<strong>", is_open=True )
        return self

    @property
    def nav(self):
        self._tag("<nav>", is_open=True)
        return self

    @property
    def em(self):
        self._tag("<em>", is_open=True)
        return self

    @property
    def small(self):
        self._tag( "<small>", is_open=True )
        return self

    @property
    def s(self):
        self._tag( "<s>", is_open=True )
        return self

    @property
    def q(self):
        self._tag( "<q>", is_open=True )
        return self

    @property
    def cite(self):
        self._tag( "<cite>", is_open=True )
        return self

    @property
    def dfn(self):
        self._tag( "<dfn>", is_open=True )
        return self

    @property
    def abbr(self):
        self._tag( "<abbr>", is_open=True )
        return self

    @property
    def data(self):
        self._tag( "<data>", is_open=True )
        return self

    @property
    def time(self):
        self._tag( "<time>", is_open=True )
        return self

    @property
    def code(self):
        self._tag( "<code>", is_open=True )
        return self

    @property
    def var(self):
        self._tag( "<var>", is_open=True )
        return self

    @property
    def samp(self):
        self._tag( "<samp>", is_open=True )
        return self

    @property
    def kbd(self):
        self._tag( "<kbd>", is_open=True )
        return self

    @property
    def sup(self):
        self._tag( "<sup>", is_open=True )
        return self

    @property
    def sub(self):
        self._tag( "<sub>", is_open=True )
        return self

    @property
    def i(self):
        self._tag("<i>", is_open=True)
        return self

    @property
    def section(self):
        self._tag("<section>", is_open=True)
        return self

    @property
    def b(self):
        self._tag( "<b>", is_open=True )
        return self

    @property
    def u(self):
        self._tag( "<u>", is_open=True )
        return self

    @property
    def mark(self):
        self._tag( "<mark>", is_open=True )
        return self

    @property
    def img(self):
        self._tag( "<img>", is_open=False )
        return self

    @property
    def video(self):
        self._tag( "<video>", is_open=True )
        return self

    @property
    def audio(self):
        self._tag( "<audio>", is_open=True )
        return self

    @property
    def source(self):
        self._tag( "<source>", is_open=False )
        return self

    @property
    def track(self):
        self._tag( "<track>", is_open=False )
        return self

    @property
    def map(self):
        self._tag( "<map>", is_open=True )
        return self

    @property
    def area(self):
        self._tag( "<area>", is_open=False )
        return self

    @property
    def object(self):
        self._tag( "<object>", is_open=True )
        return self

    @property
    def embed(self):
        self._tag( "<embed>", is_open=False )
        return self

    @property
    def iframe(self):
        self._tag( "<iframe>", is_open=True )
        return self

    @property
    def canvas(self):
        self._tag( "<canvas>", is_open=True )
        return self

    @property
    def svg(self):
        self._tag( "<svg>", is_open=True )
        return self

    @property
    def table(self):
        self._tag( "<table>", is_open=True )
        return self

    @property
    def thead(self):
        self._tag( "<thead>", is_open=True )
        return self

    @property
    def tbody(self):
        self._tag( "<tbody>", is_open=True )
        return self

    @property
    def tfoot(self):
        self._tag( "<tfoot>", is_open=True )
        return self

    @property
    def tr(self):
        self._tag( "<tr>", is_open=True )
        return self

    @property
    def th(self):
        self._tag( "<th>", is_open=True )
        return self

    @property
    def td(self):
        self._tag( "<td>", is_open=True )
        return self

    @property
    def li(self):
        self._tag( "<li>", is_open=True )
        return self

    @property
    def ul(self):
        self._tag( "<ul>", is_open=True )
        return self

    @property
    def col(self):
        self._tag( "<col>", is_open=False )
        return self

    @property
    def colgroup(self):
        self._tag( "<colgroup>", is_open=True )
        return self

    @property
    def caption(self):
        self._tag( "<caption>", is_open=True )
        return self

    @property
    def form(self):
        self._tag( "<form>", is_open=True )
        return self

    @property
    def input(self):
        self._tag( "<input>", is_open=False )
        return self

    @property
    def button(self):
        self._tag( "<button>", is_open=True )
        return self

    @property
    def select(self):
        self._tag( "<select>", is_open=True )
        return self

    @property
    def datalist(self):
        self._tag( "<datalist>", is_open=True )
        return self

    @property
    def optgroup(self):
        self._tag( "<optgroup>", is_open=True )
        return self

    @property
    def option(self):
        self._tag( "<option>", is_open=True )
        return self

    @property
    def textarea(self):
        self._tag( "<textarea>", is_open=True )
        return self

    @property
    def label(self):
        self._tag( "<label>", is_open=True )
        return self

    @property
    def fieldset(self):
        self._tag( "<fieldset>", is_open=True )
        return self

    @property
    def legend(self):
        self._tag( "<legend>", is_open=True )
        return self

    @property
    def output(self):
        self._tag( "<output>", is_open=True )
        return self

    @property
    def progress(self):
        self._tag( "<progress>", is_open=True )
        return self

    @property
    def meter(self):
        self._tag( "<meter>", is_open=True )
        return self

    @property
    def head(self):
        self._tag( "<head>", is_open=True )
        return self

    @property
    def title(self):
        self._tag( "<title>", is_open=True )
        return self

    @property
    def meta(self):
        self._tag( "<meta>", is_open=False )
        return self

    @property
    def style(self):
        self._tag( "<style>", is_open=True )
        return self

    @property
    def link(self):
        self._tag( "<link>", is_open=False )
        return self

    @property
    def script(self):
        self._tag( "<script>", is_open=True )
        return self

    @property
    def noscript(self):
        self._tag( "<noscript>", is_open=True )
        return self

    @property
    def template(self):
        self._tag("<template>", is_open=True)
        return self

    @property
    def br(self):
        self._tag("<br>", is_open=False)
        return self

    @property
    def slot(self):
        self._tag( "<slot>", is_open=True )
        return self

    @property
    def pre(self):
        self._tag( "<pre>", is_open=True )
        return self

    @property
    def doctype(self):
        self._tag( "<!DOCTYPE html>", is_open=False )
        return self

    @property
    def html(self):
        self._tag( "<html>", is_open=False )
        return self

    @property
    def body(self):
        self._tag( "<body>", is_open=True )
        return self

    @property
    def footer(self):
        self._tag( "<footer>", is_open=True )
        return self

    @property
    def span(self):
        self._tag( "<span>", is_open=True)
        return self

    #  html inside tags

    def in_alt(self, value: str):
        self.in_content( f'alt="{value}"' )
        return self

    def in_method(self, value: str):
        self.in_content( f'method="{value}"' )
        return self

    def in_type(self, value: str):
        self.in_content( f'type="{value}"' )
        return self

    def in_title(self, value: str):
        self.in_content( f'title="{value}"' )
        return self

    def in_for(self, value: str):
        self.in_content(f'for="{value}"')
        return self

    def in_bgcolor(self, value: str):
        self.in_content(f'bgcolor="{value}"')
        return self

    def in_src(self, value: str):
        self.in_content( f'src="{value}"' )
        return self

    def in_width(self, value: str):
        self.in_content( f'width="{value}"' )
        return self

    def in_colspan(self, value: str):
        self.in_content(f'colspan="{value}"')
        return self

    def in_cols(self, value: str):
        self.in_content(f'cols="{value}"')
        return self

    def in_rows(self, value: str):
        self.in_content(f'rows="{value}"')
        return self

    def in_accesskey(self, value: str):
        self.in_content(f'accesskey="{value}"')
        return self

    def in_border(self, value: str):
        self.in_content(f'border="{value}"')
        return self

    def in_class(self, value: str):
        self.in_content(f'class="{value}"')
        return self

    def in_action(self, value: str):
        self.in_content(f'action="{value}"')
        return self

    def in_rowspan(self, value: str):
        self.in_content(f'rowspan="{value}"')
        return self

    def in_value(self, value: str):
        self.in_content(f'value="{value}"')
        return self

    def in_lang(self, value: str):
        self.in_content(f'lang="{value}"')
        return self

    def in_style(self, value: str):
        self.in_content(f'style="{value}"')
        return self

    def in_cellpadding(self, value: str):
        self.in_content(f'cellpadding="{value}"')
        return self

    def in_height(self, value: str):
        self.in_content(f'height="{value}"')
        return self

    def in_cellspacing(self, value: str):
        self.in_content(f'cellspacing="{value}"')
        return self

    def in_target(self, value: str):
        self.in_content(f'target="{value}"')
        return self

    def in_id(self, value: str):
        self.in_content(f'id="{value}"')
        return self

    def in_tabindex(self, value: str):
        self.in_content(f'tabindex="{value}"')
        return self

    def in_name(self, value: str):
        self.in_content(f'name="{value}"')
        return self

    def in_href(self, value: str):
        self.in_content(f'href="{value}"')
        return self

    # Jinja in code

    def jnj(self, expretion):
        self.content("{" + expretion + "}\n")
        return self

    def jnj_add_bootstrap(self):
        self.jnj_block('bootstrat')\
            .jnj_expretion('super()') \
            .jnj_expretion('bootstrap.load_css()')\
            .jnj_expretion('bootstrap.load_js()')\
            .jnj_endblock()
        return self

    def jnj_expretion(self, expretion):
        self.content("{{ " + expretion + " }}\n")
        return self

    def jnj_comand(self, comand):
        self.content("{% " + comand + " %}\n")
        return self

    def jnj_coment(self, coment):
        self.content("{# " + coment + " #}\n")
        return self

    def jnj_if(self, expretion):
        self.content("{% if " + expretion + " %}\n")
        return self

    def jnj_elif(self, expretion):
        self.content( "{% elif " + expretion + " %}\n" )
        return self

    def jnj_else(self):
        self.content("{% else %}\n")
        return self

    def jnj_endif(self):
        self.content("{% endif %}\n")
        return self

    def jnj_block(self, name: str):
        self.content("{%" + name + "%}\n")
        return self

    def jnj_endblock(self):
        self.content("{% endblock %}\n")
        return self

    def jnj_extends_temp(self, template: str):
        self.content("{% extends " + template + " %}\n")
        return self

    def jnj_include_temp(self, template: str):
        self.content("{% include " + template + " %}\n")
        return self

    def init_html(self, title, lang: str, charset="UTF-8", inhead: str = ''):
        """
        Generates the stat of a html code until the bod

        <!DOCTYPE html>
        <html lang=":param lang:"}>
        <head>
            :param inhead:
            <meta charset=":param charset:">
            <title>:param title:</title>
        </head>
        <body> {UNTIL HERE}

        :param title:               title of your html page
        :param lang:                 lang of html
        :param charset:              charset of html
        :param inhead:               puts content un head
        :return:                     self
        """
        _ = self \
            .doctype() \
            .html[f'lang="{lang}"', 'in']()\
            .head[inhead]\
            .meta[f'charset="{charset}"', 'in']()\
            .title[title](2)\
            .body
        return self

    def import_style(self, style_path, encoding='UTF-8'):
        """
        Import style from css code
        :param style_path:             Path to the css code
        :param encoding:               encoding of css code
        :return:                       return self
        """
        with open(style_path, 'rt', encoding=encoding) as file:
            css: str = file.read()
            _ = self.style[css]()
        return self

    # todo: this method was never tested
    def import_html(self, style_path, charset='UTF-8') -> None:
        """
        Import html code from file code
        :param style_path:             Path to the css code
        :param charset:               encoding of css code
        :return:                       return self
        """
        with open(style_path, 'rt', encoding=charset) as file:
            html: str = file.read()
            _ = self.content(html)
        return self

    def to_html(self, name: str, path: str = '') -> None:
        """ Export to Html
        :param name:        name of html code with sufix
        :param path:        path to put code with slash bar
        :return: None
        """
        with open(f'{path}{name}', 'w') as arq:
            arq.write(self.generate())

    dnl = downline
    sdnl = simple_down
