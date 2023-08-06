from pyspass import HtmlDiv


class TestHtmlTextInput:

    def test_textinput_with_alignment(self):
        div = HtmlDiv()
        div.textinput(name="test", var_input=123, alignment="right")
        assert 'style="text-align: right"' in str(div)

    def test_textinput_with_class(self):
        div = HtmlDiv()
        div.textinput(name="test", var_input=123, class_html="my_class")
        assert 'my_class' in str(div)
