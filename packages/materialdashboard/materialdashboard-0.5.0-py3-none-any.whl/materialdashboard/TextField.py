# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TextField(Component):
    """A TextField component.
Material-UI TextField.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the component.

- id (string; optional):
    The id of the `input` element. Use this prop to make `label` and
    `helperText` accessible for screen readers.

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
    make sense for this component.

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- defaultValue (boolean | number | string | dict | list; optional):
    The default value. Use when the component is not controlled.

- dir (string; optional)

- disabled (boolean; optional):
    If `True`, the component is disabled.

- draggable (a value equal to: false, true, "true", "false"; optional)

- error (boolean; optional):
    If `True`, the label is displayed in an error state.

- focused (boolean; optional):
    If `True`, the component is displayed in focused state.

- fullWidth (boolean; optional):
    If `True`, the input will take up the full width of its container.

- helperText (boolean | number | string | dict | list; optional):
    The helper text content.

- hidden (boolean; optional)

- hiddenLabel (boolean; optional):
    If `True`, the label is hidden. This is used to increase density
    for a `FilledInput`. Be sure to add `aria-label` to the `input`
    element.

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

- label (boolean | number | string | dict | list; optional):
    The label content.

- lang (string; optional)

- margin (a value equal to: "none", "normal", "dense"; optional):
    If `dense` or `normal`, will adjust vertical spacing of this and
    contained components.

- maxRows (string | number; optional):
    Maximum number of rows to display when multiline option is set to
    True.

- minRows (string | number; optional):
    Minimum number of rows to display when multiline option is set to
    True.

- multiline (boolean; optional):
    If `True`, a `textarea` element is rendered instead of an input.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- name (string; optional):
    Name attribute of the `input` element.

- persisted_props (list of a value equal to: 'value's; default ['value']):
    Properties whose user interactions will persist after refreshing
    the  component or the page. Since only `value` is allowed this
    prop can normally be ignored.

- persistence (boolean | string | number; optional):
    Used to allow user interactions in this component to be persisted
    when  the component - or the page - is refreshed. If `persisted`
    is truthy and  hasn't changed from its previous value, a `value`
    that the user has  changed while using the app will keep that
    change, as long as  the new `value` also matches what was given
    originally. Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory', 'location'; default 'local'):
    Where persisted user changes will be stored:  memory: only kept in
    memory, reset on page refresh.  local: window.localStorage, data
    is kept after the browser quit.  session: window.sessionStorage,
    data is cleared once the browser quit.  location: window.location,
    data appears in the URL and can be shared with others.

- placeholder (string; optional):
    The short hint displayed in the `input` before the user enters a
    value.

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- required (boolean; optional):
    If `True`, the label is displayed as required and the `input`
    element is required.

- resource (string; optional)

- results (number; optional)

- rows (string | number; optional):
    Number of rows to display when multiline option is set to True.

- security (string; optional)

- select (boolean; optional):
    Render a [`Select`](/api/select/) element while passing the Input
    element to `Select` as `input` parameter. If this option is set
    you must pass the options of the select as children.

- size (a value equal to: "small", "medium"; optional):
    The size of the component.

- slot (string; optional)

- spellCheck (a value equal to: false, true, "true", "false"; optional)

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

- variant (a value equal to: "outlined", "standard", "filled"; optional):
    The variant to use.

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, children=None, variant=Component.UNDEFINED, autoComplete=Component.UNDEFINED, autoFocus=Component.UNDEFINED, color=Component.UNDEFINED, defaultValue=Component.UNDEFINED, disabled=Component.UNDEFINED, error=Component.UNDEFINED, fullWidth=Component.UNDEFINED, helperText=Component.UNDEFINED, id=Component.UNDEFINED, label=Component.UNDEFINED, multiline=Component.UNDEFINED, name=Component.UNDEFINED, placeholder=Component.UNDEFINED, required=Component.UNDEFINED, rows=Component.UNDEFINED, maxRows=Component.UNDEFINED, minRows=Component.UNDEFINED, select=Component.UNDEFINED, size=Component.UNDEFINED, type=Component.UNDEFINED, value=Component.UNDEFINED, className=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, key=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, lang=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, margin=Component.UNDEFINED, focused=Component.UNDEFINED, hiddenLabel=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'about', 'accessKey', 'autoCapitalize', 'autoComplete', 'autoCorrect', 'autoFocus', 'autoSave', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'defaultValue', 'dir', 'disabled', 'draggable', 'error', 'focused', 'fullWidth', 'helperText', 'hidden', 'hiddenLabel', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'label', 'lang', 'margin', 'maxRows', 'minRows', 'multiline', 'n_clicks', 'name', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'prefix', 'property', 'radioGroup', 'required', 'resource', 'results', 'rows', 'security', 'select', 'size', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'type', 'typeof', 'unselectable', 'value', 'variant', 'vocab']
        self._type = 'TextField'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'about', 'accessKey', 'autoCapitalize', 'autoComplete', 'autoCorrect', 'autoFocus', 'autoSave', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'defaultValue', 'dir', 'disabled', 'draggable', 'error', 'focused', 'fullWidth', 'helperText', 'hidden', 'hiddenLabel', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'label', 'lang', 'margin', 'maxRows', 'minRows', 'multiline', 'n_clicks', 'name', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'prefix', 'property', 'radioGroup', 'required', 'resource', 'results', 'rows', 'security', 'select', 'size', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'type', 'typeof', 'unselectable', 'value', 'variant', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TextField, self).__init__(children=children, **args)
