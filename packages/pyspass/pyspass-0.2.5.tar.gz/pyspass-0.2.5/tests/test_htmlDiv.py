from pyspass import HtmlDiv


class TestHtmlDiv:

    def test_constructor_with_id(self):
        id_name = "my_id"
        div = HtmlDiv(id_html=id_name)
        assert div.id_html == id_name
        assert 'id' in div.tag_content
        assert div.tag_content['id'] == id_name
