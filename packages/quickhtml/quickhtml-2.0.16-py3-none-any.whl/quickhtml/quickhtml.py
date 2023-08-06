"""This file contains the main program functionality."""

import re

REGEX_BLOCKQUOTE = re.compile(r"""
    \s*         # Match between 0 and ∞ whitespaces.
    (>+)        # CAPTURE GROUP (1) | Match between 1 and ∞ ">".
    \s*         # Match between 0 and ∞ whitespaces.
    ([^>].*?)   # CAPTURE GROUP (2) | Match first character that is not ">",
                # then match between 0 and ∞ characters, as few times as
                # possible.
    \s*         # Match between 0 and ∞ whitespaces.""", re.VERBOSE)

REGEX_BOLD = re.compile(r"""
    (?<!\\)         # Ensure there's no escaping backslash.
    \*{2}           # Match "*" twice.
    ([^\s*].*?)     # CAPTURE GROUP (1) | Match first character that is not "*"
                    # or a whitespace, then match between 0 and ∞ characters,
                    # as few times as possible.
    (?<![\\\s*])    # Ensure there's no escaping backslash, whitespace, or "*".
    \*{2}           # Match "*" twice.
    |               # OR
    (?<!\\)         # Ensure there's no escaping backslash.
    _{2}            # Match "_" twice.
    ([^\s_].*?)     # CAPTURE GROUP (2) | Match first character that is not "_"
                    # or a whitespace, then match between 0 and ∞ characters,
                    # as few times as possible.
    (?<![\\\s_])    # Ensure there's no escaping backslash, whitespace, or "_".
    _{2}            # Match "_" twice.""", re.VERBOSE)

REGEX_CODE = re.compile(r"""
    (?<!\\)     # Ensure there's no escaping backslash.
    (?:         # Open non-capturing group.
        `{2}    # Match "`" twice.
        \s*     # Match between 0 and ∞ whitespaces.
        (.+?)   # CAPTURE GROUP (1) | Match between 1 and ∞ characters, as few
                # times as possible.
        \s*     # Match between 0 and ∞ whitespaces.
        (?<!\\) # Ensure there's no escaping backslash.
        `{2}    # Match "`" twice.
    )           # Close and match non-capturing group.
    |           # OR
    (?:         # Open non-capturing group.
        `       # Match "`" once.
        \s*     # Match between 0 and ∞ whitespaces.
        (.+?)   # CAPTURE GROUP (2) | Match between 1 and ∞ characters, as few
                # times as possible.
        \s*     # Match between 0 and ∞ whitespaces.
        (?<!\\) # Ensure there's no escaping backslash.
        `       # Match "`" once.
    )           # Close and match non-capturing group.
    (?=[^`]|$)  # Make sure there is a line end or a character other than "`"
                # ahead.""", re.VERBOSE)

REGEX_ESCAPED_CHARACTER = re.compile(r"""
    \\  # Match "\" once.
    (.) # CAPTURE GROUP (1) | Match any character once.""", re.VERBOSE)

REGEX_HEADING = re.compile(r"""
    ((?:^|>|-|[0-9]+[.\)])\s*)  # CAPTURE GROUP (1) | Match either line start,
                                # ">", "-", or a number followed by either "."
                                # or ")", then match between 0 and ∞
                                # whitespaces.
    (\#{1,6})                   # CAPTURE GROUP (2) | Match "#" between 1 and 6
                                # times.
    \s+                         # Match between 1 and ∞ whitespaces.
    ([^\s].*?)                  # CAPTURE GROUP (3) | Match first character
                                # that is not a whitespace, then match between
                                # 0 and ∞ characters, as few times as possible.
    (\s*)                       # CAPTURE GROUP (4) | Match between 0 and ∞
                                # whitespaces.
    $                           # Match line end.""", re.VERBOSE)

REGEX_HEADING__ALTERNATIVE_LEVEL_1 = re.compile(r"""
    (.+?)   # CAPTURE GROUP (1) | Match between 1 and ∞ characters, as few
            # times as possible.
    \n      # Match a newline.
    \s*     # Match between 1 and ∞ whitespaces.
    ={2,}   # Match "=" between 2 and ∞ times.
    $       # Match line end.
""", re.VERBOSE | re.MULTILINE)

