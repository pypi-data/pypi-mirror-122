# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class List(Component):
    """A List component.
Material-UI List.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- dense (boolean; optional):
    If `True`, compact vertical padding designed for keyboard and
    mouse input is used for the list and list items. The prop is
    available to descendant components as the `dense` context.

- disablePadding (boolean; optional):
    If `True`, vertical padding is removed from the list.

- style (dict; optional)

- subheader (boolean | number | string | dict | list; optional):
    The content of the subheader, normally `ListSubheader`."""
    @_explicitize_args
    def __init__(self, children=None, dense=Component.UNDEFINED, disablePadding=Component.UNDEFINED, subheader=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'classes', 'dense', 'disablePadding', 'style', 'subheader']
        self._type = 'List'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'classes', 'dense', 'disablePadding', 'style', 'subheader']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(List, self).__init__(children=children, **args)
