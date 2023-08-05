# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Paper(Component):
    """A Paper component.
Material-UI Paper.

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

- elevation (number; optional):
    Shadow depth, corresponds to `dp` in the spec. It accepts values
    between 0 and 24 inclusive.

- square (boolean; optional):
    If `True`, rounded corners are disabled.

- style (dict; optional)

- variant (a value equal to: "elevation", "outlined"; optional):
    The variant to use."""
    @_explicitize_args
    def __init__(self, children=None, elevation=Component.UNDEFINED, square=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'classes', 'elevation', 'square', 'style', 'variant']
        self._type = 'Paper'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'classes', 'elevation', 'square', 'style', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Paper, self).__init__(children=children, **args)
