# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FormControlUnstyled(Component):
    """A FormControlUnstyled component.
Material-UI FormControlUnstyled.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional):
    Class name applied to the root element.

- defaultValue (boolean | number | string | dict | list; optional)

- disabled (boolean; optional):
    If `True`, the label, input and helper text should be displayed in
    a disabled state.

- error (boolean; optional):
    If `True`, the label is displayed in an error state.

- focused (boolean; optional):
    If `True`, the component is displayed in focused state.

- required (boolean; optional):
    If `True`, the label will indicate that the `input` is required.

- value (boolean | number | string | dict | list; optional)"""
    @_explicitize_args
    def __init__(self, children=None, className=Component.UNDEFINED, defaultValue=Component.UNDEFINED, disabled=Component.UNDEFINED, error=Component.UNDEFINED, focused=Component.UNDEFINED, required=Component.UNDEFINED, value=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'defaultValue', 'disabled', 'error', 'focused', 'required', 'value']
        self._type = 'FormControlUnstyled'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'defaultValue', 'disabled', 'error', 'focused', 'required', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FormControlUnstyled, self).__init__(children=children, **args)
