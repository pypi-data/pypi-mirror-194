import pytest

from pyspass import HtmlForm, HtmlDiv


class TestHtmlForm:

    def test_get_form_with_no_parent(self):
        div = HtmlDiv()
        assert div.get_form() is None

    def test_get_form_with_no_parent_form(self):
        div_outer = HtmlDiv('outer_div')
        div = div_outer.div()
        assert div.get_form() is None

    def test_error_on_nested_forms_for_nonform(self):
        form_outer = HtmlForm('outer_form')
        div = form_outer.div()
        form_inner = div.form('inner_form')
        div_sub = form_inner.div()
        with pytest.raises(Exception):
            div_sub.get_form()

    def test_error_on_nested_forms_for_form(self):
        form_outer = HtmlForm('outer_form')
        div = form_outer.div()
        form_inner = div.form('inner_form')
        with pytest.raises(Exception):
            form_inner.get_form()
