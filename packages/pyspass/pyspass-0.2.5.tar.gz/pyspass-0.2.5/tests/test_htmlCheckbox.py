from pyspass import HtmlDiv


class TestHtmlCheckbox:

    def test_checkbox_without_minimum_params(self):
        div = HtmlDiv()
        div.checkbox(name="check_test", value=1, label='label')
        assert '<input type="checkbox" name="check_test" value="1"/>' in str(div)
