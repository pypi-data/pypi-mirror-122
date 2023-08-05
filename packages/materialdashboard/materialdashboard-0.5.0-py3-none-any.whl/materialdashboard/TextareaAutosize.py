# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TextareaAutosize(Component):
    """A TextareaAutosize component.
Material-UI TextareaAutosize.

Keyword arguments:

- id (string; optional)

- about (string; optional)

- accessKey (string; optional)

- autoCapitalize (string; optional)

- autoComplete (string; optional)

- autoCorrect (string; optional)

- autoFocus (boolean; optional)

- autoSave (string; optional)

- className (string; optional)

- color (string; optional)

- cols (number; optional)

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- dir (string; optional)

- dirName (string; optional)

- disabled (boolean; optional)

- draggable (a value equal to: false, true, "true", "false"; optional)

- form (string; optional)

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

- maxLength (number; optional)

- maxRows (string | number; optional):
    Maximum number of rows to display.

- minLength (number; optional)

- minRows (string | number; optional):
    Minimum number of rows to display.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- name (string; optional)

- placeholder (string; optional)

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- readOnly (boolean; optional)

- required (boolean; optional)

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

- vocab (string; optional)

- wrap (string; optional)"""
    @_explicitize_args
    def __init__(self, maxRows=Component.UNDEFINED, minRows=Component.UNDEFINED, className=Component.UNDEFINED, form=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, disabled=Component.UNDEFINED, name=Component.UNDEFINED, autoFocus=Component.UNDEFINED, autoComplete=Component.UNDEFINED, maxLength=Component.UNDEFINED, minLength=Component.UNDEFINED, readOnly=Component.UNDEFINED, required=Component.UNDEFINED, cols=Component.UNDEFINED, dirName=Component.UNDEFINED, wrap=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'about', 'accessKey', 'autoCapitalize', 'autoComplete', 'autoCorrect', 'autoFocus', 'autoSave', 'className', 'color', 'cols', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'dirName', 'disabled', 'draggable', 'form', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'maxLength', 'maxRows', 'minLength', 'minRows', 'n_clicks', 'name', 'placeholder', 'prefix', 'property', 'radioGroup', 'readOnly', 'required', 'resource', 'results', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab', 'wrap']
        self._type = 'TextareaAutosize'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'about', 'accessKey', 'autoCapitalize', 'autoComplete', 'autoCorrect', 'autoFocus', 'autoSave', 'className', 'color', 'cols', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'dirName', 'disabled', 'draggable', 'form', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'maxLength', 'maxRows', 'minLength', 'minRows', 'n_clicks', 'name', 'placeholder', 'prefix', 'property', 'radioGroup', 'readOnly', 'required', 'resource', 'results', 'security', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab', 'wrap']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TextareaAutosize, self).__init__(**args)
