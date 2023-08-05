# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ExtendBadgeUnstyled(Component):
    """An ExtendBadgeUnstyled component.
Material-UI ExtendBadgeUnstyled.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The badge will be added relative to this node.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- badgeContent (boolean | number | string | dict | list; optional):
    The content rendered within the badge.

- classes (dict; optional):
    Override or extend the styles applied to the component.

- invisible (boolean; optional):
    If `True`, the badge is invisible.

- max (number; optional):
    Max count to show.

- overlap (a value equal to: "circular", "rectangular"; optional):
    Wrapped shape the badge should overlap.

- showZero (boolean; optional):
    Controls whether the badge is hidden when `badgeContent` is zero.

- variant (string; optional):
    The variant to use."""
    @_explicitize_args
    def __init__(self, children=None, overlap=Component.UNDEFINED, badgeContent=Component.UNDEFINED, invisible=Component.UNDEFINED, max=Component.UNDEFINED, showZero=Component.UNDEFINED, variant=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'badgeContent', 'classes', 'invisible', 'max', 'overlap', 'showZero', 'variant']
        self._type = 'ExtendBadgeUnstyled'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'badgeContent', 'classes', 'invisible', 'max', 'overlap', 'showZero', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ExtendBadgeUnstyled, self).__init__(children=children, **args)