REGEX_HEADING__ALTERNATIVE_LEVEL_2 = re.compile(r"""
    (.+?)   # CAPTURE GROUP (1) | Match between 1 and ∞ characters, as few
            # times as possible.
    \n      # Match a newline.
    \s*     # Match between 1 and ∞ whitespaces.
    -{2,}   # Match "-" between 2 and ∞ times.
    $       # Match line end.
""", re.VERBOSE | re.MULTILINE)

REGEX_HORIZONTAL_RULE = re.compile(r"""
    ^               # Match line start.
    \s*             # Match between 0 and ∞ whitespaces.
    (?:\*|-|_){3,}  # Match either "*", "-" or "_", at least 3 times.
    \s*             # Match between 0 and ∞ whitespaces.
    $               # Match line end.""", re.VERBOSE)

REGEX_IMAGE = re.compile(r"""
    (?<!\\)     # Ensure there's no escaping backslash.
    !           # Match "!" once.
    \[          # Match "[" once.
    \s*         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP (2) | Match between 1 and ∞ characters, as few
                # times as possible.
    \s*         # Match between 0 and ∞ whitespaces.
    \]          # Match "]" once.
    \(          # Match "(" once.
    \s*         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP (3) | Match between 1 and ∞ characters, as few
                # times as possible.
    \s*         # Match between 0 and ∞ whitespaces.
    (?:         # Open non-capturing group.
        [\"']   # Match either "'" or '"' once.
        \s*     # Match between 0 and ∞ whitespaces.
        (.+?)   # CAPTURE GROUP (4) | Match between 1 and ∞ characters, as few
                # times as possible.
        \s*     # Match between 0 and ∞ whitespaces.
        [\"']   # Match either "'" or '"' once.
    )?          # Close non-capturing group and match it either 0 or 1 times.
    \s*         # Match between 0 and ∞ whitespaces.
    \)          # Match ")" once.""", re.VERBOSE)

REGEX_ITALIC = re.compile(r"""
    (?<!\\)         # Ensure there's no escaping backslash.
    \*              # Match "*" once.
    ([^\s*].*?)     # CAPTURE GROUP (1) | Match first character that is not "*"
                    # or a whitespace, then match between 0 and ∞ characters,
                    # as few times as possible.
    (?<![\\\s*])    # Ensure there's no escaping backslash, whitespace, or "*".
    \*              # Match "*" once.
    |               # OR
    (?<!\\)         # Ensure there's no escaping backslash.
    _               # Match "_" once.
    ([^\s_].*?)     # CAPTURE GROUP (2) | Match first character that is not "_"
                    # or a whitespace, then match between 0 and ∞ characters,
                    # as few times as possible.
    (?<![\\\s_])    # Ensure there's no escaping backslash, whitespace, or "_".
    _               # Match "_" once.""", re.VERBOSE)

REGEX_LINK = re.compile(r"""
    (?<!\\)     # Ensure there's no escaping backslash.
    \[          # Match "[" once.
    \s*         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP (1) | Match between 1 and ∞ characters, as few
                # times as possible.
    \s*         # Match between 0 and ∞ whitespaces.
    \]          # Match "]" once.
    \(          # Match "(" once.
    \s*         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP (2) | Match between 1 and ∞ characters, as few
                # times as possible.
    \s*         # Match between 0 and ∞ whitespaces.
    (?:         # Open non-capturing group.
        [\"']   # Match either "'" or '"' once.
        \s*     # Match between 0 and ∞ whitespaces.
        (.+?)   # CAPTURE GROUP (3) | Match between 1 and ∞ characters, as few
                # times as possible.
        \s*     # Match between 0 and ∞ whitespaces.
        [\"']   # Match either "'" or '"' once.
    )?          # Close non-capturing group and match it either 0 or 1 times.
    \s*         # Match between 0 and ∞ whitespaces.
    \)          # Match ")" once.""", re.VERBOSE)

