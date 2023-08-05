# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dialog(Component):
    """A Dialog component.
Material-UI Dialog.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Dialog children, usually the included sub-components.

- id (string; optional)

- about (string; optional)

- accessKey (string; optional)

- autoCapitalize (string; optional)

- autoCorrect (string; optional)

- autoSave (string; optional)

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- closeAfterTransition (boolean; optional):
    When set to True the Modal waits until a nested Transition is
    completed before closing.

- color (string; optional)

- container (string; optional):
    An HTML element or function that returns one. The `container` will
    have the portal children appended to it.  By default, it uses the
    body of the top-level document object, so it's simply
    `document.body` most of the time.

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- dir (string; optional)

- disableAutoFocus (boolean; optional):
    If `True`, the modal will not automatically shift focus to itself
    when it opens, and replace it to the last focused element when it
    closes. This also works correctly with any modal children that
    have the `disableAutoFocus` prop.  Generally this should never be
    set to `True` as it makes the modal less accessible to assistive
    technologies, like screen readers.

- disableEnforceFocus (boolean; optional):
    If `True`, the modal will not prevent focus from leaving the modal
    while open.  Generally this should never be set to `True` as it
    makes the modal less accessible to assistive technologies, like
    screen readers.

- disableEscapeKeyDown (boolean; optional):
    If `True`, hitting escape will not fire the `onClose` callback.

- disablePortal (boolean; optional):
    The `children` will be under the DOM hierarchy of the parent
    component.

- disableRestoreFocus (boolean; optional):
    If `True`, the modal will not restore focus to previously focused
    element once modal is hidden.

- disableScrollLock (boolean; optional):
    Disable the scroll lock behavior.

- draggable (a value equal to: false, true, "true", "false"; optional)

- fullScreen (boolean; optional):
    If `True`, the dialog is full-screen.

- fullWidth (boolean; optional):
    If `True`, the dialog stretches to `maxWidth`.  Notice that the
    dialog width grow is limited by the default margin.

- hidden (boolean; optional)

- hideBackdrop (boolean; optional):
    If `True`, the backdrop is not rendered.

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

- keepMounted (boolean; optional):
    Always keep the children in the DOM. This prop can be useful in
    SEO situation or when you want to maximize the responsiveness of
    the Modal.

- key (string | number; optional)

- lang (string; optional)

- maxWidth (a value equal to: false, "xs", "sm", "md", "lg", "xl"; optional):
    Determine the max-width of the dialog. The dialog width grows with
    the size of the screen. Set to `False` to disable `maxWidth`.

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

- scroll (a value equal to: "body", "paper"; optional):
    Determine the container for scrolling the dialog.

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
    def __init__(self, children=None, disableEscapeKeyDown=Component.UNDEFINED, fullScreen=Component.UNDEFINED, fullWidth=Component.UNDEFINED, maxWidth=Component.UNDEFINED, open=Component.UNDEFINED, scroll=Component.UNDEFINED, className=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, key=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, closeAfterTransition=Component.UNDEFINED, disableAutoFocus=Component.UNDEFINED, disableEnforceFocus=Component.UNDEFINED, disablePortal=Component.UNDEFINED, disableRestoreFocus=Component.UNDEFINED, disableScrollLock=Component.UNDEFINED, hideBackdrop=Component.UNDEFINED, keepMounted=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, container=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'about', 'accessKey', 'autoCapitalize', 'autoCorrect', 'autoSave', 'className', 'classes', 'closeAfterTransition', 'color', 'container', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableAutoFocus', 'disableEnforceFocus', 'disableEscapeKeyDown', 'disablePortal', 'disableRestoreFocus', 'disableScrollLock', 'draggable', 'fullScreen', 'fullWidth', 'hidden', 'hideBackdrop', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'keepMounted', 'key', 'lang', 'maxWidth', 'n_clicks', 'open', 'placeholder', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'scroll', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab']
        self._type = 'Dialog'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'about', 'accessKey', 'autoCapitalize', 'autoCorrect', 'autoSave', 'className', 'classes', 'closeAfterTransition', 'color', 'container', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableAutoFocus', 'disableEnforceFocus', 'disableEscapeKeyDown', 'disablePortal', 'disableRestoreFocus', 'disableScrollLock', 'draggable', 'fullScreen', 'fullWidth', 'hidden', 'hideBackdrop', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'keepMounted', 'key', 'lang', 'maxWidth', 'n_clicks', 'open', 'placeholder', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'scroll', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Dialog, self).__init__(children=children, **args)
