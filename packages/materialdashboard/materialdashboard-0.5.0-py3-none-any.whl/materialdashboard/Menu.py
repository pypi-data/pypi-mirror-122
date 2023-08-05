# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Menu(Component):
    """A Menu component.
Material-UI Menu.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Menu contents, normally `MenuItem`s.

- id (string; optional)

- about (string; optional)

- accessKey (string; optional)

- anchorEl (string; optional):
    An HTML element, or a function that returns one. It's used to set
    the position of the menu.

- anchorReference (a value equal to: "none", "anchorEl", "anchorPosition"; optional):
    This determines which anchor prop to refer to when setting the
    position of the popover.

- autoCapitalize (string; optional)

- autoCorrect (string; optional)

- autoFocus (boolean; optional):
    If `True` (Default) will focus the `[role=\"menu\"]` if no
    focusable child is found. Disabled children are not focusable. If
    you set this prop to `False` focus will be placed on the parent
    modal container. This has severe accessibility implications and
    should only be considered if you manage focus otherwise.

- autoSave (string; optional)

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- closeAfterTransition (boolean; optional):
    When set to True the Modal waits until a nested Transition is
    completed before closing.

- color (string; optional)

- container (string; optional):
    An HTML element, component instance, or function that returns
    either. The `container` will passed to the Modal component.  By
    default, it uses the body of the anchorEl's top-level document
    object, so it's simply `document.body` most of the time.

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

- disableAutoFocusItem (boolean; optional):
    When opening the menu will not focus the active item but the
    `[role=\"menu\"]` unless `autoFocus` is also set to `False`. Not
    using the default means not following WAI-ARIA authoring
    practices. Please be considerate about possible accessibility
    implications.

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

- elevation (number; optional):
    The elevation of the popover.

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

- marginThreshold (number; optional):
    Specifies how close to the edge of the window the popover can
    appear.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- n_closes (number; default 0)

- open (boolean; optional):
    If `True`, the component is shown.

- placeholder (string; optional)

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- resource (string; optional)

- results (number; optional)

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

- variant (a value equal to: "menu", "selectedMenu"; optional):
    The variant to use. Use `menu` to prevent selected items from
    impacting the initial focus.

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, children=None, autoFocus=Component.UNDEFINED, disableAutoFocusItem=Component.UNDEFINED, open=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, elevation=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, key=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, closeAfterTransition=Component.UNDEFINED, disableAutoFocus=Component.UNDEFINED, disableEnforceFocus=Component.UNDEFINED, disableEscapeKeyDown=Component.UNDEFINED, disablePortal=Component.UNDEFINED, disableRestoreFocus=Component.UNDEFINED, disableScrollLock=Component.UNDEFINED, hideBackdrop=Component.UNDEFINED, keepMounted=Component.UNDEFINED, anchorReference=Component.UNDEFINED, marginThreshold=Component.UNDEFINED, n_closes=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, anchorEl=Component.UNDEFINED, container=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'about', 'accessKey', 'anchorEl', 'anchorReference', 'autoCapitalize', 'autoCorrect', 'autoFocus', 'autoSave', 'className', 'classes', 'closeAfterTransition', 'color', 'container', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableAutoFocus', 'disableAutoFocusItem', 'disableEnforceFocus', 'disableEscapeKeyDown', 'disablePortal', 'disableRestoreFocus', 'disableScrollLock', 'draggable', 'elevation', 'hidden', 'hideBackdrop', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'keepMounted', 'key', 'lang', 'marginThreshold', 'n_clicks', 'n_closes', 'open', 'placeholder', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'variant', 'vocab']
        self._type = 'Menu'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'about', 'accessKey', 'anchorEl', 'anchorReference', 'autoCapitalize', 'autoCorrect', 'autoFocus', 'autoSave', 'className', 'classes', 'closeAfterTransition', 'color', 'container', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableAutoFocus', 'disableAutoFocusItem', 'disableEnforceFocus', 'disableEscapeKeyDown', 'disablePortal', 'disableRestoreFocus', 'disableScrollLock', 'draggable', 'elevation', 'hidden', 'hideBackdrop', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'keepMounted', 'key', 'lang', 'marginThreshold', 'n_clicks', 'n_closes', 'open', 'placeholder', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'variant', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Menu, self).__init__(children=children, **args)