REGEX_REFERENCE_DEFINITION = re.compile(r"""
    ^           # Match line start.
    (?<!\\)     # Ensure there's no escaping backslash.
    \s*         # Match between 0 and ∞ whitespaces.
    \[          # Match "[" once.
    \s*         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP (1) | Match between 1 and ∞ characters, as few
                # times as possible.
    \s*         # Match between 0 and ∞ whitespaces.
    \]          # Match "]" once.
    \s*         # Match between 0 and ∞ whitespaces.
    :           # Match ":" once.
    \s*         # Match between 0 and ∞ whitespaces.
    <?          # Match "<" either 0 or 1 times.
    \s*         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP (2) | Match between 1 and ∞ characters, as few
                # times as possible.
    \s*         # Match between 0 and ∞ whitespaces.
    >?          # Match ">" either 0 or 1 times.
    \s*         # Match between 0 and ∞ whitespaces.
    (?:         # Open non-capturing group.
        [\"'(]  # Match '"', "'", or "(" once.
        \s*     # Match between 0 and ∞ whitespaces.
        (.+?)   # CAPTURE GROUP (3) | Match between 1 and ∞ characters, as few
                # times as possible.
        \s*     # Match between 0 and ∞ whitespaces.
        [\"')]  # Match '"', "'", or ")" once.
    )?          # Close non-capturing group and match it either 0 or 1 times.
    \s*         # Match between 0 and ∞ whitespaces.
    $           # Match line end.""", re.VERBOSE | re.MULTILINE)

REGEX_REFERENCE_LINK = re.compile(r"""
    (?<!\\)     # Ensure there's no escaping backslash.
    \[          # Match "[" once.
    \s*         # Match between 0 and ∞ whitespaces.
    (.+?)       # CAPTURE GROUP (1) | Match between 1 and ∞ characters, as few
                # times as possible.
    \s*         # Match between 0 and ∞ whitespaces.
    \]          # Match "]" once.
    \s*         # Match between 0 and ∞ whitespaces.
    (?:         # Open non-capturing group.
        \[      # Match "[" once.
        \s*     # Match between 0 and ∞ whitespaces.
        (.+?)   # CAPTURE GROUP (2) | Match between 1 and ∞ characters, as few
                # times as possible.
        \s*     # Match between 0 and ∞ whitespaces.
        \]      # Match "]" once.
    )?          # Close non-capturing group and match it either 0 or 1
                # times.""", re.VERBOSE)

REGEX_ORDERED_LIST = re.compile(r"""
    (\s+)?  # CAPTURE GROUP (1) | Match between 1 and ∞ whitespaces, as many
            # times as possible, as either one or zero matches.
    [0-9]+  # Match between 1 and ∞ numbers.
    [.)]    # Match either "." or ")" once.
    \s+     # Match between 1 and ∞ whitespaces.
    (.+?)   # CAPTURE GROUP (2) | Match between 1 and ∞ characters, as few
            # times as possible.
    \s*     # Match between 0 and ∞ whitespaces.""", re.VERBOSE)

REGEX_QUICK_EMAIL = re.compile(r"""
    (?<!\\)         # Ensure there's no escaping backslash.
    <               # Match "<" once.
    (               # CAPTURE GROUP (1) | Open capture group.
        [\w\d_.+-]+ # Match either a word character, a digit, "_", ".", "+", or
                    # "-", between 1 and ∞ times.
        @           # Match "@" once.
        [\w\d-]+    # Match either a word character, a digit, or "-", between 1
                    # and ∞ times.
        \.          # Match "." once.
        [\w\d.-]+   # Match either a word character, a digit, ".", or "-",
                    # between 1 and ∞ times.
    )               # CAPTURE GROUP (1) | Close and match capture group.
    >               # Match ">" once.""", re.VERBOSE)

