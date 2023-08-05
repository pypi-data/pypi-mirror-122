# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Link(Component):
    """A Link component.
Material-UI Link.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional)

- about (string; optional)

- accessKey (string; optional)

- align (a value equal to: "inherit", "left", "right", "center", "justify"; optional):
    Set the text-align on the component.

- autoCapitalize (string; optional)

- autoCorrect (string; optional)

- autoSave (string; optional)

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- dir (string; optional)

- download (boolean | number | string | dict | list; optional)

- draggable (a value equal to: false, true, "true", "false"; optional)

- gutterBottom (boolean; optional):
    If `True`, the text will have a bottom margin.

- hidden (boolean; optional)

- href (string; optional)

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

- noWrap (boolean; optional):
    If `True`, the text will not wrap, but instead will truncate with
    a text overflow ellipsis.  Note that text overflow can only happen
    with block or inline-block level elements (the element needs to
    have a width in order to overflow).

- paragraph (boolean; optional):
    If `True`, the element will be a paragraph element.

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

- slot (string; optional)

- spellCheck (a value equal to: false, true, "true", "false"; optional)

- style (dict; optional)

- suppressContentEditableWarning (boolean; optional)

- suppressHydrationWarning (boolean; optional)

- tabIndex (number; optional)

- title (string; optional)

- translate (a value equal to: "yes", "no"; optional)

- type (string; optional)

- typeof (string; optional)

- underline (a value equal to: "none", "hover", "always"; optional):
    Controls when the link should have an underline.

- unselectable (a value equal to: "on", "off"; optional)

- variant (a value equal to: "button", "caption", "h1", "h2", "h3", "h4", "h5", "h6", "inherit", "subtitle1", "subtitle2", "body1", "body2", "overline"; optional):
    Applies the theme typography styles.

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, children=None, className=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, key=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, download=Component.UNDEFINED, href=Component.UNDEFINED, hrefLang=Component.UNDEFINED, media=Component.UNDEFINED, ping=Component.UNDEFINED, rel=Component.UNDEFINED, type=Component.UNDEFINED, referrerPolicy=Component.UNDEFINED, align=Component.UNDEFINED, gutterBottom=Component.UNDEFINED, noWrap=Component.UNDEFINED, paragraph=Component.UNDEFINED, underline=Component.UNDEFINED, variant=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'about', 'accessKey', 'align', 'autoCapitalize', 'autoCorrect', 'autoSave', 'className', 'classes', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'download', 'draggable', 'gutterBottom', 'hidden', 'href', 'hrefLang', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'media', 'n_clicks', 'noWrap', 'paragraph', 'ping', 'placeholder', 'prefix', 'property', 'radioGroup', 'referrerPolicy', 'rel', 'resource', 'results', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'type', 'typeof', 'underline', 'unselectable', 'variant', 'vocab']
        self._type = 'Link'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'about', 'accessKey', 'align', 'autoCapitalize', 'autoCorrect', 'autoSave', 'className', 'classes', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'download', 'draggable', 'gutterBottom', 'hidden', 'href', 'hrefLang', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'media', 'n_clicks', 'noWrap', 'paragraph', 'ping', 'placeholder', 'prefix', 'property', 'radioGroup', 'referrerPolicy', 'rel', 'resource', 'results', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'type', 'typeof', 'underline', 'unselectable', 'variant', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Link, self).__init__(children=children, **args)
