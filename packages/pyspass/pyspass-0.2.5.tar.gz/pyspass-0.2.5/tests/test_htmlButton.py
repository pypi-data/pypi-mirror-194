from pyspass import HtmlButton


class TestHtmlButton:

    def test_constructor_with_html_class(self):
        button = HtmlButton(name="test_button", value="test_label", class_html='test_class')
        assert 'test_class"' in str(button)
