from django import forms

from django_bootstrap_input_group.renderers import InputGroupRenderer
from .case import BootstrapTestCase


class TestForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")

    nofloat = forms.ChoiceField(
        choices=[('foo', 'Foo'), ('bar', 'Bar')],
        widget=forms.RadioSelect
    )

    field_groups = [('Name', ['first_name', 'last_name'])]


class TestInputGroupRenderer(BootstrapTestCase):

    def setUp(self):
        self.form = TestForm()

    def get_renderer(self, fields=None, **kwargs):
        if fields is None:
            fields = [self.form['first_name'], self.form['last_name']]
        label = kwargs.pop('label', 'Name')
        return InputGroupRenderer(fields, label, **kwargs)

    def test_render(self):
        self.assertHTMLEqual(
            '<div class="test-wrapper-class">'
            '<label class="form-label">Name</label>'
            '<div class="input-group">'
            '<input type="text" name="first_name" class="form-control" placeholder="First Name" required id="id_first_name">'
            '<input type="text" name="last_name" class="form-control" placeholder="Last Name" required id="id_last_name">'
            '</div>'
            '</div>',
            self.render('{% bootstrap_input_group form.first_name form.last_name label="Name" %}', {'form': TestForm()})
        )

    def test_group_html(self):
        self.assertHTMLEqual(
            '<div class="input-group">'
            '<input type="text" name="first_name" class="form-control" placeholder="First Name" required id="id_first_name">'
            '<input type="text" name="last_name" class="form-control" placeholder="Last Name" required id="id_last_name">'
            '</div>',
            self.get_renderer().get_group_html()
        )

    def test_group_html_floating(self):
        self.maxDiff = None
        self.assertHTMLEqual(
            '<div class="input-group form-floating">'
            '<div class="form-floating">'
            '<input type="text" name="first_name" class="form-control" placeholder="First Name" required id="id_first_name">'
            '<label class="form-label" for="id_first_name">First Name</label>'
            '</div>'
            '<div class="form-floating">'
            '<input type="text" name="last_name" class="form-control" placeholder="Last Name" required id="id_last_name">'
            '<label class="form-label" for="id_last_name">Last Name</label>'
            '</div>'
            '</div>',
            self.get_renderer(layout="floating").get_group_html()
        )

    def test_group_html_horizontal(self):
        self.assertHTMLEqual(
            '<div class="test-horizontal-field">'
            '<div class="input-group">'
            '<input type="text" name="first_name" class="form-control" placeholder="First Name" required id="id_first_name">'
            '<input type="text" name="last_name" class="form-control" placeholder="Last Name" required id="id_last_name">'
            '</div>'
            '</div>',
            self.get_renderer(layout="horizontal").get_group_html()
        )

    def test_get_group_field_html(self):
        field = self.form['first_name']
        self.assertHTMLEqual(
            '<input type="text" name="first_name" class="form-control" placeholder="First Name" required id="id_first_name">',
            self.get_renderer().get_group_field_html(field)
        )

    def test_get_group_field_html_floating(self):
        field = self.form['first_name']
        self.assertHTMLEqual(
            '<div class="form-floating">'
            '<input type="text" name="first_name" class="form-control" placeholder="First Name" required id="id_first_name">'
            '<label class="form-label" for="id_first_name">First Name</label>'
            '</div>',
            self.get_renderer(layout="floating").get_group_field_html(field)
        )

    def test_get_group_field_html_floating_widget_cannot_float(self):
        """Assert that the field does not get wrapped with .form-floating class if the widget cannot float."""
        field = self.form['nofloat']
        self.assertNotIn("form-floating", self.get_renderer(layout="floating").get_group_field_html(field))

    def test_group_label_default_layout(self):
        self.assertInHTML(
            '<label class="form-label">Name</label>',
            self.render('{% bootstrap_grouped_form form layout="default" show_label=True %}', {"form": TestForm()})
        )

    def test_group_label_horizontal_layout(self):
        self.assertInHTML(
            '<label class="test-horizontal-label col-form-label">Name</label>',
            self.render('{% bootstrap_grouped_form form layout="horizontal" show_label=True %}', {"form": TestForm()})
        )

    def test_group_label_floating_layout(self):
        """No group label should be added in floating layouts."""
        for show_label in (True, False, "skip"):
            with self.subTest(show_label=show_label):
                self.assertNotIn(
                    '>Name</label>',  # unique to the group label
                    self.render(
                        f'{{% bootstrap_grouped_form form show_label={show_label} layout="floating" %}}',
                        {"form": TestForm()}
                    )
                )

    def test_group_label_inline_layout(self):
        self.assertInHTML(
            '<label class="visually-hidden">Name</label>',
            self.render('{% bootstrap_grouped_form form layout="inline" show_label=True %}', {"form": TestForm()})
        )

    def test_group_label_show_label_false(self):
        for show_label in (False, "''"):
            for layout in ("default", "horizontal", "inline"):
                with self.subTest(layout=layout, show_label=show_label):
                    self.assertInHTML(
                        '<label class="visually-hidden">Name</label>',
                        self.render(
                            f'{{% bootstrap_grouped_form form show_label={show_label} layout="{layout}" %}}',
                            {"form": TestForm()}
                        )
                    )

    def test_group_label_show_label_skip(self):
        for layout in ("default", "horizontal", "inline"):
            with self.subTest(layout=layout):
                self.assertNotIn(
                    ">Name</label>",
                    self.render(
                        f'{{% bootstrap_grouped_form form show_label="skip" layout="{layout}" %}}',
                        {"form": TestForm()}
                    )
                )

    def test_group_label_no_group_label(self):
        for label in (None, ""):
            with self.subTest(label=label):
                self.assertIn('>First Name</label>', self.get_renderer(label=label).get_group_label())
