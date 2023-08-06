from django import forms

from django_bootstrap_input_group.renderers import GroupedFormsetRenderer
from .case import BootstrapTestCase


class TestForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")

    field_groups = [('Name', ['first_name', 'last_name'])]


class TestGroupedFormsetRenderer(BootstrapTestCase):

    def test_render(self):
        self.assertHTMLEqual(
            # Management form:
            '<input type="hidden" name="form-TOTAL_FORMS" value="1" id="id_form-TOTAL_FORMS">'
            '<input type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS">'
            '<input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS">'
            '<input type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS">'
            # Formset form 1:
            '<div class="test-wrapper-class">'
            '<label class="form-label">Name</label>'
            '<div class="input-group">'
            '<input type="text" name="form-0-first_name" class="form-control" placeholder="First Name" id="id_form-0-first_name">'
            '<input type="text" name="form-0-last_name" class="form-control" placeholder="Last Name" id="id_form-0-last_name">'
            '</div>'
            '</div>',
            self.render('{% bootstrap_grouped_formset formset %}', {'formset': forms.formset_factory(TestForm)()})
        )

    def test_render_forms(self):
        formset = forms.formset_factory(TestForm, extra=2)
        renderer = GroupedFormsetRenderer(formset())
        self.assertHTMLEqual(
            # Formset form 1:
            '<div class="test-wrapper-class">'
            '<label class="form-label">Name</label>'
            '<div class="input-group">'
            '<input type="text" name="form-0-first_name" class="form-control" placeholder="First Name" id="id_form-0-first_name">'
            '<input type="text" name="form-0-last_name" class="form-control" placeholder="Last Name" id="id_form-0-last_name">'
            '</div>'
            '</div>'
            # Formset form 2:
            '<div class="test-wrapper-class">'
            '<label class="form-label">Name</label>'
            '<div class="input-group">'
            '<input type="text" name="form-1-first_name" class="form-control" placeholder="First Name" id="id_form-1-first_name">'
            '<input type="text" name="form-1-last_name" class="form-control" placeholder="Last Name" id="id_form-1-last_name">'
            '</div>'
            '</div>',
            renderer.render_forms()
        )
