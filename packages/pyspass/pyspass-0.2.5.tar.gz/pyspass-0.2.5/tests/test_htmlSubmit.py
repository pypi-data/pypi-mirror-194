from pyspass import HtmlSubmit


class TestHtmlSubmit:

    def test_constructor_with_html_class(self):
        submit = HtmlSubmit(name="test_button", value="test_label", class_html='test_class')
        assert 'test_class"' in str(submit)
