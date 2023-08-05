# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MobileStepper(Component):
    """A MobileStepper component.
Material-UI MobileStepper.

Keyword arguments:

- id (string; optional)

- about (string; optional)

- accessKey (string; optional)

- activeStep (number; optional):
    Set the active step (zero based index). Defines which dot is
    highlighted when the variant is 'dots'.

- autoCapitalize (string; optional)

- autoCorrect (string; optional)

- autoSave (string; optional)

- backButton (boolean | number | string | dict | list; optional):
    A back button element. For instance, it can be a `Button` or an
    `IconButton`.

- className (string; optional)

- classes (dict; optional):
    Override or extend the styles applied to the component.

- color (string; optional)

- contentEditable (a value equal to: false, true, "true", "false", "inherit"; optional)

- contextMenu (string; optional)

- datatype (string; optional)

- defaultChecked (boolean; optional)

- dir (string; optional)

- draggable (a value equal to: false, true, "true", "false"; optional)

- elevation (number; optional):
    Shadow depth, corresponds to `dp` in the spec. It accepts values
    between 0 and 24 inclusive.

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

- key (string | number; optional)

- lang (string; optional)

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- nextButton (boolean | number | string | dict | list; optional):
    A next button element. For instance, it can be a `Button` or an
    `IconButton`.

- placeholder (string; optional)

- position (a value equal to: "bottom", "top", "static"; optional):
    Set the positioning type.

- prefix (string; optional)

- property (string; optional)

- radioGroup (string; optional)

- resource (string; optional)

- results (number; optional)

- security (string; optional)

- slot (string; optional)

- spellCheck (a value equal to: false, true, "true", "false"; optional)

- square (boolean; optional):
    If `True`, rounded corners are disabled.

- steps (number; optional):
    The total steps.

- style (dict; optional)

- suppressContentEditableWarning (boolean; optional)

- suppressHydrationWarning (boolean; optional)

- tabIndex (number; optional)

- title (string; optional)

- translate (a value equal to: "yes", "no"; optional)

- typeof (string; optional)

- unselectable (a value equal to: "on", "off"; optional)

- variant (a value equal to: "progress", "text", "dots"; optional):
    The variant to use.

- vocab (string; optional)"""
    @_explicitize_args
    def __init__(self, activeStep=Component.UNDEFINED, backButton=Component.UNDEFINED, nextButton=Component.UNDEFINED, position=Component.UNDEFINED, steps=Component.UNDEFINED, variant=Component.UNDEFINED, className=Component.UNDEFINED, elevation=Component.UNDEFINED, square=Component.UNDEFINED, slot=Component.UNDEFINED, title=Component.UNDEFINED, key=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, suppressContentEditableWarning=Component.UNDEFINED, suppressHydrationWarning=Component.UNDEFINED, accessKey=Component.UNDEFINED, contentEditable=Component.UNDEFINED, contextMenu=Component.UNDEFINED, dir=Component.UNDEFINED, draggable=Component.UNDEFINED, hidden=Component.UNDEFINED, id=Component.UNDEFINED, lang=Component.UNDEFINED, placeholder=Component.UNDEFINED, spellCheck=Component.UNDEFINED, tabIndex=Component.UNDEFINED, translate=Component.UNDEFINED, radioGroup=Component.UNDEFINED, about=Component.UNDEFINED, datatype=Component.UNDEFINED, inlist=Component.UNDEFINED, prefix=Component.UNDEFINED, property=Component.UNDEFINED, resource=Component.UNDEFINED, typeof=Component.UNDEFINED, vocab=Component.UNDEFINED, autoCapitalize=Component.UNDEFINED, autoCorrect=Component.UNDEFINED, autoSave=Component.UNDEFINED, color=Component.UNDEFINED, itemProp=Component.UNDEFINED, itemScope=Component.UNDEFINED, itemType=Component.UNDEFINED, itemID=Component.UNDEFINED, itemRef=Component.UNDEFINED, results=Component.UNDEFINED, security=Component.UNDEFINED, unselectable=Component.UNDEFINED, inputMode=Component.UNDEFINED, classes=Component.UNDEFINED, style=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'about', 'accessKey', 'activeStep', 'autoCapitalize', 'autoCorrect', 'autoSave', 'backButton', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'draggable', 'elevation', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'n_clicks', 'nextButton', 'placeholder', 'position', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'security', 'slot', 'spellCheck', 'square', 'steps', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'variant', 'vocab']
        self._type = 'MobileStepper'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'about', 'accessKey', 'activeStep', 'autoCapitalize', 'autoCorrect', 'autoSave', 'backButton', 'className', 'classes', 'color', 'contentEditable', 'contextMenu', 'datatype', 'defaultChecked', 'dir', 'draggable', 'elevation', 'hidden', 'inlist', 'inputMode', 'is', 'itemID', 'itemProp', 'itemRef', 'itemScope', 'itemType', 'key', 'lang', 'n_clicks', 'nextButton', 'placeholder', 'position', 'prefix', 'property', 'radioGroup', 'resource', 'results', 'security', 'slot', 'spellCheck', 'square', 'steps', 'style', 'suppressContentEditableWarning', 'suppressHydrationWarning', 'tabIndex', 'title', 'translate', 'typeof', 'unselectable', 'variant', 'vocab']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(MobileStepper, self).__init__(**args)
