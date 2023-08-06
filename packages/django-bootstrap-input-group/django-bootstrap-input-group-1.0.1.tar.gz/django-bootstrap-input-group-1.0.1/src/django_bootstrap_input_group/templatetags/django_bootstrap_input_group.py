from django import template

register = template.Library()


@register.simple_tag
def bootstrap_grouped_form(form, **kwargs):
    """
    Render a form that groups some of its fields into input groups.

    Groups are declared through a `field_groups` attribute on the form.
    """

    from django_bootstrap_input_group.renderers import GroupedFormRenderer
    return GroupedFormRenderer(form, **kwargs).render()


@register.simple_tag
def bootstrap_grouped_formset(formset, **kwargs):
    """Render a formset of a form that groups some of its fields into input groups."""

    from django_bootstrap_input_group.renderers import GroupedFormsetRenderer
    return GroupedFormsetRenderer(formset, **kwargs).render()


@register.simple_tag
def bootstrap_input_group(*fields, **kwargs):
    """
    Render a number of bound form fields as an input group.

    Example:
        {% bootstrap_input_group form.field_1 form.field_2 label="label" %}
    """

    from django_bootstrap_input_group.renderers import InputGroupRenderer
    return InputGroupRenderer(fields, **kwargs).render()
