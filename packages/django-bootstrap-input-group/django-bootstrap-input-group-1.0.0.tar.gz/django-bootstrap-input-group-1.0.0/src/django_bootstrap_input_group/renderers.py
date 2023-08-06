from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django_bootstrap5 import core
from django_bootstrap5.css import merge_css_classes
from django_bootstrap5.forms import render_field, render_label
from django_bootstrap5.text import text_value

BaseFormRenderer = core.get_form_renderer()
BaseFormsetRenderer = core.get_formset_renderer()
BaseFieldRenderer = core.get_field_renderer()


class GroupedFormRenderer(BaseFormRenderer):
    """
    Render a form that groups some of its fields into input groups.

    Groups are declared through the form attribute `field_groups`.
    `field_groups` contains the names of form fields in the order that they
    should be rendered in, with nested lists (or tuples) of names representing
    a group.
    The nested list can be either a flat list, or a two-item list, where the
    first item is the label for the group and the second is the list of field
    names.

    Example:

        class Form(forms.Form):
            first_name = forms.CharField()
            second_name = forms.CharField()
            tel = forms.CharField()
            address = forms.CharField()

            field_groups = [
                ('Name', ['first_name', 'second_name']),
                'tel',
                'address',
            ]

        The fields `first_name` and `second_name` will be rendered together as
        an input group with the label 'Name'. The other fields are rendered as
        usual.
    """

    @property
    def groups(self):
        if hasattr(self, '_groups'):
            return self._groups

        groups = []
        for group in getattr(self.form, 'field_groups', ()):
            if not isinstance(group, (str, list, tuple)):
                raise TypeError(
                    f"Invalid group item {group}. "
                    "Group items must be strings or lists or tuples."
                )
            group_label = ""
            if isinstance(group, str):
                field_names = [group]
            elif len(group) == 2 and isinstance(group[1], (list, tuple)):
                group_label = group[0]
                field_names = group[1]
            else:
                field_names = group
            group_fields = [self.form[field_name] for field_name in field_names]
            if not group_label:
                group_label = group_fields[0].label
            groups.append((group_label, group_fields))
        self._groups = groups
        return self._groups

    def render_fields(self):
        if not self.groups or all(len(fields) == 1 for _label, fields in self.groups):
            # Nothing to group - use the default renderer.
            return super().render_fields()

        rendered_fields = mark_safe("")
        kwargs = self.get_kwargs()
        for label, fields in self.groups:
            if len(fields) == 1:
                rendered_fields += render_field(fields[0], **kwargs)
            else:
                rendered_fields += InputGroupRenderer(fields, label=label, **kwargs).render()
        return rendered_fields


class GroupedFormsetRenderer(BaseFormsetRenderer):
    """Render a formset of a form that groups some of its fields into input groups."""

    def render_forms(self):
        rendered_forms = mark_safe("")
        kwargs = self.get_kwargs()
        for form in self.formset.forms:
            rendered_forms += GroupedFormRenderer(form, **kwargs).render()
        return rendered_forms


class InputGroupRenderer(BaseFieldRenderer):
    """Render the widgets of a list of fields as an input group."""

    def __init__(self, fields, label="", **kwargs):
        self.fields = fields
        self.label = label
        super(BaseFieldRenderer, self).__init__(**kwargs)

    def render(self):
        return format_html(
            '<div class="{wrapper_classes}">{group_label}{group}</div>',
            wrapper_classes=self.get_wrapper_classes(),
            group_label=self.get_group_label(),
            group=self.get_group_html(),
        )

    def get_group_label_class(self, horizontal=False):
        """Return CSS clas for the group label."""
        label_classes = [text_value(self.label_class)]
        if not self.show_label:
            label_classes.append("visually-hidden")
        else:
            if self.is_inline:
                widget_label_class = "visually-hidden"
            elif horizontal:
                widget_label_class = merge_css_classes(self.horizontal_label_class, "col-form-label")
            else:
                widget_label_class = "form-label"
            label_classes = [widget_label_class] + label_classes
        return merge_css_classes(*label_classes)

    def get_group_label(self):
        """
        Provide a label for an input group.

        If no label was provided, use the label of the field of the group.
        Return an empty string if set to floating layout or if set to skip the
        labels.
        """
        if self.is_floating or self.show_label == "skip":
            # Do not provide a label for the group.
            # (for floating layouts, the fields in the group will provide their own floating label)
            return mark_safe("")
        elif self.label:
            return render_label(
                self.label,
                label_class=self.get_group_label_class(horizontal=self.is_horizontal),
            )
        else:
            # Use the label of the first field in the group as the group label:
            renderer = BaseFieldRenderer(self.fields[0], **self.get_kwargs())
            return renderer.get_label_html(horizontal=self.is_horizontal)

    def get_group_html(self):
        """Render multiple fields as an input-group."""
        fields = mark_safe("")
        for field in self.fields:
            fields += self.get_group_field_html(field)

        group_classes = "input-group"  # TODO: get input group CSS class from settings?
        if self.is_floating:
            group_classes = "input-group form-floating"
        if self.is_horizontal:
            return format_html(
                '<div class="{horizontal_class}">'
                '<div class="{group_classes}">{fields}</div>'
                '</div>',
                horizontal_class=self.horizontal_field_class,
                group_classes=group_classes,
                fields=fields
            )
        else:
            return format_html(
                '<div class="{group_classes}">{fields}</div>',
                group_classes=group_classes,
                fields=fields,
            )

    def get_group_field_html(self, field):
        """Render a field for an input-group."""
        renderer = BaseFieldRenderer(field, **self.get_kwargs())

        if self.is_floating and self.can_widget_float(field.field.widget):
            wrapper_classes = "form-floating"
            return format_html(
                '<div class="{wrapper_classes}">{field}{label}</div>',
                wrapper_classes=wrapper_classes,
                field=renderer.get_field_html(),
                label=renderer.get_label_html(),
            )
        else:
            return renderer.get_field_html()

    @property
    def is_floating(self):
        """Return whether to render `form-control` widgets as floating."""
        return super(BaseFieldRenderer, self).is_floating

    def get_wrapper_classes(self):
        renderer = BaseFieldRenderer(self.fields[0], **self.get_kwargs())
        return renderer.get_wrapper_classes()
