# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tooltip(Component):
    """A Tooltip component.
Material-UI Tooltip.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Tooltip reference element.

- id (string; optional):
    This prop is used to help implement the accessibility logic. If
    you don't provide this prop. It falls back to a randomly generated
    id.

- about (string; optional)

- accessKey (string; optional)

- arrow (boolean; optional):
    If `True`, adds an arrow to the tooltip.

- autoCapitalize (string; optional)

- autoCorrect (string; optional)

- autoSave (string; optional)

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- color (string; optional)

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- describeChild (boolean; optional):
    Set to `True` if the `title` acts as an accessible description. By
    default the `title` acts as an accessible label for the child.

- dir (string; optional)

- disableFocusListener (boolean; optional):
    Do not respond to focus-visible events.

- disableHoverListener (boolean; optional):
    Do not respond to hover events.

- disableInteractive (boolean; optional):
    Makes a tooltip not interactive, i.e. it will close when the user
    hovers over the tooltip before the `leaveDelay` is expired.

- disableTouchListener (boolean; optional):
    Do not respond to long press touch events.

- draggable (a value equal to: false, true, "true", "false"; optional)

- enterDelay (number; optional):
    The number of milliseconds to wait before showing the tooltip.
    This prop won't impact the enter touch delay (`enterTouchDelay`).

- enterNextDelay (number; optional):
    The number of milliseconds to wait before showing the tooltip when
    one was already recently opened.

- enterTouchDelay (number; optional):
    The number of milliseconds a user must touch the element before
    showing the tooltip.

- followCursor (boolean; optional):
    If `True`, the tooltip follow the cursor over the wrapped element.

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

- lang (string; optional)

- leaveDelay (number; optional):
    The number of milliseconds to wait before hiding the tooltip. This
    prop won't impact the leave touch delay (`leaveTouchDelay`).

- leaveTouchDelay (number; optional):
    The number of milliseconds after the user stops touching an
    element before hiding the tooltip.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- open (boolean; optional):
    If `True`, the component is shown.

- placeholder (string; optional)

- placement (a value equal to: "bottom", "left", "right", "top", "top-start", "top-end", "bottom-start", "bottom-end", "right-start", "right-end", "left-start", "left-end"; optional):
    Tooltip placement.

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

- title (boolean | number | string | dict | list; optional):
    Tooltip title. Zero-length titles string are never displayed.

- translate (a value equal to: "yes", "no"; optional)

- typeof (string; optional)

- unselectable (a value equal to: "on", "off"; optional)

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, children=None, arrow=Component.UNDEFINED, describeChild=Component.UNDEFINED, disableFocusListener=Component.UNDEFINED, disableHoverListener=Component.UNDEFINED, disableInteractive=Component.UNDEFINED, disableTouchListener=Component.UNDEFINED, enterDelay=Component.UNDEFINED, enterNextDelay=Component.UNDEFINED, enterTouchDelay=Component.UNDEFINED, followCursor=Component.UNDEFINED, id=Component.UNDEFINED, leaveDelay=Component.UNDEFINED, leaveTouchDelay=Component.UNDEFINED, open=Component.UNDEFINED, placement=Component.UNDEFINED, title=Component.UNDEFINED, className=Component.UNDEFINED, slot=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'about', 'accessKey', 'arrow', 'autoCapitalize', 'autoCorrect', 'autoSave', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'describeChild', 'dir', 'disableFocusListener', 'disableHoverListener', 'disableInteractive', 'disableTouchListener', 'draggable', 'enterDelay', 'enterNextDelay', 'enterTouchDelay', 'followCursor', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'leaveDelay', 'leaveTouchDelay', 'n_clicks', 'open', 'placeholder', 'placement', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab']
        self._type = 'Tooltip'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'about', 'accessKey', 'arrow', 'autoCapitalize', 'autoCorrect', 'autoSave', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'describeChild', 'dir', 'disableFocusListener', 'disableHoverListener', 'disableInteractive', 'disableTouchListener', 'draggable', 'enterDelay', 'enterNextDelay', 'enterTouchDelay', 'followCursor', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'leaveDelay', 'leaveTouchDelay', 'n_clicks', 'open', 'placeholder', 'placement', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tooltip, self).__init__(children=children, **args)
