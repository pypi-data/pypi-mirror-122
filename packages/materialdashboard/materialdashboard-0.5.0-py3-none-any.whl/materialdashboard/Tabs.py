# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tabs(Component):
    """A Tabs component.
Material-UI Tabs.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- allowScrollButtonsMobile (boolean; optional):
    If `True`, the scroll buttons aren't forced hidden on mobile. By
    default the scroll buttons are hidden on mobile and takes
    precedence over `scrollButtons`.

- centered (boolean; optional):
    If `True`, the tabs are centered. This prop is intended for large
    views.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- indicatorColor (a value equal to: "primary", "secondary"; optional):
    Determines the color of the indicator.

- orientation (a value equal to: "horizontal", "vertical"; optional):
    The component orientation (layout flow direction).

- scrollButtons (a value equal to: false, true, "auto"; optional):
    Determine behavior of scroll buttons when tabs are set to scroll:
    - `auto` will only present them when not all the items are
    visible. - `True` will always present them. - `False` will never
    present them.  By default the scroll buttons are hidden on mobile.
    This behavior can be disabled with `allowScrollButtonsMobile`.

- selectionFollowsFocus (boolean; optional):
    If `True` the selected tab changes on focus. Otherwise it only
    changes on activation.

- style (dict; optional)

- textColor (a value equal to: "inherit", "primary", "secondary"; optional):
    Determines the color of the `Tab`.

- value (boolean | number | string | dict | list; optional):
    The value of the currently selected `Tab`. If you don't want any
    selected `Tab`, you can set this prop to `False`.

- variant (a value equal to: "standard", "fullWidth", "scrollable"; optional):
    Determines additional display behavior of the tabs:  -
    `scrollable` will invoke scrolling properties and allow for
    horizontally scrolling (or swiping) of the tab bar. -`fullWidth`
    will make the tabs grow to use all the available space, which
    should be used for small views, like on mobile. - `standard` will
    render the default state.

- visibleScrollbar (boolean; optional):
    If `True`, the scrollbar is visible. It can be useful when
    displaying a long vertical list of tabs."""
    @_explicitize_args
    def __init__(self, children=None, allowScrollButtonsMobile=Component.UNDEFINED, centered=Component.UNDEFINED, indicatorColor=Component.UNDEFINED, orientation=Component.UNDEFINED, scrollButtons=Component.UNDEFINED, selectionFollowsFocus=Component.UNDEFINED, textColor=Component.UNDEFINED, value=Component.UNDEFINED, variant=Component.UNDEFINED, visibleScrollbar=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'allowScrollButtonsMobile', 'centered', 'className', 'classes', 'indicatorColor', 'orientation', 'scrollButtons', 'selectionFollowsFocus', 'style', 'textColor', 'value', 'variant', 'visibleScrollbar']
        self._type = 'Tabs'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'allowScrollButtonsMobile', 'centered', 'className', 'classes', 'indicatorColor', 'orientation', 'scrollButtons', 'selectionFollowsFocus', 'style', 'textColor', 'value', 'variant', 'visibleScrollbar']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tabs, self).__init__(children=children, **args)
