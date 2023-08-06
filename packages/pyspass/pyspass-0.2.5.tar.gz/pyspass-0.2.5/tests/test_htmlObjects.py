from pyspass import HtmlBody, HtmlForm, HtmlH1, HtmlH2, HtmlH3, HtmlDiv, HtmlCell


class TestHtmlObjects:
    def test_str(self):
        body = HtmlBody()
        assert str(body).startswith("<body>")
        assert str(body).endswith("</body>\n")

    def test_h1_str(self):
        h1 = HtmlH1()
        assert str(h1).replace('\n', ''), '<h1></h1>'

    def test_h2_str(self):
        h2 = HtmlH2()
        assert str(h2).replace('\n', ''), '<h2></h2>'

    def test_h3_str(self):
        h3 = HtmlH3()
        assert str(h3).replace('\n', ''), '<h3></h3>'

    def test_containter_return_added_objects(self):
        div = HtmlDiv()
        cell = HtmlCell()
        return_value = div.add(cell)
        assert cell == return_value

    def test_containter_return_themselfs_if_string_added(self):
        div = HtmlDiv()
        return_value = div.add('abc')
        assert div == return_value

    def test_pass_parent_to_child(self):
        form = HtmlForm(id_html='id_form123')
        div = form.div()
        assert div.parent == form

    def test_pass_parent_to_child_by_reference(self):
        form = HtmlForm(id_html='id_form123')
        div = form.div()
        assert id(div.parent) == id(form)

    def test_string_composition(self):
        div = HtmlDiv()
        assert str(div).startswith('<div>')  # no blank in tag
        div = HtmlDiv(id_html='id')
        assert str(div).startswith('<div id="id">')  # one blank in tag

    def test_get_parent_form_1up(self):
        div = HtmlDiv()
        form = div.form(id_html="1level")
        div_sub = form.div()
        assert div_sub.get_form() == form

    def test_get_parent_form_3up(self):
        """test recursive search of form"""
        div = HtmlDiv()
        form = div.form(id_html="1level")
        div_1sub = form.div()
        div_2sub = div_1sub.div()
        div_3sub = div_2sub.div()
        assert div_3sub.get_form() == form

    def test_indents(self):
        div = HtmlDiv()
        div2 = HtmlDiv()
        div.add(div2)
        # todo elaborate
