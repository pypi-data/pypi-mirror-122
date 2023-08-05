# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SwitchUnstyled(Component):
    """A SwitchUnstyled component.
Material-UI SwitchUnstyled.

Keyword arguments:

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- checked (boolean; optional):
    If `True`, the component is checked.

- className (string; optional):
    Class name applied to the root element.

- defaultChecked (boolean; optional):
    The default checked state. Use when the component is not
    controlled.

- disabled (boolean; optional):
    If `True`, the component is disabled.

- key (string | number; optional)

- readOnly (boolean; optional):
    If `True`, the component is read only.

- required (boolean; optional):
    If `True`, the `input` element is required."""
    @_explicitize_args
    def __init__(self, className=Component.UNDEFINED, checked=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, disabled=Component.UNDEFINED, readOnly=Component.UNDEFINED, required=Component.UNDEFINED, key=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'checked', 'className', 'defaultChecked', 'disabled', 'key', 'readOnly', 'required']
        self._type = 'SwitchUnstyled'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'checked', 'className', 'defaultChecked', 'disabled', 'key', 'readOnly', 'required']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SwitchUnstyled, self).__init__(**args)
