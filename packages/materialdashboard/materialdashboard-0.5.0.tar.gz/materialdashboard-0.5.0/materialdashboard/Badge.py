# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Badge(Component):
    """A Badge component.
Material-UI Badge.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The badge will be added relative to this node.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- badgeContent (boolean | number | string | dict | list; optional):
    The content rendered within the badge.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- color (a value equal to: "success", "info", "warning", "error", "primary", "secondary", "default"; optional):
    The color of the component. It supports those theme colors that
    make sense for this component.

- invisible (boolean; optional):
    If `True`, the badge is invisible.

- max (number; optional):
    Max count to show.

- overlap (a value equal to: "circular", "rectangular"; optional):
    Wrapped shape the badge should overlap.

- showZero (boolean; optional):
    Controls whether the badge is hidden when `badgeContent` is zero.

- style (dict; optional)

- variant (a value equal to: "standard", "dot"; optional):
    The variant to use."""
    @_explicitize_args
    def __init__(self, children=None, color=Component.UNDEFINED, variant=Component.UNDEFINED, overlap=Component.UNDEFINED, badgeContent=Component.UNDEFINED, invisible=Component.UNDEFINED, max=Component.UNDEFINED, showZero=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'badgeContent', 'className', 'classes', 'color', 'invisible', 'max', 'overlap', 'showZero', 'style', 'variant']
        self._type = 'Badge'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'badgeContent', 'className', 'classes', 'color', 'invisible', 'max', 'overlap', 'showZero', 'style', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Badge, self).__init__(children=children, **args)
