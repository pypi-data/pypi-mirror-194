import pytest

from pyspass import HtmlForm, HtmlDiv
from pyspass import ResultChoice


@pytest.fixture(scope="session")
def content_as_dicts():
    return [{'column_1': 1, 'column_2': 2, 'column_3': 3},
            {'column_1': 4, 'column_2': 5, 'column_3': 6},
            {'column_1': 7, 'column_2': 8, 'column_3': 9},
            {'column_1': 10, 'column_2': 11, 'column_3': 12},
            {'column_1': 13, 'column_2': None, 'column_3': 15},
            {'column_1': 16, 'column_2': 17, 'column_3': 18}]


class TestResultChoice:

    def test_constructor(self, content_as_dicts):
        # just test if it creates an object
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=content_as_dicts, listing_index='column_1', row_selected=None)
        rl.compose()
        assert len(rl.table_) == len(content_as_dicts) + 1  # +1 for header

    def test_constructor_without_valid_parentform(self, content_as_dicts):
        # if no form with an unique id is present, an error has to be raised
        div = HtmlDiv()
        rl = div.result_choice(content=content_as_dicts, listing_index='column_1', row_selected=None)
        with pytest.raises(Exception):
            rl.compose()

    def test_setter_listing_index(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=content_as_dicts, listing_index='column_1', row_selected=None)
        assert rl.listing_index == ['column_1', ]

    def test_constructor_empty_content(self):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=None, listing_index='column_1', row_selected=None)
        rl.compose()

    def test_multiple_index(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=content_as_dicts, listing_index=['column_1', 'column_2'],
                                     row_selected={})
        rl.compose()
        # todo elaborate

    def test_row_selection(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=content_as_dicts, listing_index='column_1',
                                     row_selected={'column_1': 4})
        rl.compose()
        assert 'name="_rct_selected_column_1" value="4"' in str(rl)

        # Do it again with a string input
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=content_as_dicts, listing_index='column_1',
                                     row_selected={'column_1': '4'})
        rl.compose()
        assert 'name="_rct_selected_column_1" value="4"' in str(rl)

    def test_row_selection_with_multible_columns(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=content_as_dicts, listing_index=['column_1', 'column_2'],
                                     row_selected={'column_1': 4, 'column_2': 5})
        rl.compose()
        assert 'name="_rct_selected_column_1" value="4"' in str(rl)
        assert 'name="_rct_selected_column_2" value="5"' in str(rl)

    def test_indirect_format_id(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        html_div = html_form.div()
        rc = html_div.result_choice(content=content_as_dicts, listing_index='column_1', row_selected=None)
        assert rc.get_form().id_html == "form_id"

    def test_set_codes_constructor_with_dict(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        rl: ResultChoice = html_form.result_choice(content=content_as_dicts, listing_index='column_1',
                                                   row_selected=None)
        rl.set_codes("column_1", {1: "a", 2: "c"})
        rl.compose()

    def test_set_codes_constructor_with_list(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        rl: ResultChoice = html_form.result_choice(content=content_as_dicts, listing_index='column_1',
                                                   row_selected=None)
        rl.set_codes("column_1", [1, 2])
        rl.compose()

    def test_set_codes_constructor_with_dict_and_missing_list_index(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        rl: ResultChoice = html_form.result_choice(content=content_as_dicts, listing_index='not_there',
                                                   row_selected=None)
        with pytest.raises(Exception):
            rl.set_codes("column_1", {1: "a", 2: "c"})
            rl.compose()

    def test_select_multiple_rows_at_once(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        rl: ResultChoice = html_form.result_choice(content=content_as_dicts,
                                                   listing_index='column_1',
                                                   row_selected=[{'column_1': '4'},
                                                                 {'column_1': '10'}])
        rl.compose()
        assert 'white' in str(rl)
        assert 'name="_rct_selected_column_1" value="4;10"' in str(rl)

    def test__is_selected_row(self, content_as_dicts):
        html_form = HtmlForm(id_html='form_id')
        rl: ResultChoice = html_form.result_choice(content=content_as_dicts,
                                                   listing_index='column_1',
                                                   row_selected=[{'column_1': '4'},
                                                                 {'column_1': '10'}])
        rl.compose()

        assert rl._is_selected_row({'column_1': '4'})
        assert rl._is_selected_row({'column_1': '10'})
        assert not rl._is_selected_row({'column_1': '5'})
        assert not rl._is_selected_row({'column_2': '4'})
        assert not rl._is_selected_row({'column_2': '5'})

        # test with list as input
        rl: ResultChoice = html_form.result_choice(content=content_as_dicts,
                                                   listing_index=['column_1'],
                                                   row_selected=[{'column_1': '4'},
                                                                 {'column_1': '10'}])
        rl.compose()
        assert rl._is_selected_row({'column_1': '4'})
        assert not rl._is_selected_row({'column_1': '5'})

        # test with multiple columns
        rl: ResultChoice = html_form.result_choice(content=content_as_dicts,
                                                   listing_index=['column_1', 'column_2'],
                                                   row_selected=[{'column_1': '4', 'column_2': '5'},
                                                                 {'column_1': '6', 'column_2': '7'}])
        rl.compose()
        assert rl._is_selected_row({'column_1': 4, 'column_2': 5})
        assert rl._is_selected_row({'column_1': 6, 'column_2': 7})
        assert not rl._is_selected_row({'column_1': 2, 'column_2': 3})
        assert not rl._is_selected_row({'column_1': 4, 'column_2': 3})
        assert not rl._is_selected_row({'column_1': 1, 'column_2': 7})

    def test_with_alchemy(self):
        from sqlalchemy import Table, MetaData, Column, Integer, String, select
        from sqlalchemy import create_engine
        con = create_engine('sqlite://').connect()
        meta = MetaData()
        tab = Table("test_table", meta,
                    Column("column_a", Integer),
                    Column("column_b", String))
        meta.create_all(con)
        con.execute(tab.insert().values((1, "a")))
        result = con.execute(select(tab.c.column_b)).mappings().fetchall()

        html_form = HtmlForm(id_html='form_id')
        rc: ResultChoice = html_form.result_choice(content=result, listing_index='not_there')
        assert "column_b" in str(rc)
