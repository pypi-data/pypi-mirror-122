# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Stack(Component):
    """A Stack component.
Material-UI Stack.

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

- direction (a value equal to: "row", "row-reverse", "column", "column-reverse"; optional):
    Defines the `flex-direction` style property. It is applied for all
    screen sizes.

- divider (boolean | number | string | dict | list; optional):
    Add an element between each child.

- spacing (number; optional):
    Defines the space between immediate children.

- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, divider=Component.UNDEFINED, className=Component.UNDEFINED, spacing=Component.UNDEFINED, direction=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'classes', 'direction', 'divider', 'spacing', 'style']
        self._type = 'Stack'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'classes', 'direction', 'divider', 'spacing', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Stack, self).__init__(children=children, **args)
