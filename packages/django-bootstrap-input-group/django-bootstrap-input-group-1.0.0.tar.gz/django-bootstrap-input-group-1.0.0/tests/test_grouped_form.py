from django import forms

from django_bootstrap_input_group.renderers import GroupedFormRenderer
from .case import BootstrapTestCase


class TestForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    tel = forms.CharField(label="Phone")

    field_groups = [('Name', ['first_name', 'last_name']), 'tel']


class NoFieldGroupsForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    tel = forms.CharField(label="Phone")


class TestGroupedFormRenderer(BootstrapTestCase):

    def test_render(self):
        self.assertHTMLEqual(
            '<div class="test-wrapper-class">'
            '<label class="form-label">Name</label>'
            '<div class="input-group">'
            '<input type="text" name="first_name" class="form-control" placeholder="First Name" required id="id_first_name">'
            '<input type="text" name="last_name" class="form-control" placeholder="Last Name" required id="id_last_name">'
            '</div>'
            '</div>'
            '<div class="test-wrapper-class">'
            '<label class="form-label" for="id_tel">Phone</label>'
            '<input type="text" name="tel" class="form-control" placeholder="Phone" required id="id_tel">'
            '</div>',
            self.render('{% bootstrap_grouped_form form %}', {'form': TestForm()})
        )

    def test_groups_no_groups(self):
        """Single item groups are expected if `field_groups` only contains strings and no groups."""
        form = TestForm()
        form.field_groups = ['first_name', 'last_name', 'tel']
        renderer = GroupedFormRenderer(form)
        expected_groups = [
            ('First Name', [form['first_name']]),
            ('Last Name', [form['last_name']]),
            ('Phone', [form['tel']]),
        ]
        self.assertEqual(renderer.groups, expected_groups)

    def test_groups_mixed(self):
        """Test groups when `field_groups` is a mixture of flat lists and strings, and Nested lists and strings."""
        form = TestForm()
        for groups, group_label in (
                # <----------- groups -----------> expected label
                ([['first_name', 'last_name'], 'tel'], 'First Name'),
                ([('Name', ['first_name', 'last_name']), 'tel'], 'Name'),
        ):
            with self.subTest(field_groups=groups):
                form.field_groups = groups
                renderer = GroupedFormRenderer(form)
                self.assertEqual(
                    [(group_label, [form['first_name'], form['last_name']]), ('Phone', [form['tel']])],
                    renderer.groups,
                )

    def test_groups_flat_list(self):
        """For flat group lists, the group label should be the label of the first group field."""
        form = TestForm()
        form.field_groups = [('first_name', 'last_name')]
        renderer = GroupedFormRenderer(form)
        self.assertEqual(renderer.groups, [('First Name', [form['first_name'], form['last_name']])])

    def test_groups_two_tuple(self):
        form = TestForm()
        form.field_groups = [('Name', ['first_name', 'last_name'])]
        renderer = GroupedFormRenderer(form)
        self.assertEqual(renderer.groups, [('Name', [form['first_name'], form['last_name']])])

    def test_groups_no_label(self):
        form = TestForm()
        field_groups = [
            [('', ['first_name', 'last_name'])],
            [(None, ['first_name', 'last_name'])],
            [('first_name', 'last_name')]
        ]
        for group in field_groups:
            with self.subTest(field_groups=group):
                form.field_groups = group
                renderer = GroupedFormRenderer(form)
                self.assertEqual(renderer.groups, [('First Name', [form['first_name'], form['last_name']])])

    def test_groups_no_field_groups_attribute(self):
        """Groups should be an empty list if the form declares no `field_groups` attribute."""
        form = NoFieldGroupsForm()
        renderer = GroupedFormRenderer(form)
        self.assertEqual(renderer.groups, [])

    def test_groups_no_field_groups_empty(self):
        """Groups should be an empty list if `field_groups` is empty."""
        form = TestForm()
        form.field_groups = []
        renderer = GroupedFormRenderer(form)
        self.assertEqual(renderer.groups, [])

    def test_groups_invalid(self):
        """Group declarations must be either string or lists or tuples."""
        form = TestForm()
        for invalid_group in ([('first_name', 'last_name'), 2], [('first_name', 'last_name'), {}]):
            with self.subTest(invalid_group=invalid_group):
                form.field_groups = invalid_group
                renderer = GroupedFormRenderer(form)
                with self.assertRaises(TypeError):
                    renderer.groups

    def test_render_fields(self):
        form = TestForm()
        renderer = GroupedFormRenderer(form)
        rendered_fields = renderer.render_fields()

        # 'Name' field group:
        self.assertInHTML(
            '<div class="test-wrapper-class">'
            '<label class="form-label">Name</label>'
            '<div class="input-group">'
            '<input type="text" name="first_name" class="form-control" placeholder="First Name" required id="id_first_name">'
            '<input type="text" name="last_name" class="form-control" placeholder="Last Name" required id="id_last_name">'
            '</div>'
            '</div>',
            rendered_fields
        )
        # Phone field:
        self.assertInHTML(
            '<div class="test-wrapper-class">'
            '<label class="form-label" for="id_tel">Phone</label>'
            '<input type="text" name="tel" class="form-control" placeholder="Phone" required id="id_tel">'
            '</div>',
            rendered_fields
        )

    def test_render_fields_no_groups(self):
        form = TestForm()
        renderer = GroupedFormRenderer(form)
        for field_groups in ([], ['first_name', 'last_name', 'tel']):
            with self.subTest(field_groups=field_groups):
                form.field_groups = field_groups
                self.assertNotIn('input-group', renderer.render_fields())
