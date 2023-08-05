# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashLatex(Component):
    """A DashLatex component.
DashLatex is a Dash wrapper for ReactLatex (https://github.com/zzish/react-latex) which is itself a wrapper for Katex (https://katex.org/docs/options.html).

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    React element to be rendered inside the GSK Button component.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- displayMode (boolean; optional):
    displayMode: boolean (default: False). If True the math will be
    rendered in display mode. If False the math will be rendered in
    inline mode. Differences between the two modes include: Display
    mode starts in \\displaystyle, so \\int and \\sum are large, for
    example; while inline mode starts in \\textstyle, where subscripts
    and superscripts usually don't stack on top of operators like
    \\sum. You can always manually switch between \\displaystyle and
    \\textstyle using those commands. Display mode centers math on its
    on line and disables automatic line breaking (though you can
    customize this behavior with custom CSS). In inline mode, KaTeX
    allows line breaks after outermost relations (like = or <) or
    binary operators (like + or \\times), the same as TeX.

- errorColor (string; optional):
    errorColor: string. A color string given in the format \"#XXX\" or
    \"#XXXXXX\". This option determines the color that unsupported
    commands and invalid LaTeX are rendered in when throwOnError is
    set to False. (default: #cc0000).

- fleqn (boolean; optional):
    fleqn: boolean. If True, display math renders flush left with a
    2em left margin, like \\documentclass[fleqn] in LaTeX with the
    amsmath package.

- globalGroup (boolean; optional):
    globalGroup: boolean (default: False). Place KaTeX code in the
    global group. As a consequence, \\def and \\newcommand persist in
    macros across render calls. In LaTeX, constructs such as
    \\begin{equation} and $$ create a local group and prevent
    definitions from becoming visible outside of those blocks.

- leqno (boolean; optional):
    leqno: boolean. If True, display math has \\tags rendered on the
    left instead of the right, like \\usepackage[leqno]{amsmath} in
    LaTeX.

- macros (dict; optional):
    macros: object. A collection of custom macros. Each macro is a
    property with a name like \\name (written \"\\\\name\" in
    JavaScript) which maps to a string that describes the expansion of
    the macro, or a function that accepts an instance of MacroExpander
    as first argument and returns the expansion as a string.
    MacroExpander is an internal API and subject to non-backwards
    compatible changes. See src/macros.js for its usage.
    Single-character keys can also be included in which case the
    character will be redefined as the given macro (similar to TeX
    active characters). This object will be modified if the LaTeX code
    defines its own macros via \\gdef, which enables consecutive calls
    to KaTeX to share state.

- maxExpand (number; optional):
    maxExpand: number. Limit the number of macro expansions to the
    specified number, to prevent e.g. infinite macro loops. If set to
    Infinity, the macro expander will try to fully expand as in LaTeX.
    (default: 1000).

- maxSize (number; optional):
    maxSize: number. All user-specified sizes, e.g. in
    \\rule{500em}{500em}, will be capped to maxSize ems. If set to
    Infinity (the default), users can make elements and spaces
    arbitrarily large.

- minRuleThickness (number; optional):
    minRuleThickness: number. Specifies a minimum thickness, in ems,
    for fraction lines, \\sqrt top lines, {array} vertical lines,
    \\hline, \\hdashline, \\underline, \\overline, and the borders of
    \\fbox, \\boxed, and \\fcolorbox. The usual value for these items
    is 0.04, so for minRuleThickness to be effective it should
    probably take a value slightly above 0.04, say 0.05 or 0.06.
    Negative values will be ignored.

- strict (boolean | string; optional):
    strict: boolean or string or function (default: \"warn\"). If
    False or \"ignore\", allow features that make writing LaTeX
    convenient but are not actually supported by (Xe)LaTeX (similar to
    MathJax). If True or \"error\" (LaTeX faithfulness mode), throw an
    error for any such transgressions. If \"warn\" (the default), warn
    about such behavior via console.warn. Provide a custom function
    handler(errorCode, errorMsg, token) to customize behavior
    depending on the type of transgression (summarized by the string
    code errorCode and detailed in errorMsg); this function can also
    return \"ignore\", \"error\", or \"warn\" to use a built-in
    behavior. A list of such features and their errorCodes:.

- throwOnError (boolean; optional):
    throwOnError: boolean. If True (the default), KaTeX will throw a
    ParseError when it encounters an unsupported command or invalid
    LaTeX. If False, KaTeX will render unsupported commands as text,
    and render invalid LaTeX as its source code with hover text giving
    the error, in the color given by errorColor."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, displayMode=Component.UNDEFINED, leqno=Component.UNDEFINED, fleqn=Component.UNDEFINED, throwOnError=Component.UNDEFINED, errorColor=Component.UNDEFINED, macros=Component.UNDEFINED, minRuleThickness=Component.UNDEFINED, maxSize=Component.UNDEFINED, maxExpand=Component.UNDEFINED, strict=Component.UNDEFINED, globalGroup=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'displayMode', 'errorColor', 'fleqn', 'globalGroup', 'leqno', 'macros', 'maxExpand', 'maxSize', 'minRuleThickness', 'strict', 'throwOnError']
        self._type = 'DashLatex'
        self._namespace = 'dash_latex'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'displayMode', 'errorColor', 'fleqn', 'globalGroup', 'leqno', 'macros', 'maxExpand', 'maxSize', 'minRuleThickness', 'strict', 'throwOnError']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashLatex, self).__init__(children=children, **args)
