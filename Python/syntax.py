from PyQt6 import QtCore, QtGui

def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QtGui.QColor()
    if isinstance(color, str):
        _color.setNamedColor(color)
    else:
        _color.setRgb(color)

    _format = QtGui.QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QtGui.QFont.Weight.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
DARK_STYLES = {
    # 'keyword': format('steelblue'),
    'keyword': format(0x569CD6),
    'operator': format('coral'),
    'brace': format('darkGray'),
    'defclass': format(0x4EC9B0),
    'string': format('darksalmon'),
    'string2': format('darksalmon'),
    'comment': format(0x57A64A),
    'self': format('steelblue'),
    'numbers': format('beige'),
}
LIGHT_STYLES = {
    'keyword': format('blue'),
    'operator': format('red'),
    'brace': format('darkGray'),
    'defclass': format('black'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen'),
    'self': format('blue'),
    'numbers': format('brown'),
}

class PythonHighlighter (QtGui.QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'and', 'assert', 'as', 'async', 'await', 'break', 'case', 'class', 'continue', 'def',
        'default', 'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in', 'input',
        'is', 'lambda', 'match', 'nonlocal', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'with', 'yield',
        'None', 'True', 'False',
    ]

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\\+', '-', '\\*', '/', '//', '\\%', '\\*\\*',
        # In-place
        '\\+=', '-=', '\\*=', '/=', '\\%=',
        # Bitwise
        '\\^', '\\|', '\\&', '\\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\\{', '\\}', '\\(', '\\)', '\\[', '\\]',
    ]

    def __init__(self, parent: QtGui.QTextDocument) -> None:
        super().__init__(parent)
        is_darkMode = QtGui.QPalette().color(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText).lightness() > 128
        STYLES = DARK_STYLES if is_darkMode else LIGHT_STYLES
        # Multi-line strings (expression, flag, style)
        self.tri_single = (QtCore.QRegularExpression("'''"), 1, STYLES['string2'])
        self.tri_double = (QtCore.QRegularExpression('"""'), 2, STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
            for w in PythonHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
            for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
            for b in PythonHighlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QtCore.QRegularExpression(pat), index, fmt)
            for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        self.tripleQuoutesWithinStrings = []
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            match = expression.match(text)
            if match.hasMatch():
                index = match.capturedStart()
            # index = expression.indexIn(text, 0)
            # if index >= 0:
                # if there is a string we check
                # if there are some triple quotes within the string
                # they will be ignored if they are matched again
                if expression.pattern() in [r'"[^"\\]*(\\.[^"\\]*)*"', r"'[^'\\]*(\\.[^'\\]*)*'"]:
                    innerMatch = self.tri_single[0].match(text, index + 1)
                    if not innerMatch.hasMatch():
                        innerMatch = self.tri_double[0].match(text, index + 1)

                    if innerMatch.hasMatch():
                        innerIndex = innerMatch.capturedStart()
                        tripleQuoteIndexes = range(innerIndex, innerIndex + 3)
                        self.tripleQuoutesWithinStrings.extend(tripleQuoteIndexes)

            # while index >= 0:
            while match.hasMatch():
                index = match.capturedStart()
                # skipping triple quotes within strings
                if index in self.tripleQuoutesWithinStrings:
                    index += 1
                    match = expression.match(text, index)
                    continue

                # We actually want the index of the nth match
                index = match.capturedStart(nth)
                length = match.capturedLength(nth)
                self.setFormat(index, length, format)
                match = expression.match(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start_match = delimiter.match(text)
            start = start_match.capturedStart()
            # skipping triple quotes within strings
            if start in self.tripleQuoutesWithinStrings:
                return False
            # Move past this match
            add = start_match.capturedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end_match = delimiter.match(text, start + add)
            end = end_match.capturedStart()
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + end_match.capturedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start_match = delimiter.match(text, start + length)
            start = start_match.capturedStart()

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        return False
