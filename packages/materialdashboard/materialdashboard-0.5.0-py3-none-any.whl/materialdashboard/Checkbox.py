# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Checkbox(Component):
    """A Checkbox component.
Material-UI Checkbox.

Keyword arguments:

- id (string; optional):
    The id of the `input` element.

- about (string; optional)

- accessKey (string; optional)

- autoCapitalize (string; optional)

- autoCorrect (string; optional)

- autoFocus (boolean; optional)

- autoSave (string; optional)

- centerRipple (boolean; optional):
    If `True`, the ripples are centered. They won't start at the
    cursor interaction position.

- checked (boolean; optional):
    If `True`, the component is checked.

- checkedIcon (boolean | number | string | dict | list; optional):
    The icon to display when the component is checked.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- color (a value equal to: "success", "info", "warning", "error", "primary", "secondary", "default"; optional):
    The color of the component. It supports those theme colors that
    make sense for this component.

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional):
    The default checked state. Use when the component is not
    controlled.

- dir (string; optional)

- disableFocusRipple (boolean; optional):
    If `True`, the  keyboard focus ripple is disabled.

- disableRipple (boolean; optional):
    If `True`, the ripple effect is disabled.

- disableTouchRipple (boolean; optional):
    If `True`, the touch ripple effect is disabled.

- disabled (boolean; optional):
    If `True`, the component is disabled.

- draggable (a value equal to: false, true, "true", "false"; optional)

- edge (a value equal to: false, "end", "start"; optional):
    If given, uses a negative margin to counteract the padding on one
    side (this is often helpful for aligning the left or right side of
    the icon with content above or below, without ruining the border
    size and shape).

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

- form (string; optional)

- formAction (string; optional)

- formEncType (string; optional)

- formMethod (string; optional)

- formNoValidate (boolean; optional)

- formTarget (string; optional)

- hidden (boolean; optional)

- icon (boolean | number | string | dict | list; optional):
    The icon to display when the component is unchecked.

- indeterminate (boolean; optional):
    If `True`, the component appears indeterminate. This does not set
    the native input element to indeterminate due to inconsistent
    behavior across browsers. However, we set a `data-indeterminate`
    attribute on the `input`.

- indeterminateIcon (boolean | number | string | dict | list; optional):
    The icon to display when the component is indeterminate.

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

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- name (string; optional):
    Name attribute of the `input` element.

- persisted_props (list of a value equal to: 'checked's; default ['checked']):
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

- placeholder (string; optional)

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- readOnly (boolean; optional)

- required (boolean; optional):
    If `True`, the `input` element is required.

- resource (string; optional)

- results (number; optional)

- security (string; optional)

- size (a value equal to: "small", "medium"; optional):
    The size of the component. `small` is equivalent to the dense
    checkbox styling.

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

- value (boolean | number | string | dict | list; optional):
    The value of the component. The DOM API casts this to a string.
    The browser uses \"on\" as the default value.

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, checked=Component.UNDEFINED, checkedIcon=Component.UNDEFINED, color=Component.UNDEFINED, disabled=Component.UNDEFINED, disableRipple=Component.UNDEFINED, icon=Component.UNDEFINED, id=Component.UNDEFINED, indeterminate=Component.UNDEFINED, indeterminateIcon=Component.UNDEFINED, required=Component.UNDEFINED, size=Component.UNDEFINED, value=Component.UNDEFINED, className=Component.UNDEFINED, form=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, key=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, centerRipple=Component.UNDEFINED, disableTouchRipple=Component.UNDEFINED, focusRipple=Component.UNDEFINED, focusVisibleClassName=Component.UNDEFINED, name=Component.UNDEFINED, autoFocus=Component.UNDEFINED, formAction=Component.UNDEFINED, formEncType=Component.UNDEFINED, formMethod=Component.UNDEFINED, formNoValidate=Component.UNDEFINED, formTarget=Component.UNDEFINED, readOnly=Component.UNDEFINED, disableFocusRipple=Component.UNDEFINED, edge=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'about', 'accessKey', 'autoCapitalize', 'autoCorrect', 'autoFocus', 'autoSave', 'centerRipple', 'checked', 'checkedIcon', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableFocusRipple', 'disableRipple', 'disableTouchRipple', 'disabled', 'draggable', 'edge', 'focusRipple', 'focusVisibleClassName', 'form', 'formAction', 'formEncType', 'formMethod', 'formNoValidate', 'formTarget', 'hidden', 'icon', 'indeterminate', 'indeterminateIcon', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'n_clicks', 'name', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'prefix', 'property', 'radioGroup', 'readOnly', 'required', 'resource', 'results', 'security', 'size', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'value', 'vocab']
        self._type = 'Checkbox'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'about', 'accessKey', 'autoCapitalize', 'autoCorrect', 'autoFocus', 'autoSave', 'centerRipple', 'checked', 'checkedIcon', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableFocusRipple', 'disableRipple', 'disableTouchRipple', 'disabled', 'draggable', 'edge', 'focusRipple', 'focusVisibleClassName', 'form', 'formAction', 'formEncType', 'formMethod', 'formNoValidate', 'formTarget', 'hidden', 'icon', 'indeterminate', 'indeterminateIcon', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'n_clicks', 'name', 'persisted_props', 'persistence', 'persistence_type', 'placeholder', 'prefix', 'property', 'radioGroup', 'readOnly', 'required', 'resource', 'results', 'security', 'size', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'value', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Checkbox, self).__init__(**args)
