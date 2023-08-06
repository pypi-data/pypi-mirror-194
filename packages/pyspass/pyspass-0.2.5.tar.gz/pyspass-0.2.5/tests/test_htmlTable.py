from pyspass import HtmlTable, HtmlRow, Iterator


class TestHtmlTable:

    def test_table_constructor(self):
        tab = HtmlTable()
        assert "table" in str(tab)

    def test_table_assembly(self):
        tab = HtmlTable()
        assert "table" in str(tab)
        assert tab.header is None

        tab.tr()
        assert isinstance(tab.header, HtmlRow)
        assert isinstance(tab.rows, Iterator)
