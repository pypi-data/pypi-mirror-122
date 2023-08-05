# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Autocomplete(Component):
    """An Autocomplete component.
Material-UI Autocomplete.

Keyword arguments:

- id (string; optional):
    This prop is used to help implement the accessibility logic. If
    you don't provide an id it will fall back to a randomly generated
    one.

- about (string; optional)

- accessKey (string; optional)

- autoCapitalize (string; optional)

- autoComplete (boolean; optional):
    If `True`, the portion of the selected suggestion that has not
    been typed by the user, known as the completion string, appears
    inline after the input cursor in the textbox. The inline
    completion string is visually highlighted and has a selected
    state.

- autoCorrect (string; optional)

- autoHighlight (boolean; optional):
    If `True`, the first option is automatically highlighted.

- autoSave (string; optional)

- autoSelect (boolean; optional):
    If `True`, the selected option becomes the value of the input when
    the Autocomplete loses focus unless the user chooses a different
    option or changes the character string in the input.

- blurOnSelect (a value equal to: false, true, "touch", "mouse"; optional):
    Control if the input should be blurred when an option is selected:
    - `False` the input is not blurred. - `True` the input is always
    blurred. - `touch` the input is blurred after a touch event. -
    `mouse` the input is blurred after a mouse event.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- clearIcon (boolean | number | string | dict | list; optional):
    The icon to display in place of the default clear icon.

- clearOnBlur (boolean; optional):
    If `True`, the input's text is cleared on blur if no value is
    selected.  Set to `True` if you want to help the user enter a new
    value. Set to `False` if you want to help the user resume his
    search.

- clearOnEscape (boolean; optional):
    If `True`, clear all values when the user presses escape and the
    popup is closed.

- clearText (string; optional):
    Override the default text for the *clear* icon button.  For
    localization purposes, you can use the provided
    [translations](/guides/localization/).

- closeText (string; optional):
    Override the default text for the *close popup* icon button.  For
    localization purposes, you can use the provided
    [translations](/guides/localization/).

- color (string; optional)

- componentName (string; optional):
    The component name that is using this hook. Used for warnings.

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- dir (string; optional)

- disableCloseOnSelect (boolean; optional):
    If `True`, the popup won't close when a value is selected.

- disableListWrap (boolean; optional):
    If `True`, the list box in the popup will not wrap focus.

- disablePortal (boolean; optional):
    If `True`, the `Popper` content will be under the DOM hierarchy of
    the parent component.

- disabled (boolean; optional):
    If `True`, the component is disabled.

- disabledItemsFocusable (boolean; optional):
    If `True`, will allow focus on disabled items.

- draggable (a value equal to: false, true, "true", "false"; optional)

- filterSelectedOptions (boolean; optional):
    If `True`, hide the selected options from the list box.

- forcePopupIcon (a value equal to: false, true, "auto"; optional):
    Force the visibility display of the popup icon.

- fullWidth (boolean; optional):
    If `True`, the input will take up the full width of its container.

- handleHomeEndKeys (boolean; optional):
    If `True`, the component handles the \"Home\" and \"End\" keys
    when the popup is open. It should move focus to the first option
    and last option, respectively.

- hidden (boolean; optional)

- includeInputInList (boolean; optional):
    If `True`, the highlight can move to the input.

- inlist (boolean | number | string | dict | list; optional)

- inputMode (a value equal to: "text", "none", "search", "tel", "url", "email", "numeric", "decimal"; optional):
    Hints at the type of data that might be entered by the user while
    editing the element or its contents.

- inputValue (string; optional):
    The input value.

- is (string; optional):
    Specify that a standard HTML element should behave like a defined
    custom built-in element.

- itemID (string; optional)

- itemProp (string; optional)

- itemRef (string; optional)

- itemScope (boolean; optional)

- itemType (string; optional)

- lang (string; optional)

- limitTags (number; optional):
    The maximum number of tags that will be visible when not focused.
    Set `-1` to disable the limit.

- loading (boolean; optional):
    If `True`, the component is in a loading state. This shows the
    `loadingText` in place of suggestions (only if there are no
    suggestions to show, e.g. `options` are empty).

- loadingText (boolean | number | string | dict | list; optional):
    Text to display when in a loading state.  For localization
    purposes, you can use the provided
    [translations](/guides/localization/).

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- noOptionsText (boolean | number | string | dict | list; optional):
    Text to display when there are no options.  For localization
    purposes, you can use the provided
    [translations](/guides/localization/).

- open (boolean; optional):
    If `True`, the component is shown.

- openOnFocus (boolean; optional):
    If `True`, the popup will open on input focus.

- openText (string; optional):
    Override the default text for the *open popup* icon button.  For
    localization purposes, you can use the provided
    [translations](/guides/localization/).

- placeholder (string; optional)

- popupIcon (boolean | number | string | dict | list; optional):
    The icon to display in place of the default popup icon.

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- resource (string; optional)

- results (number; optional)

- security (string; optional)

- selectOnFocus (boolean; optional):
    If `True`, the input's text is selected on focus. It helps the
    user clear the selected value.

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

- typeof (string; optional)

- unselectable (a value equal to: "on", "off"; optional)

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, clearIcon=Component.UNDEFINED, clearText=Component.UNDEFINED, closeText=Component.UNDEFINED, disabled=Component.UNDEFINED, disablePortal=Component.UNDEFINED, forcePopupIcon=Component.UNDEFINED, fullWidth=Component.UNDEFINED, loading=Component.UNDEFINED, loadingText=Component.UNDEFINED, limitTags=Component.UNDEFINED, noOptionsText=Component.UNDEFINED, openText=Component.UNDEFINED, popupIcon=Component.UNDEFINED, size=Component.UNDEFINED, autoComplete=Component.UNDEFINED, autoHighlight=Component.UNDEFINED, autoSelect=Component.UNDEFINED, blurOnSelect=Component.UNDEFINED, clearOnBlur=Component.UNDEFINED, clearOnEscape=Component.UNDEFINED, componentName=Component.UNDEFINED, disableCloseOnSelect=Component.UNDEFINED, disabledItemsFocusable=Component.UNDEFINED, disableListWrap=Component.UNDEFINED, filterSelectedOptions=Component.UNDEFINED, handleHomeEndKeys=Component.UNDEFINED, id=Component.UNDEFINED, includeInputInList=Component.UNDEFINED, inputValue=Component.UNDEFINED, open=Component.UNDEFINED, openOnFocus=Component.UNDEFINED, selectOnFocus=Component.UNDEFINED, className=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'about', 'accessKey', 'autoCapitalize', 'autoComplete', 'autoCorrect', 'autoHighlight', 'autoSave', 'autoSelect', 'blurOnSelect', 'className', 'classes', 'clearIcon', 'clearOnBlur', 'clearOnEscape', 'clearText', 'closeText', 'color', 'componentName', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableCloseOnSelect', 'disableListWrap', 'disablePortal', 'disabled', 'disabledItemsFocusable', 'draggable', 'filterSelectedOptions', 'forcePopupIcon', 'fullWidth', 'handleHomeEndKeys', 'hidden', 'includeInputInList', 'inlist', 'inputMode', 'inputValue', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'limitTags', 'loading', 'loadingText', 'n_clicks', 'noOptionsText', 'open', 'openOnFocus', 'openText', 'placeholder', 'popupIcon', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'security', 'selectOnFocus', 'size', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab']
        self._type = 'Autocomplete'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'about', 'accessKey', 'autoCapitalize', 'autoComplete', 'autoCorrect', 'autoHighlight', 'autoSave', 'autoSelect', 'blurOnSelect', 'className', 'classes', 'clearIcon', 'clearOnBlur', 'clearOnEscape', 'clearText', 'closeText', 'color', 'componentName', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'disableCloseOnSelect', 'disableListWrap', 'disablePortal', 'disabled', 'disabledItemsFocusable', 'draggable', 'filterSelectedOptions', 'forcePopupIcon', 'fullWidth', 'handleHomeEndKeys', 'hidden', 'includeInputInList', 'inlist', 'inputMode', 'inputValue', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'lang', 'limitTags', 'loading', 'loadingText', 'n_clicks', 'noOptionsText', 'open', 'openOnFocus', 'openText', 'placeholder', 'popupIcon', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'security', 'selectOnFocus', 'size', 'slot', 'spellCheck', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Autocomplete, self).__init__(**args)
