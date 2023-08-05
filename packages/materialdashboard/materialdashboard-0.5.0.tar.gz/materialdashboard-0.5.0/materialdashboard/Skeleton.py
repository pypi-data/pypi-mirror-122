# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Skeleton(Component):
    """A Skeleton component.
Material-UI Skeleton.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Optional children to infer width and height from.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- animation (a value equal to: false, "pulse", "wave"; optional):
    The animation. If `False` the animation effect is disabled.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- height (string | number; optional):
    Height of the skeleton. Useful when you don't want to adapt the
    skeleton to a text element but for instance a card.

- style (dict; optional)

- variant (a value equal to: "text", "circular", "rectangular"; optional):
    The type of content that will be rendered.

- width (string | number; optional):
    Width of the skeleton. Useful when the skeleton is inside an
    inline element with no width of its own."""
    @_explicitize_args
    def __init__(self, children=None, animation=Component.UNDEFINED, height=Component.UNDEFINED, variant=Component.UNDEFINED, width=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'animation', 'className', 'classes', 'height', 'style', 'variant', 'width']
        self._type = 'Skeleton'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'animation', 'className', 'classes', 'height', 'style', 'variant', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Skeleton, self).__init__(children=children, **args)
