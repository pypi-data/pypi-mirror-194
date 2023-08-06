from pyspass import HtmlDiv


class TestHtmlLabel:

    def test_rendering_with_forid(self):
        div = HtmlDiv()
        div.label(content="test", for_id="input_id")
        assert '<label for="input_id">test</label>' in str(div).replace("\n", "")
