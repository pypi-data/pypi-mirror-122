# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class InputBase(Component):
    """An InputBase component.
Material-UI InputBase.

Keyword arguments:

- id (string; optional):
    The id of the `input` element.

- about (string; optional)

- accessKey (string; optional)

- autoCapitalize (string; optional)

- autoComplete (string; optional):
    This prop helps users to fill forms faster, especially on mobile
    devices. The name can be confusing, as it's more like an autofill.
    You can learn more about it [following the
    specification](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill).

- autoCorrect (string; optional)

- autoFocus (boolean; optional):
    If `True`, the `input` element is focused during the first mount.

- autoSave (string; optional)

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- color (a value equal to: "success", "info", "warning", "error", "primary", "secondary"; optional):
    The color of the component. It supports those theme colors that
    make sense for this component. The prop defaults to the value
    (`'primary'`) inherited from the parent FormControl component.

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- defaultValue (boolean | number | string | dict | list; optional):
    The default value. Use when the component is not controlled.

- dir (string; optional)

- disabled (boolean; optional):
    If `True`, the component is disabled. The prop defaults to the
    value (`False`) inherited from the parent FormControl component.

- draggable (a value equal to: false, true, "true", "false"; optional)

- endAdornment (boolean | number | string | dict | list; optional):
    End `InputAdornment` for this component.

- error (boolean; optional):
    If `True`, the `input` will indicate an error. The prop defaults
    to the value (`False`) inherited from the parent FormControl
    component.

- fullWidth (boolean; optional):
    If `True`, the `input` will take up the full width of its
    container.

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

- margin (a value equal to: "none", "dense"; optional):
    If `dense`, will adjust vertical spacing. This is normally
    obtained via context from FormControl. The prop defaults to the
    value (`'none'`) inherited from the parent FormControl component.

- maxRows (string | number; optional):
    Maximum number of rows to display when multiline option is set to
    True.

- minRows (string | number; optional):
    Minimum number of rows to display when multiline option is set to
    True.

- multiline (boolean; optional):
    If `True`, a `textarea` element is rendered.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- name (string; optional):
    Name attribute of the `input` element.

- placeholder (string; optional):
    The short hint displayed in the `input` before the user enters a
    value.

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- readOnly (boolean; optional):
    It prevents the user from changing the value of the field (not
    from interacting with the field).

- required (boolean; optional):
    If `True`, the `input` element is required. The prop defaults to
    the value (`False`) inherited from the parent FormControl
    component.

- resource (string; optional)

- results (number; optional)

- rows (string | number; optional):
    Number of rows to display when multiline option is set to True.

- security (string; optional)

- size (a value equal to: "small", "medium"; optional):
    The size of the component.

- slot (string; optional)

- spellCheck (a value equal to: false, true, "true", "false"; optional)

- startAdornment (boolean | number | string | dict | list; optional):
    Start `InputAdornment` for this component.

- style (dict; optional)

- suppressContentEditableWarning (boolean; optional)

- suppressHydrationWarning (boolean; optional)

- tabIndex (number; optional)

- title (string; optional)

- translate (a value equal to: "yes", "no"; optional)

- type (string; optional):
    Type of the `input` element. It should be [a valid HTML5 input
    type](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#Form_%3Cinput%3E_types).

- typeof (string; optional)

- unselectable (a value equal to: "on", "off"; optional)

- value (boolean | number | string | dict | list; optional):
    The value of the `input` element, required for a controlled
    component.

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, autoComplete=Component.UNDEFINED, autoFocus=Component.UNDEFINED, color=Component.UNDEFINED, defaultValue=Component.UNDEFINED, disabled=Component.UNDEFINED, endAdornment=Component.UNDEFINED, error=Component.UNDEFINED, fullWidth=Component.UNDEFINED, id=Component.UNDEFINED, margin=Component.UNDEFINED, multiline=Component.UNDEFINED, name=Component.UNDEFINED, placeholder=Component.UNDEFINED, readOnly=Component.UNDEFINED, required=Component.UNDEFINED, rows=Component.UNDEFINED, maxRows=Component.UNDEFINED, minRows=Component.UNDEFINED, size=Component.UNDEFINED, startAdornment=Component.UNDEFINED, type=Component.UNDEFINED, value=Component.UNDEFINED, className=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, lang=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'about', 'accessKey', 'autoCapitalize', 'autoComplete', 'autoCorrect', 'autoFocus', 'autoSave', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'defaultValue', 'dir', 'disabled', 'draggable', 'endAdornment', 'error', 'fullWidth', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'margin', 'maxRows', 'minRows', 'multiline', 'n_clicks', 'name', 'placeholder', 'prefix', 'property', 'radioGroup', 'readOnly', 'required', 'resource', 'results', 'rows', 'security', 'size', 'slot', 'spellCheck', 'startAdornment', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'type', 'typeof', 'unselectable', 'value', 'vocab']
        self._type = 'InputBase'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'about', 'accessKey', 'autoCapitalize', 'autoComplete', 'autoCorrect', 'autoFocus', 'autoSave', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'defaultValue', 'dir', 'disabled', 'draggable', 'endAdornment', 'error', 'fullWidth', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'margin', 'maxRows', 'minRows', 'multiline', 'n_clicks', 'name', 'placeholder', 'prefix', 'property', 'radioGroup', 'readOnly', 'required', 'resource', 'results', 'rows', 'security', 'size', 'slot', 'spellCheck', 'startAdornment', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'type', 'typeof', 'unselectable', 'value', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(InputBase, self).__init__(**args)
