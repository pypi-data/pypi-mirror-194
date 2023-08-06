import pytest

from pyspass import HtmlForm
from pyspass import ResultEditor


@pytest.fixture(scope="session")
def content_as_dicts():
    return [{'column_id': 1,
             'column_2': 2,
             'column_3': 'A'},
            {'column_id': 2,
             'column_2': 4,
             'column_3': 'B'},
            {'column_id': 3,
             'column_2': 6,
             'column_3': 'C'}]


class TestResultEditor:

    def test_resultEditor(self, content_as_dicts):
        form = HtmlForm(id_html='form_id')
        re = ResultEditor(content=content_as_dicts, listing_index='column_id', row_selected='2')
        form.add(re)
        re.compose()

    def test_resultEditor_show_all(self, content_as_dicts):
        form = HtmlForm(id_html='form_id')
        re = ResultEditor(content=content_as_dicts, listing_index='column_id', row_selected='2', show_all=True)
        form.add(re)
        re.compose()
