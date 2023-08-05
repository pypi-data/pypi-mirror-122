# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Divider(Component):
    """A Divider component.
Material-UI Divider.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- absolute (boolean; optional):
    Absolutely position the element.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- flexItem (boolean; optional):
    If `True`, a vertical divider will have the correct height when
    used in flex container. (By default, a vertical divider will have
    a calculated height of `0px` if it is the child of a flex
    container.).

- light (boolean; optional):
    If `True`, the divider will have a lighter color.

- orientation (a value equal to: "horizontal", "vertical"; optional):
    The component orientation.

- style (dict; optional)

- textAlign (a value equal to: "left", "right", "center"; optional):
    The text alignment.

- variant (a value equal to: "inset", "middle", "fullWidth"; optional):
    The variant to use."""
    @_explicitize_args
    def __init__(self, children=None, absolute=Component.UNDEFINED, flexItem=Component.UNDEFINED, light=Component.UNDEFINED, orientation=Component.UNDEFINED, textAlign=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'absolute', 'className', 'classes', 'flexItem', 'light', 'orientation', 'style', 'textAlign', 'variant']
        self._type = 'Divider'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'absolute', 'className', 'classes', 'flexItem', 'light', 'orientation', 'style', 'textAlign', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Divider, self).__init__(children=children, **args)
