# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ImageList(Component):
    """An ImageList component.
Material-UI ImageList.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component, normally `ImageListItem`s.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- cols (number; optional):
    Number of columns.

- gap (number; optional):
    The gap between items in px.

- rowHeight (number | string; optional):
    The height of one row in px.

- style (dict; optional)

- variant (a value equal to: "standard", "masonry", "quilted", "woven"; optional):
    The variant to use."""
    @_explicitize_args
    def __init__(self, children=None, cols=Component.UNDEFINED, gap=Component.UNDEFINED, rowHeight=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'classes', 'cols', 'gap', 'rowHeight', 'style', 'variant']
        self._type = 'ImageList'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'classes', 'cols', 'gap', 'rowHeight', 'style', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ImageList, self).__init__(children=children, **args)
