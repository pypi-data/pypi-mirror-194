from pyspass import HtmlDiv


class TestHtmlLink:

    def test_rendering_constructor_with_only_content(self):
        div = HtmlDiv()
        link = div.link("my_link")
        assert str(link).replace("\n", "") == '<a href="my_link" target="_blank">my_link</a>'

    def test_rendering_constructor_with_content_and_href(self):
        div = HtmlDiv()
        link = div.link("my_link", href="destination")
        assert str(link).replace("\n", "") == '<a href="destination" target="_blank">my_link</a>'