REGEX_QUICK_LINK = re.compile(r"""
    (?<!\\)                 # Ensure there's no escaping backslash.
    <                       # Match "<" once.
    (                       # CAPTURE GROUP (1) | Open capture group.
        https?              # Match either "http" or "https".
        ://                 # Match "://" once.
        (?:                 # Open non-capturing group.
            -               # Match "-" once.
            \.              # Match "." once.
        )?                  # Close non-capturing group and match it either 0
                            # or 1 times.
        (?:                 # Open non-capturing group.
            [^\s/?.#->]+    # Match any character that is not a whitespace,
                            # "/", "?", ".", "#", or "-", between 1 and ∞
                            # times.
            \.?             # Match ".", either 0 or 1 times.
        )+                  # Close non-capturing group and match it between 1
                            # and ∞ times.
        (?:                 # Open non-capturing group.
            /               # Match "/" once.
            [^\s]*          # Match any character that is not a whitespace,
                            # between 0 and ∞ times.
        )?                  # Close non-capturing group and match it either 0
                            # or 1 times.
    )                       # CAPTURE GROUP (1) | Close and match capture
                            # group.
    >                       # Match ">" once.""", re.VERBOSE)

REGEX_UNORDERED_LIST = re.compile(r"""
    (\s+)?  # CAPTURE GROUP (1) | Match between 1 and ∞ whitespaces, as many
            # times as possible, as either one or zero matches.
    [-*+]+  # Match between 1 and ∞ "-", "*", or "+".
    \s+     # Match between 1 and ∞ whitespaces.
    (.+?)   # CAPTURE GROUP (2) | Match between 1 and ∞ characters, as few
            # times as possible.
    \s*     # Match between 0 and ∞ whitespaces.""", re.VERBOSE)

NESTED_TAGS = (
    {
        "regex": REGEX_BLOCKQUOTE,
        "outer_opening_tag": "<blockquote>",
        "outer_closing_tag": "</blockquote>",
        "inner_opening_tag": "<p>",
        "inner_closing_tag": "</p>",
        "minimum_level": 1
    },
    {
        "regex": REGEX_ORDERED_LIST,
        "outer_opening_tag": "<ol>",
        "outer_closing_tag": "</ol>",
        "inner_opening_tag": "<li>",
        "inner_closing_tag": "</li>",
        "minimum_level": 0
    },
    {
        "regex": REGEX_UNORDERED_LIST,
        "outer_opening_tag": "<ul>",
        "outer_closing_tag": "</ul>",
        "inner_opening_tag": "<li>",
        "inner_closing_tag": "</li>",
        "minimum_level": 0
    }
)


def check_paragraph(line):
    """
    Check whether or not a line should be enclosed in paragraph tags.

    Args:
        line (str): Line to check.

    Returns:
        bool: Whether or not the line should be enclosed in paragraph tags.
    """
    line = line.strip()

    # A paragraph can start with a "<br>", but not just be a "<br>".
    if line in ("", "<br>", "<hr>"):
        return False

    # Tags that do not need be enclosed in <p> tags:
    INDEPENDENT_TAG_REGEXES = [
        r"""<h[1-6]>.+<\/h[1-6]>""",
        r"""<a\s+href="[^"]+?"\s*(?:\s*title="[^"]+?")?>.+?<\/a>""",
        r"""<img\s+src="[^"]+?"\s*alt="[^"]+?"(?:\s*title="[^"]+?")?>""",
        r"""<code>.+</code>""",
        r"""<blockquote>.+""",
        r"""<ol>.+""",
        r"""<ul>.+""",
        r"""<pre><code>.+""",
    ]

    for regex in INDEPENDENT_TAG_REGEXES:
        line = re.sub(regex, "", line)

    return False if line == "" else True


