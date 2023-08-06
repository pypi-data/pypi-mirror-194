import pytest

from pyspass import ResultListing


@pytest.fixture(scope="session")
def content_as_dicts():
    return [{'column_1': 1, 'column_2': 2}]


class TestResultListing:

    def test_resultListing(self, content_as_dicts):
        rl = ResultListing(content_as_dicts)
        assert rl  # no error

    def test_result_listing_dict_no_mapping(self, content_as_dicts):
        rl = ResultListing(content_as_dicts)
        assert rl  # no error

    def test_result_listing_dict_exact_list_mapping(self, content_as_dicts):
        mapping = ['column_1', 'column_2']
        rl = ResultListing(content_as_dicts, mapping=mapping, show_all=False)
        assert rl._derive_columnnames_for_display() == mapping

    def test_result_listing_dict_pruned_list_mapping(self, content_as_dicts):
        mapping = ['column_1']
        rl = ResultListing(content_as_dicts, mapping=mapping, show_all=False)
        assert rl._derive_columnnames_for_display() == mapping

    def test_result_listing_dict_pruned_list_mapping_showall(self, content_as_dicts):
        mapping = ['column_2']
        rl = ResultListing(content_as_dicts, mapping=mapping, show_all=True)
        assert sorted(rl._derive_columnnames_for_display()) == ['column_1', 'column_2']
        # no error

    def test_result_listing_dict_overlapping_list_mapping(self, content_as_dicts):
        mapping = ['column_1', 'column_2', 'column3']
        rl = ResultListing(content_as_dicts, mapping=mapping, show_all=False)
        assert rl._derive_columnnames_for_display() == ['column_1', 'column_2']

    def test_result_listing_dict_differing_list_mapping(self):
        content = [{'column_1': 1, 'column_2': 2}]
        rl = ResultListing(content, mapping=['XYZ', 'ABC'])
        assert rl  # no error

    def test_column_alignment(self):
        content = [{'column_1': 1, 'column_2': 2, 'column_3': 3}]
        r1 = ResultListing(content, alignments="lrc")
        assert "right" in str(r1)
        assert "center" in str(r1)
        assert "left" in str(r1)
