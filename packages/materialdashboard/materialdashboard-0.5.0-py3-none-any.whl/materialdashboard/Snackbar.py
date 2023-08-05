# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Snackbar(Component):
    """A Snackbar component.
Material-UI Snackbar.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Replace the `SnackbarContent` component.

- id (string; optional)

- about (string; optional)

- accessKey (string; optional)

- action (boolean | number | string | dict | list; optional):
    The action to display. It renders after the message, at the end of
    the snackbar.

- autoCapitalize (string; optional)

- autoCorrect (string; optional)

- autoHideDuration (number; optional):
    The number of milliseconds to wait before automatically calling
    the `onClose` function. `onClose` should then set the state of the
    `open` prop to hide the Snackbar. This behavior is disabled by
    default with the `None` value.

- autoSave (string; optional)

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- color (string; optional)

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- dir (string; optional)

- disableWindowBlurListener (boolean; optional):
    If `True`, the `autoHideDuration` timer will expire even if the
    window is not focused.

- draggable (a value equal to: false, true, "true", "false"; optional)

- hidden (boolean; optional)

- inlist (boolean | number | string | dict | list; optional)

- inputMode (a value equal to: "text", "none", "search", "tel", "url", "email", "numeric", "decimal"; optional):
    Hints at the type of data that might be entered by the user while
    editing the element or its contents.

- is (string; optional):
    Specify that a standard HTML element should behave like a defined
    custom built-in element.

- itemID (string; optional)

- itemProp (string; optional)

- itemRef (string; optional)

- itemScope (boolean; optional)

- itemType (string; optional)

- key (boolean | number | string | dict | list; optional):
    When displaying multiple consecutive Snackbars from a parent
    rendering a single <Snackbar/>, add the key prop to ensure
    independent treatment of each message. e.g. <Snackbar
    key={message} />, otherwise, the message may update-in-place and
    features such as autoHideDuration may be canceled.

- lang (string; optional)

- message (boolean | number | string | dict | list; optional):
    The message to display.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- open (boolean; optional):
    If `True`, the component is shown.

- placeholder (string; optional)

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- resource (string; optional)

- results (number; optional)

- resumeHideDuration (number; optional):
    The number of milliseconds to wait before dismissing after user
    interaction. If `autoHideDuration` prop isn't specified, it does
    nothing. If `autoHideDuration` prop is specified but
    `resumeHideDuration` isn't, we default to `autoHideDuration / 2`
    ms.

- security (string; optional)

- slot (string; optional)

- spellCheck (a value equal to: false, true, "true", "false"; optional)

- style (dict; optional)

- suppressContentEditableWarning (boolean; optional)

- suppressHydrationWarning (boolean; optional)

- tabIndex (number; optional)

- title (string; optional)

- translate (a value equal to: "yes", "no"; optional)

- typeof (string; optional)

- unselectable (a value equal to: "on", "off"; optional)

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, children=None, action=Component.UNDEFINED, autoHideDuration=Component.UNDEFINED, disableWindowBlurListener=Component.UNDEFINED, key=Component.UNDEFINED, message=Component.UNDEFINED, open=Component.UNDEFINED, resumeHideDuration=Component.UNDEFINED, className=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'about', 'accessKey', 'action', 'autoCapitalize', 'autoCorrect', 'autoHideDuration', 'autoSave', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableWindowBlurListener', 'draggable', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'message', 'n_clicks', 'open', 'placeholder', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'resumeHideDuration', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab']
        self._type = 'Snackbar'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'about', 'accessKey', 'action', 'autoCapitalize', 'autoCorrect', 'autoHideDuration', 'autoSave', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableWindowBlurListener', 'draggable', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'message', 'n_clicks', 'open', 'placeholder', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'resumeHideDuration', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Snackbar, self).__init__(children=children, **args)
