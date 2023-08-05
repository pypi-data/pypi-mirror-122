# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Backdrop(Component):
    """A Backdrop component.
Material-UI Backdrop.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- appear (boolean; optional):
    Perform the enter transition when it first mounts if `in` is also
    `True`. Set this to `False` to disable this behavior.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- enter (boolean; optional):
    Enable or disable enter transitions.

- exit (boolean; optional):
    Enable or disable exit transitions.

- in (boolean; optional):
    If `True`, the component will transition in.

- invisible (boolean; optional):
    If `True`, the backdrop is invisible. It can be used when
    rendering a popover or a custom select component.

- mountOnEnter (boolean; optional):
    By default the child component is mounted immediately along with
    the parent Transition component. If you want to \"lazy mount\" the
    component on the first `in={True}` you can set `mountOnEnter`.
    After the first enter transition the component will stay mounted,
    even on \"exited\", unless you also specify `unmountOnExit`.

- open (boolean; optional):
    If `True`, the component is shown.

- style (dict; optional)

- unmountOnExit (boolean; optional):
    By default the child component stays mounted after it reaches the
    'exited' state. Set `unmountOnExit` if you'd prefer to unmount the
    component after it finishes exiting."""
    @_explicitize_args
    def __init__(self, children=None, mountOnEnter=Component.UNDEFINED, unmountOnExit=Component.UNDEFINED, enter=Component.UNDEFINED, appear=Component.UNDEFINED, exit=Component.UNDEFINED, open=Component.UNDEFINED, invisible=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'appear', 'className', 'classes', 'enter', 'exit', 'in', 'invisible', 'mountOnEnter', 'open', 'style', 'unmountOnExit']
        self._type = 'Backdrop'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'appear', 'className', 'classes', 'enter', 'exit', 'in', 'invisible', 'mountOnEnter', 'open', 'style', 'unmountOnExit']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Backdrop, self).__init__(children=children, **args)