def convert_nested_tag(line, cur_tag, open_tags):
    """
    Convert one or more nested tags in a line.

    Conversion is based on the level of the last tag open, opening a new tag if
    the current level is greater than the last, and closing the last tag if the
    current level is lesser than the last.

    E.g.:
        > Quote Level 1
        Becomes:
        <blockquote>
            <p>Quote Level 1</p>

        > Quote Level 1
        >> Quote Level 2
        > Quote Level 1
        Becomes (after function runs on the three lines):
        <blockquote>
            <p>Quote Level 1</p>
            <blockquote>
                <p>Quote Level 2</p>
            </blockquote>
            <p>Quote Level 1</p>

        > Quote Level 1
        >> Quote Level 2
        >>> Quote Level 3
        >>>> Quote Level 4
        Becomes (after function runs on the four lines):
        <blockquote>
            <p>Quote Level 1</p>
            <blockquote>
                <p>Quote Level 2</p>
                <blockquote>
                    <p>Quote Level 3</p>
                    <blockquote>
                        <p>Quote Level 4</p>

    Args:
        line (str): Line to convert.
        cur_tag (dict[str, Any]): Dictionary containing data about type of tag
            used in conversion.
        open_tags (list[tuple[dict[str, Any], int]]): A list of tuples which
            represent tags left open, where each tuple contains a dictionary
            representing a tag, and its respective level.
    Returns:
        new_line (str) : Converted line.
    """
    def inner_tags(string, tag):
        """
        Add opening and closing inner tags to a string, if required.

        If the inner tags are paragraphs, it will then be decided whether or
        not the string has to be enclosed in paragraph tags. Otherwise, it is
        enclosed in the inner tags. For example, lists within blockquotes
        should not be enclosed in paragraph tags.

        Args:
            string (str): String to add tags to.
            tag (tuple[dict[str, Any]]): A dictionary representing a tag.

        Returns:
            string: Resulting string.
        """
        if tag["inner_opening_tag"] == "<p>":
            return f"<p>{string}</p>" if check_paragraph(string) else string

        return "".join((
            tag["inner_opening_tag"],
            string,
            tag["inner_closing_tag"]
        ))

    def convert_inline(string):
        """
        Recursively convert nested tags present in a string.

        This function should only be used to convert nested tags present in the
        content of another nested tag. That is, it is only useful for nested
        tags which are on the same line as an initially matched main tag, since
        it does not account for levels.

        E.g.:
            "1. - Unordered list inside an ordered list."
            Becomes:
            <ol>
                <li>
                    <ul>
                        <li>Unordered list inside an ordered list.</li>
                    </ul>
                </li>
            </ol>

        Args:
            string (str): String to convert.

        Returns:
            string: Converted string.
        """
        for tag in NESTED_TAGS:
            match = tag["regex"].fullmatch(string)
            if match:
                content = match[2]
                string = "".join((
                    tag["outer_opening_tag"],
                    inner_tags(convert_inline(content.strip()), tag),
                    tag["outer_closing_tag"]
                ))
        return string

    new_line = ""
    match = cur_tag["regex"].fullmatch(line)

    try:
        last_tag = open_tags[-1][0]
        last_tag_level = open_tags[-1][1]
    except IndexError:
        last_tag_level = 0
    try:
        # 1 is added to ensure level is never less than 1. This prevents
        # inconsistent behavior from arising due to lists minimum level being
        # zero, and blockquotes minimum level being 1. This mainly addresses
        # inconsistencies when tags are used separately.
        cur_tag_level = len(match[1]) + 1
    except TypeError:
        cur_tag_level = 1

    # Tag minimum level is removed from the current level due to the same
    # reason as above. This mainly addresses inconsistencies when tags are
    # mixed.
    cur_tag_level -= cur_tag["minimum_level"]

    content = convert_inline(match[2])

    # If current level is greater than last level, open a new tag, then append
    # tag and level to the list of open tags.
    if cur_tag_level > last_tag_level:
        new_line = "".join((
            cur_tag["outer_opening_tag"],
            inner_tags(content, cur_tag)
        ))
        open_tags.append((cur_tag, cur_tag_level))

    # If current level is lesser than last level:
    elif cur_tag_level < last_tag_level:
        # If none of the open tags have a level equal to or lesser than current
        # level, close the last tag, remove it from the list of open tags, open
        # a new tag, and add it to the list of open tags. This is checked
        # mainly to account for edge cases.
        if not any(open_tag[1] <= cur_tag_level for open_tag in open_tags):
            new_line = "".join((
                last_tag["outer_closing_tag"],
                cur_tag["outer_opening_tag"],
                inner_tags(content, cur_tag)
            ))
            open_tags.remove(open_tags[-1])
            open_tags.append((cur_tag, cur_tag_level))
        else:
            # Go through open tags, closing them until a tag's level is equal
            # to or lesser than current level.
            for open_tag in reversed(open_tags):
                tag, level = open_tag
                if level > cur_tag_level:
                    new_line += tag["outer_closing_tag"]
                    open_tags.remove(open_tag)
                else:
                    # If this tag is the same type as current tag, open inner
                    # tags only.
                    if tag == cur_tag:
                        new_line += inner_tags(content, cur_tag)

                    # If not, then close it, remove it from the list of open
                    # tags, open a new tag and add it to the list of open tags.
                    else:
                        new_line += "".join((
                            tag["outer_closing_tag"],
                            cur_tag["outer_opening_tag"],
                            inner_tags(content, cur_tag)
                        ))
                        open_tags.remove(open_tag)
                        open_tags.append((cur_tag, cur_tag_level))
                    break

    # If current level is the same as last level:
    else:
        # If last tag is the same type as current tag, open inner tags only.
        if last_tag == cur_tag:
            new_line = inner_tags(content, cur_tag)

        # If not, then close it, remove it from the list of open tags, open a
        # new tag, and add it to the list of open tags.
        else:
            new_line = "".join((
                last_tag["outer_closing_tag"],
                cur_tag["outer_opening_tag"],
                inner_tags(content, cur_tag)
            ))
            open_tags.remove(open_tags[-1])
            open_tags.append((cur_tag, cur_tag_level))

    return new_line


