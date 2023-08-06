from pyspass import HtmlRow, HtmlCell


class TestHtmlLabel:

    def test_rendering_cell_without_content(self):
        row = HtmlRow()
        cell = row.td()
        assert isinstance(cell, HtmlCell)
        assert str(cell).startswith("<td>")
        assert str(cell).strip().endswith("</td>")

    def test_rendering_headcell_without_content(self):
        row = HtmlRow()
        cell = row.th()
        assert isinstance(cell, HtmlCell)
        assert str(cell).startswith("<th>")
        assert str(cell).strip().endswith("</th>")

    def test_rendering_headcell_with_list_content(self):
        row = HtmlRow()
        cells = row.th(['A', 'B'])
        cell = cells[0]
        assert isinstance(cell, HtmlCell)
        assert str(cell).startswith("<th>")
        assert str(cell).strip().endswith("</th>")
