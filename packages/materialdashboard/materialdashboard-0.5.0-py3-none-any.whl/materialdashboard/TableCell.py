# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TableCell(Component):
    """A TableCell component.
Material-UI TableCell.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional)

- abbr (string; optional)

- about (string; optional)

- accessKey (string; optional)

- align (a value equal to: "inherit", "left", "right", "center", "justify"; optional):
    Set the text-align on the table cell content.  Monetary or
    generally number fields **should be right aligned** as that allows
    you to add them up quickly in your head without having to worry
    about decimals.

- autoCapitalize (string; optional)

- autoCorrect (string; optional)

- autoSave (string; optional)

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- colSpan (number; optional)

- color (string; optional)

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- dir (string; optional)

- draggable (a value equal to: false, true, "true", "false"; optional)

- headers (string; optional)

- height (string | number; optional)

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

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- padding (a value equal to: "checkbox", "none", "normal"; optional):
    Sets the padding applied to the cell. The prop defaults to the
    value (`'default'`) inherited from the parent Table component.

- placeholder (string; optional)

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- resource (string; optional)

- results (number; optional)

- rowSpan (number; optional)

- scope (string; optional):
    Set scope attribute.

- security (string; optional)

- size (a value equal to: "small", "medium"; optional):
    Specify the size of the cell. The prop defaults to the value
    (`'medium'`) inherited from the parent Table component.

- slot (string; optional)

- sortDirection (a value equal to: false, "desc", "asc"; optional):
    Set aria-sort direction.

- spellCheck (a value equal to: false, true, "true", "false"; optional)

- style (dict; optional)

- suppressContentEditableWarning (boolean; optional)

- suppressHydrationWarning (boolean; optional)

- tabIndex (number; optional)

- title (string; optional)

- translate (a value equal to: "yes", "no"; optional)

- typeof (string; optional)

- unselectable (a value equal to: "on", "off"; optional)

- valign (a value equal to: "bottom", "top", "baseline", "middle"; optional)

- variant (a value equal to: "body", "footer", "head"; optional):
    Specify the cell type. The prop defaults to the value inherited
    from the parent TableHead, TableBody, or TableFooter components.

- vocab (string; optional)

- width (string | number; optional)"""
    @_explicitize_args
    def __init__(self, children=None, align=Component.UNDEFINED, padding=Component.UNDEFINED, scope=Component.UNDEFINED, size=Component.UNDEFINED, sortDirection=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, abbr=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, height=Component.UNDEFINED, width=Component.UNDEFINED, colSpan=Component.UNDEFINED, headers=Component.UNDEFINED, rowSpan=Component.UNDEFINED, valign=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'abbr', 'about', 'accessKey', 'align', 'autoCapitalize', 'autoCorrect', 'autoSave', 'className', 'classes', 'colSpan', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'draggable', 'headers', 'height', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'n_clicks', 'padding', 'placeholder', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'rowSpan', 'scope', 'security', 'size', 'slot', 'sortDirection', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'valign', 'variant', 'vocab', 'width']
        self._type = 'TableCell'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'abbr', 'about', 'accessKey', 'align', 'autoCapitalize', 'autoCorrect', 'autoSave', 'className', 'classes', 'colSpan', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'draggable', 'headers', 'height', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'n_clicks', 'padding', 'placeholder', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'rowSpan', 'scope', 'security', 'size', 'slot', 'sortDirection', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'valign', 'variant', 'vocab', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TableCell, self).__init__(children=children, **args)
