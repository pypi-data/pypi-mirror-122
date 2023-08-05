# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.
Material-UI Button.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional)

- about (string; optional)

- accessKey (string; optional)

- autoCapitalize (string; optional)

- autoCorrect (string; optional)

- autoSave (string; optional)

- centerRipple (boolean; optional):
    If `True`, the ripples are centered. They won't start at the
    cursor interaction position.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- color (a value equal to: "inherit", "success", "info", "warning", "error", "primary", "secondary"; optional):
    The color of the component. It supports those theme colors that
    make sense for this component.

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- dir (string; optional)

- disableElevation (boolean; optional):
    If `True`, no elevation is used.

- disableFocusRipple (boolean; optional):
    If `True`, the  keyboard focus ripple is disabled.

- disableRipple (boolean; optional):
    If `True`, the ripple effect is disabled.  ⚠️ Without a ripple
    there is no styling for :focus-visible by default. Be sure to
    highlight the element by applying separate styles with the
    `.Mui-focusVisible` class.

- disableTouchRipple (boolean; optional):
    If `True`, the touch ripple effect is disabled.

- disabled (boolean; optional):
    If `True`, the component is disabled.

- download (boolean | number | string | dict | list; optional)

- draggable (a value equal to: false, true, "true", "false"; optional)

- endIcon (boolean | number | string | dict | list; optional):
    Element placed after the children.

- focusRipple (boolean; optional):
    If `True`, the base button will have a keyboard focus ripple.

- focusVisibleClassName (string; optional):
    This prop can help identify which element has keyboard focus. The
    class name will be applied when the element gains the focus
    through keyboard interaction. It's a polyfill for the [CSS
    :focus-visible
    selector](https://drafts.csswg.org/selectors-4/#the-focus-visible-pseudo).
    The rationale for using this feature [is explained
    here](https://github.com/WICG/focus-visible/blob/master/explainer.md).
    A [polyfill can be used](https://github.com/WICG/focus-visible) to
    apply a `focus-visible` class to other components if needed.

- fullWidth (boolean; optional):
    If `True`, the button will take up the full width of its
    container.

- hidden (boolean; optional)

- href (string; optional):
    The URL to link to when the button is clicked. If defined, an `a`
    element will be used as the root node.

- hrefLang (string; optional)

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

- key (string | number; optional)

- lang (string; optional)

- media (string; optional)

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- ping (string; optional)

- placeholder (string; optional)

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- referrerPolicy (a value equal to: "", "no-referrer", "no-referrer-when-downgrade", "origin", "origin-when-cross-origin", "same-origin", "strict-origin", "strict-origin-when-cross-origin", "unsafe-url"; optional)

- rel (string; optional)

- resource (string; optional)

- results (number; optional)

- security (string; optional)

- size (a value equal to: "small", "medium", "large"; optional):
    The size of the component. `small` is equivalent to the dense
    button styling.

- slot (string; optional)

- spellCheck (a value equal to: false, true, "true", "false"; optional)

- startIcon (boolean | number | string | dict | list; optional):
    Element placed before the children.

- style (dict; optional)

- suppressContentEditableWarning (boolean; optional)

- suppressHydrationWarning (boolean; optional)

- tabIndex (number; optional)

- title (string; optional)

- translate (a value equal to: "yes", "no"; optional)

- type (string; optional)

- typeof (string; optional)

- unselectable (a value equal to: "on", "off"; optional)

- variant (a value equal to: "text", "outlined", "contained"; optional):
    The variant to use.

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, children=None, href=Component.UNDEFINED, color=Component.UNDEFINED, disabled=Component.UNDEFINED, disableElevation=Component.UNDEFINED, disableFocusRipple=Component.UNDEFINED, endIcon=Component.UNDEFINED, fullWidth=Component.UNDEFINED, size=Component.UNDEFINED, startIcon=Component.UNDEFINED, variant=Component.UNDEFINED, tabIndex=Component.UNDEFINED, centerRipple=Component.UNDEFINED, disableRipple=Component.UNDEFINED, disableTouchRipple=Component.UNDEFINED, focusRipple=Component.UNDEFINED, focusVisibleClassName=Component.UNDEFINED, className=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, key=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, download=Component.UNDEFINED, hrefLang=Component.UNDEFINED, media=Component.UNDEFINED, ping=Component.UNDEFINED, rel=Component.UNDEFINED, type=Component.UNDEFINED, referrerPolicy=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'about', 'accessKey', 'autoCapitalize', 'autoCorrect', 'autoSave', 'centerRipple', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableElevation', 'disableFocusRipple', 'disableRipple', 'disableTouchRipple', 'disabled', 'download', 'draggable', 'endIcon', 'focusRipple', 'focusVisibleClassName', 'fullWidth', 'hidden', 'href', 'hrefLang', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'media', 'n_clicks', 'ping', 'placeholder', 'prefix', 'property', 'radioGroup', 'referrerPolicy', 'rel', 'resource', 'results', 'security', 'size', 'slot', 'spellCheck', 'startIcon', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'type', 'typeof', 'unselectable', 'variant', 'vocab']
        self._type = 'Button'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'about', 'accessKey', 'autoCapitalize', 'autoCorrect', 'autoSave', 'centerRipple', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableElevation', 'disableFocusRipple', 'disableRipple', 'disableTouchRipple', 'disabled', 'download', 'draggable', 'endIcon', 'focusRipple', 'focusVisibleClassName', 'fullWidth', 'hidden', 'href', 'hrefLang', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'media', 'n_clicks', 'ping', 'placeholder', 'prefix', 'property', 'radioGroup', 'referrerPolicy', 'rel', 'resource', 'results', 'security', 'size', 'slot', 'spellCheck', 'startIcon', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'type', 'typeof', 'unselectable', 'variant', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Button, self).__init__(children=children, **args)
