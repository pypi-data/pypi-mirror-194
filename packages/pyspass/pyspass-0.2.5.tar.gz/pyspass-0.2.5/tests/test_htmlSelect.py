from pyspass import HtmlDiv


class TestHtmlSelect:

    def test_dropdown_with_content_as_dict(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', {'A': 'Code A', 'B': 'Code B'})
        assert '<option value="A">Code A</option>' in str(drop)
        assert '<option value="B">Code B</option>' in str(drop)

    def test_dropdown_with_content_as_list(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B'])
        assert '<option value="A">A</option>' in str(drop)
        assert '<option value="B">B</option>' in str(drop)

    def test_dropdown_with_content_as_list_and_input_asaw_str(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input='B')
        assert '<option value="B" selected="selected">B</option>' in str(drop)

    def test_dropdown_with_content_as_list_and_input_as_list_of_str(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input=['B'])
        assert '<option value="B" selected="selected">B</option>' in str(drop)

    def test_dropdown_with_content_as_list_and_input_as_list_of_dicttype(self):
        div = HtmlDiv()
        request_dict = {'abc': 'B', 'def': 'A'}
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input=request_dict)
        assert '<option value="B" selected="selected">B</option>' in str(drop)

    def test_dropdown_with_content_as_list_and_input_as_list_of_multiple_str_with_option_false(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input=['B', 'C'], multiple=False)
        assert '<option value="B" selected="selected">B</option>' in str(drop)
        assert '<option value="C" selected="selected">C</option>' in str(drop)

    def test_dropdown_with_content_as_list_and_input_as_list_of_multiple_str_with_option_true(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input=['B', 'C'], multiple=True)
        assert '<option value="B" selected="selected">B</option>' in str(drop)
        assert '<option value="C" selected="selected">C</option>' in str(drop)

    def test_dropdown_with_content_as_dict_and_optgroup(self):
        div = HtmlDiv()
        optgroups = {'AB': ['A', 'B'], 'CD': ['C', 'D']}
        drop = div.dropdown('abc', {'A': 'Code A', 'B': 'Code B', 'C': 'Code C', 'D': 'Code D'}, optgroups=optgroups)
        assert '<option value="A">Code A</option>' in str(drop)
        assert '<option value="B">Code B</option>' in str(drop)
        assert '<option value="C">Code C</option>' in str(drop)
        assert '<option value="D">Code D</option>' in str(drop)
