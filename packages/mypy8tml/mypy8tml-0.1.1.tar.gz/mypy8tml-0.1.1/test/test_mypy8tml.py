from mypy_8tml import MyPy8TML
from random import Random


class Test:

    def test_put_another_(self):
        html = MyPy8TML()
        html.p['class="test"', 'in']()
        assert html.generate() == '<p class="test" ></p>\n'
    def test_content_in(self):
        html = MyPy8TML()
        html.p['class="test"', 'in']()
        assert html.generate() == '<p class="test" ></p>\n'

    def test__add__method(self):
        html = MyPy8TML()
        html = html.p + 'test'
        assert html.generate() == '<p>test</p>'

    def test_content_out(self):
        html = MyPy8TML()
        html.p['test', 'out']()
        assert html.generate() == '<p>test</p>\n'

    def test_downline_inline_close(self):
        html = MyPy8TML()
        html.p(-1).p(-1)
        assert html.generate() == '<p></p><p></p>'

    def test_downline_inline_with_randown_num_arg_greather_than_1(self):
        num = round(Random().random() * 10) + 1
        html = MyPy8TML()
        expected = ''
        for n in range(num):
            _ = html.p(-1)
            expected += '<p></p>'

        assert html.generate() == expected

    def test_downline_no_agrs(self):
        html = MyPy8TML()
        html.p.downline().p.downline()
        assert html.generate() == '<p></p>\n' \
                                  '<p></p>\n'

    def test__call_with_no_close_no_agrs(self):
        html = MyPy8TML()
        html.img(-1).img(-1)
        assert html.generate() == '<img>\n' \
                                  '<img>\n'

    def test__call__no_agrs(self):
        html = MyPy8TML()
        html.p().p()
        assert html.generate() == '<p></p>\n' \
                                  '<p></p>\n'

    def test__call__inline_close(self):
        html = MyPy8TML()
        html.p(-1).p(-1)
        assert html.generate() == '<p></p><p></p>'

    def test_init_html(self):
        html = MyPy8TML()
        html.init_html(
            title='test',
            lang='en'
        )
        expected =f'<!DOCTYPE html>\n' \
                  f'<html lang="en" >\n' \
                  f'<head><meta charset="UTF-8" >\n' \
                  f'<title>test</title>\n' \
                  f'</head>\n' \
                  f'<body></body>'

        assert html.generate() == expected

    def test_if_init_html_puts_code_on_boody(self):
        html = MyPy8TML()
        html.init_html(
            title='test',
            lang='en'
        ).p['code']()

        expected = f'<!DOCTYPE html>\n' \
                   f'<html lang="en" >\n' \
                   f'<head><meta charset="UTF-8" >\n' \
                   f'<title>test</title>\n' \
                   f'</head>\n' \
                   f'<body><p>code</p>\n' \
                   f'</body>'

        assert html.generate() == expected

    def test_if_MyPy8TML_can_recive_other_MyPy8TML(self):
        html1 = MyPy8TML()
        html2 = MyPy8TML()
        p = html1.p['test']
        p2 = html2.p[p].generate()
        assert p2 == '<p><p>test</p></p>'

    def test_set_file_name(self):
        html = MyPy8TML()
        html.set_filename('test')
        assert html._file_name == 'test'

    def test_closed_tags_in_content(self):
        html = MyPy8TML()
        html.p(-1)['<img/>'].in_src('test')
        print()
        assert html.generate() == '<p></p><img src="test" />'

    def test_p(self):
        html = MyPy8TML()
        p = html.p.generate()
        assert p == '<p></p>'

    def test_h1(self):
        html = MyPy8TML()
        h1 = html.h1.generate()
        assert h1 == "<h1></h1>"

    def test_h2(self):
        html = MyPy8TML()
        h2 = html.h2.generate()
        assert h2 == "<h2></h2>"

    def test_h3(self):
        html = MyPy8TML()
        h3 = html.h3.generate()
        assert h3 == "<h3></h3>"

    def test_h4(self):
        html = MyPy8TML()
        h4 = html.h4.generate()
        assert h4 == "<h4></h4>"

    def test_h5(self):
        html = MyPy8TML()
        h5 = html.h5.generate()
        assert h5 == "<h5></h5>"

    def test_h6(self):
        html = MyPy8TML()
        h6 = html.h6.generate()
        assert h6 == "<h6></h6>"

    def test_a(self):
        html = MyPy8TML()
        a = html.a.generate()
        assert a == "<a></a>"

    def test_strong(self):
        html = MyPy8TML()
        strong = html.strong.generate()
        assert strong == "<strong></strong>"

    def test_em(self):
        html = MyPy8TML()
        em = html.em.generate()
        assert em == "<em></em>"

    def test_small(self):
        html = MyPy8TML()
        small = html.small.generate()
        assert small == "<small></small>"

    def test_s(self):
        html = MyPy8TML()
        s = html.s.generate()
        assert s == "<s></s>"

    def test_div(self):
        html = MyPy8TML()
        s = html.div.generate()
        assert s == "<div></div>"

    def test_head(self):
        html = MyPy8TML()
        s = html.head.generate()
        assert s == "<head></head>"

    def test_section(self):
        html = MyPy8TML()
        s = html.section.generate()
        assert s == "<section></section>"

    def test_ul(self):
        html = MyPy8TML()
        s = html.ul.generate()
        assert s == "<ul></ul>"

    def test_li(self):
        html = MyPy8TML()
        s = html.li.generate()
        assert s == "<li></li>"

    def test_br(self):
        html = MyPy8TML()
        s = html.br.generate()
        assert s == "<br>"

    def test_pre(self):
        html = MyPy8TML()
        s = html.pre.generate()
        assert s == "<pre></pre>"

    def test_footer(self):
        html = MyPy8TML()
        s = html.footer.generate()
        assert s == "<footer></footer>"

    def test_span(self):
        html = MyPy8TML()
        s = html.span.generate()
        assert s == "<span></span>"

    def test_q(self):
        html = MyPy8TML()
        q = html.q.generate()
        assert q == "<q></q>"

    def test_cite(self):
        html = MyPy8TML()
        cite = html.cite.generate()
        assert cite == "<cite></cite>"

    def test_dfn(self):
        html = MyPy8TML()
        dfn = html.dfn.generate()
        assert dfn == "<dfn></dfn>"

    def test_abbr(self):
        html = MyPy8TML()
        abbr = html.abbr.generate()
        assert abbr == "<abbr></abbr>"

    def test_data(self):
        html = MyPy8TML()
        data = html.data.generate()
        assert data == "<data></data>"

    def test_time(self):
        html = MyPy8TML()
        time = html.time.generate()
        assert time == "<time></time>"

    def test_code(self):
        html = MyPy8TML()
        code = html.code.generate()
        assert code == "<code></code>"

    def test_var(self):
        html = MyPy8TML()
        var = html.var.generate()
        assert var == "<var></var>"

    def test_samp(self):
        html = MyPy8TML()
        samp = html.samp.generate()
        assert samp == "<samp></samp>"

    def test_kbd(self):
        html = MyPy8TML()
        kbd = html.kbd.generate()
        assert kbd == "<kbd></kbd>"

    def test_sup(self):
        html = MyPy8TML()
        sup = html.sup.generate()
        assert sup == "<sup></sup>"

    def test_sub(self):
        html = MyPy8TML()
        sub = html.sub.generate()
        assert sub == "<sub></sub>"

    def test_i(self):
        html = MyPy8TML()
        i = html.i.generate()
        assert i == "<i></i>"

    def test_b(self):
        html = MyPy8TML()
        b = html.b.generate()
        assert b == "<b></b>"

    def test_u(self):
        html = MyPy8TML()
        u = html.u.generate()
        assert u == "<u></u>"

    def test_mark(self):
        html = MyPy8TML()
        mark = html.mark.generate()
        assert mark == "<mark></mark>"

    def test_img(self):
        html = MyPy8TML()
        img = html.img.generate()
        assert img == "<img>"

    def test_video(self):
        html = MyPy8TML()
        video = html.video.generate()
        assert video == "<video></video>"

    def test_audio(self):
        html = MyPy8TML()
        audio = html.audio.generate()
        assert audio == "<audio></audio>"

    def test_source(self):
        html = MyPy8TML()
        source = html.source.generate()
        assert source == "<source>"

    def test_track(self):
        html = MyPy8TML()
        track = html.track.generate()
        assert track == "<track>"

    def test_map(self):
        html = MyPy8TML()
        map = html.map.generate()
        assert map == "<map></map>"

    def test_area(self):
        html = MyPy8TML()
        area = html.area.generate()
        assert area == "<area>"

    def test_object(self):
        html = MyPy8TML()
        object = html.object.generate()
        assert object == "<object></object>"

    def test_embed(self):
        html = MyPy8TML()
        embed = html.embed.generate()
        assert embed == "<embed>"

    def test_iframe(self):
        html = MyPy8TML()
        iframe = html.iframe.generate()
        assert iframe == "<iframe></iframe>"

    def test_canvas(self):
        html = MyPy8TML()
        canvas = html.canvas.generate()
        assert canvas == "<canvas></canvas>"

    def test_svg(self):
        html = MyPy8TML()
        svg = html.svg.generate()
        assert svg == "<svg></svg>"

    def test_table(self):
        html = MyPy8TML()
        table = html.table.generate()
        assert table == "<table></table>"

    def test_thead(self):
        html = MyPy8TML()
        thead = html.thead.generate()
        assert thead == "<thead></thead>"

    def test_tbody(self):
        html = MyPy8TML()
        tbody = html.tbody.generate()
        assert tbody == "<tbody></tbody>"

    def test_tfoot(self):
        html = MyPy8TML()
        tfoot = html.tfoot.generate()
        assert tfoot == "<tfoot></tfoot>"

    def test_tr(self):
        html = MyPy8TML()
        tr = html.tr.generate()
        assert tr == "<tr></tr>"

    def test_th(self):
        html = MyPy8TML()
        th = html.th.generate()
        assert th == "<th></th>"

    def test_td(self):
        html = MyPy8TML()
        td = html.td.generate()
        assert td == "<td></td>"

    def test_col(self):
        html = MyPy8TML()
        col = html.col.generate()
        assert col == "<col>"

    def test_colgroup(self):
        html = MyPy8TML()
        colgroup = html.colgroup.generate()
        assert colgroup == "<colgroup></colgroup>"

    def test_caption(self):
        html = MyPy8TML()
        caption = html.caption.generate()
        assert caption == "<caption></caption>"

    def test_form(self):
        html = MyPy8TML()
        form = html.form.generate()
        assert form == "<form></form>"

    def test_input(self):
        html = MyPy8TML()
        input = html.input.generate()
        assert input == "<input>"

    def test_button(self):
        html = MyPy8TML()
        button = html.button.generate()
        assert button == "<button></button>"

    def test_select(self):
        html = MyPy8TML()
        select = html.select.generate()
        assert select == "<select></select>"

    def test_datalist(self):
        html = MyPy8TML()
        datalist = html.datalist.generate()
        assert datalist == "<datalist></datalist>"

    def test_optgroup(self):
        html = MyPy8TML()
        optgroup = html.optgroup.generate()
        assert optgroup == "<optgroup></optgroup>"

    def test_option(self):
        html = MyPy8TML()
        option = html.option.generate()
        assert option == "<option></option>"

    def test_textarea(self):
        html = MyPy8TML()
        textarea = html.textarea.generate()
        assert textarea == "<textarea></textarea>"

    def test_label(self):
        html = MyPy8TML()
        label = html.label.generate()
        assert label == "<label></label>"

    def test_fieldset(self):
        html = MyPy8TML()
        fieldset = html.fieldset.generate()
        assert fieldset == "<fieldset></fieldset>"

    def test_legend(self):
        html = MyPy8TML()
        legend = html.legend.generate()
        assert legend == "<legend></legend>"

    def test_output(self):
        html = MyPy8TML()
        output = html.output.generate()
        assert output == "<output></output>"

    def test_progress(self):
        html = MyPy8TML()
        progress = html.progress.generate()
        assert progress == "<progress></progress>"

    def test_meter(self):
        html = MyPy8TML()
        meter = html.meter.generate()
        assert meter == "<meter></meter>"

    def test_header(self):
        html = MyPy8TML()
        head = html.header.generate()
        assert head == "<header></header>"

    def test_nav(self):
        html = MyPy8TML()
        head = html.nav.generate()
        assert head == "<nav></nav>"

    def test_title(self):
        html = MyPy8TML()
        title = html.title.generate()
        assert title == "<title></title>"

    def test_meta(self):
        html = MyPy8TML()
        meta = html.meta.generate()
        assert meta == "<meta>"

    def test_style(self):
        html = MyPy8TML()
        style = html.style.generate()
        assert style == "<style></style>"

    def test_link(self):
        html = MyPy8TML()
        link = html.link.generate()
        assert link == "<link>"

    def test_script(self):
        html = MyPy8TML()
        script = html.script.generate()
        assert script == "<script></script>"

    def test_noscript(self):
        html = MyPy8TML()
        noscript = html.noscript.generate()
        assert noscript == "<noscript></noscript>"

    def test_template(self):
        html = MyPy8TML()
        template = html.template.generate()
        assert template == "<template></template>"

    def test_slot(self):
        html = MyPy8TML()
        slot = html.slot.generate()
        assert slot == "<slot></slot>"

    def test_body(self):
        html = MyPy8TML()
        body = html.body.generate()
        assert body == "<body></body>"
    def test_in_class(self):
        html = MyPy8TML()
        html.p.in_class('test')()
        assert html.generate() == '<p class="test" ></p>\n'

    def test_in_alt(self):
        html = MyPy8TML()
        html.p.in_alt( 'test' )
        assert html.generate() == '<p alt="test" ></p>'

    def test_in_method(self):
        html = MyPy8TML()
        html.p.in_method( 'test' )
        assert html.generate() == '<p method="test" ></p>'

    def test_in_type(self):
        html = MyPy8TML()
        html.p.in_type( 'test' )
        assert html.generate() == '<p type="test" ></p>'

    def test_in_title(self):
        html = MyPy8TML()
        html.p.in_title( 'test' )
        assert html.generate() == '<p title="test" ></p>'

    def test_in_bgcolor(self):
        html = MyPy8TML()
        html.p.in_bgcolor( 'test' )
        assert html.generate() == '<p bgcolor="test" ></p>'

    def test_in_src(self):
        html = MyPy8TML()
        html.p.in_src( 'test' )
        assert html.generate() == '<p src="test" ></p>'

    def test_in_width(self):
        html = MyPy8TML()
        html.p.in_width( 'test' )
        assert html.generate() == '<p width="test" ></p>'

    def test_in_colspan(self):
        html = MyPy8TML()
        html.p.in_colspan( 'test' )
        assert html.generate() == '<p colspan="test" ></p>'

    def test_in_cols(self):
        html = MyPy8TML()
        html.p.in_cols( 'test' )
        assert html.generate() == '<p cols="test" ></p>'

    def test_in_rows(self):
        html = MyPy8TML()
        html.p.in_rows( 'test' )
        assert html.generate() == '<p rows="test" ></p>'

    def test_in_accesskey(self):
        html = MyPy8TML()
        html.p.in_accesskey( 'test' )
        assert html.generate() == '<p accesskey="test" ></p>'

    def test_in_border(self):
        html = MyPy8TML()
        html.p.in_border( 'test' )
        assert html.generate() == '<p border="test" ></p>'

    def test_in_action(self):
        html = MyPy8TML()
        html.p.in_action( 'test' )
        assert html.generate() == '<p action="test" ></p>'

    def test_in_rowspan(self):
        html = MyPy8TML()
        html.p.in_rowspan( 'test' )
        assert html.generate() == '<p rowspan="test" ></p>'

    def test_in_value(self):
        html = MyPy8TML()
        html.p.in_value( 'test' )
        assert html.generate() == '<p value="test" ></p>'

    def test_in_lang(self):
        html = MyPy8TML()
        html.p.in_lang( 'test' )
        assert html.generate() == '<p lang="test" ></p>'

    def test_in_style(self):
        html = MyPy8TML()
        html.p.in_style( 'test' )
        assert html.generate() == '<p style="test" ></p>'

    def test_in_cellpadding(self):
        html = MyPy8TML()
        html.p.in_cellpadding( 'test' )
        assert html.generate() == '<p cellpadding="test" ></p>'

    def test_in_height(self):
        html = MyPy8TML()
        html.p.in_height( 'test' )
        assert html.generate() == '<p height="test" ></p>'

    def test_in_cellspacing(self):
        html = MyPy8TML()
        html.p.in_cellspacing( 'test' )
        assert html.generate() == '<p cellspacing="test" ></p>'

    def test_in_target(self):
        html = MyPy8TML()
        html.p.in_target( 'test' )
        assert html.generate() == '<p target="test" ></p>'

    def test_in_id(self):
        html = MyPy8TML()
        html.p.in_id( 'test' )
        assert html.generate() == '<p id="test" ></p>'

    def test_in_tabindex(self):
        html = MyPy8TML()
        html.p.in_tabindex( 'test' )
        assert html.generate() == '<p tabindex="test" ></p>'

    def test_in_name(self):
        html = MyPy8TML()
        html.p.in_name( 'test' )
        assert html.generate() == '<p name="test" ></p>'

    def test_in_href(self):
        html = MyPy8TML()
        html.p.in_href( 'test' )
        assert html.generate() == '<p href="test" ></p>'

    def test_in_for(self):
        html = MyPy8TML()
        html.p.in_for('test')
        assert html.generate() == '<p for="test" ></p>'

    def test_import_html(self):
        html = MyPy8TML()
        html.import_html('test/test_files/test.html')
        assert html.generate() == '<p>test</p>'

    def test_import_css(self):
        html = MyPy8TML()
        html.import_style('test/test_files/test.css')
        assert html.generate() == '<style>test{}</style>\n'