def add_inline_tags(line, references):
    """
    Add inline tags, such as <em> and <strong>, to a line.

    Args:
        line (str): Line to add tags to.
        references (List[Dict]): A list of dictionaries, each containing
            information about a reference-style link definition.

    Returns:
        line (str): Converted line.
    """
    # Add emphasis.
    # The order here is important, otherwise "**bold**" would be converted to
    # "*<em>bold</em>*", instead of "<strong>bold</strong>".
    line = REGEX_BOLD.sub("<strong>\\1\\2</strong>", line)
    line = REGEX_ITALIC.sub("<em>\\1\\2</em>", line)

    # Add images and links.
    # The order here is important, otherwise images wouldn't work.
    if REGEX_IMAGE.search(line):
        matches = REGEX_LINK.findall(line)
        for match in matches:
            alt_text, url, title = match
            line = REGEX_IMAGE.sub(
                f'<img src="{url}" alt="{alt_text}"'
                + (f' title="{title}"' if title else '')
                + '>', line, 1)
    if REGEX_LINK.search(line):
        matches = REGEX_LINK.findall(line)
        for match in matches:
            text, url, title = match
            line = REGEX_LINK.sub(
                f'<a href="{url}"'
                + (f' title="{title}"' if title else '')
                + f'>{text}</a>', line, 1)

    # Add reference-style links.
    if references:
        matches = REGEX_REFERENCE_LINK.findall(line)
        for match in matches:
            text, label = match
            if not label:
                label = text
            for reference in references:
                if label == reference["label"]:
                    label, url, title = reference.values()
                    line = REGEX_REFERENCE_LINK.sub(
                        f'<a href="{url}"'
                        + (f' title="{title}"' if title else '')
                        + f'>{text if text else label}</a>', line, 1)
                    break

    # Add quick links.
    if REGEX_QUICK_LINK.search(line):
        line = REGEX_QUICK_LINK.sub("<a href=\"\\1\">\\1</a>", line)

    # Add quick links to email addresses.
    if REGEX_QUICK_EMAIL.search(line):
        line = REGEX_QUICK_EMAIL.sub("<a href=\"mailto:\\1\">\\1</a>", line)
    return line


