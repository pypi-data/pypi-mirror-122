# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Typography(Component):
    """A Typography component.
Material-UI Typography.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- align (a value equal to: "inherit", "left", "right", "center", "justify"; optional):
    Set the text-align on the component.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- component (string; optional):
    The component used for the root node.

- gutterBottom (boolean; optional):
    If `True`, the text will have a bottom margin.

- noWrap (boolean; optional):
    If `True`, the text will not wrap, but instead will truncate with
    a text overflow ellipsis.  Note that text overflow can only happen
    with block or inline-block level elements (the element needs to
    have a width in order to overflow).

- paragraph (boolean; optional):
    If `True`, the element will be a paragraph element.

- style (dict; optional)

- variant (a value equal to: "button", "caption", "h1", "h2", "h3", "h4", "h5", "h6", "inherit", "subtitle1", "subtitle2", "body1", "body2", "overline"; optional):
    Applies the theme typography styles."""
    @_explicitize_args
    def __init__(self, children=None, align=Component.UNDEFINED, gutterBottom=Component.UNDEFINED, noWrap=Component.UNDEFINED, paragraph=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, component=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'align', 'className', 'classes', 'component', 'gutterBottom', 'noWrap', 'paragraph', 'style', 'variant']
        self._type = 'Typography'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'align', 'className', 'classes', 'component', 'gutterBottom', 'noWrap', 'paragraph', 'style', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Typography, self).__init__(children=children, **args)