def convert(string):
    """
    Convert Markdown into HTML.

    Args:
        string (str): Markdown code to be converted.

    Returns:
        new_string (str): HTML code.
    """
    # Store reference-style link definitions.
    keys = ("label", "url", "title")
    references = [
        dict(zip(keys, i)) for i in REGEX_REFERENCE_DEFINITION.findall(string)]
    string = REGEX_REFERENCE_DEFINITION.sub("", string)

    if string.strip() == "":
        return ""

    # Convert alternate-style headings to conventional style.
    string = REGEX_HEADING__ALTERNATIVE_LEVEL_1.sub("# \\1", string)
    string = REGEX_HEADING__ALTERNATIVE_LEVEL_2.sub("## \\1", string)

    open_tags = []
    new_string = ""
    add_line_break = False
    open_paragraph = False
    open_code_block = False

    def convert_paragraph(line):
        """
        Convert a line into a paragraph.

        Args:
            line (str): Line to convert.

        Returns:
            str: Converted line.
        """
        line = f"{line.strip()} "
        nonlocal open_paragraph
        if not open_paragraph:
            open_paragraph = True
            return f"<p>{line}"
        return line

    # Ensure string ends with a newline to prevent inconsistencies.
    while string.splitlines()[-1] != "":
        string += "\n"

    for line in string.splitlines():
        # Ensure line made out of only whitespaces is an empty string, as to
        # prevent inconsistencies.
        if line.strip() == "":
            line = ""

        new_line = ""

        # Add horizontal rules.
        line = REGEX_HORIZONTAL_RULE.sub("<hr>", line)

        # Add code blocks.
        if line.startswith("    ") and not open_tags:
            # If a code block is already open, a newline should be added, as to
            # ensure text is formatted as it was in the input string.
            new_line += "<pre><code>" if not open_code_block else "\n"

            # 4 characters are removed from the start of the line to account
            # for spaces used to denote a code block.
            new_line += line[4:]
            open_code_block = True
        elif open_code_block:
            new_line = "</code></pre>"
            open_code_block = False

        # Convert string only if a code block is not open.
        if not open_code_block:
            # Add headings.
            if REGEX_HEADING.search(line):
                level = len(REGEX_HEADING.search(line)[2])
                line = REGEX_HEADING.sub(
                    f"\\1<h{level}>\\3</h{level}>\\4", line)

            # Store information about code snippets.
            code_snippets = []
            if REGEX_CODE.search(line):
                matches = ("".join(i or "") for i in REGEX_CODE.findall(line))
                right = REGEX_CODE.sub("\\1\\2", line)
                for match in matches:
                    left, right = right.split(match, 1)
                    code_snippets.append(
                        {"left": left, "content": match, "right": right})

            # Add code snippets and inline tags.
            if code_snippets:
                line = ""
                for block in code_snippets:
                    left = add_inline_tags(block["left"], references)
                    line += left + f"<code>{block['content']}</code>"
                    if block == code_snippets[-1]:
                        line += add_inline_tags(block["right"], references)
            else:
                line = add_inline_tags(line, references)

            # Check if line contains nested tags, if so, open tags.
            if any(tag["regex"].fullmatch(line) for tag in NESTED_TAGS):
                for tag in NESTED_TAGS:
                    if tag["regex"].fullmatch(line):
                        new_line += convert_nested_tag(line, tag, open_tags)

            # If not, check if there are open tags, if so, close them. After
            # doing so, check whether the line is a paragraph and add it
            # accordingly.
            elif open_tags:
                for tag in reversed(open_tags):
                    new_line += tag[0]["outer_closing_tag"]
                    open_tags.remove(tag)
                if check_paragraph(line):
                    new_line += convert_paragraph(line)
                else:
                    new_line += line

            # If not, check if line is a paragraph, if so, open a paragraph.
            elif check_paragraph(line):
                new_line += convert_paragraph(line)

            # If not, just add the line as it is.
            else:
                new_line += line

            # Escape characters.
            if REGEX_ESCAPED_CHARACTER.search(new_line):
                new_line = REGEX_ESCAPED_CHARACTER.sub("\\1", new_line)

            # Add line breaks.
            if add_line_break:
                new_line = f"<br>{new_line}"
                add_line_break = False

            # Check if a line break should be added.
            if line.lstrip().endswith("  "):
                new_line = new_line.rstrip()
                add_line_break = True

        # Close paragraph.
        if open_paragraph and not check_paragraph(new_line):
            open_paragraph = False
            new_string = new_string.rstrip()
            new_line = f"</p>{new_line}"

        new_string += new_line
    return new_string.strip()


def convert_file(file):
    """
    Open a Markdown file and return converted results.

    Args:
        file (TextIO): Markdown file to be converted.

    Returns:
        str: HTML code.
    """
    with open(file) as f:
        return convert(f.read())
