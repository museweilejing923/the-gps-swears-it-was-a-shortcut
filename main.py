#!/usr/bin/env python3
"""GPS excuse writer: validates one fixed line, then saves it.

The navigation voice insists the river crossing was a shortcut, not a
wrong turn. This script only ever writes that one sentence; every rule
below exists to prove the sentence is well formed before it is saved.
Nothing here reads input, touches the network, or looks at the clock.
"""

import sys

ENTRY = "I said shortcut. I did not say road. Technically, the river is the shortest route."
CHAR_LIMIT = 200
DESTINATION = "/output/entry.txt"
TERMINATORS = (".", "!", "?")
MARKS = set(".,!?;:'\"-() ")


def reject(message):
    """Report a failed rule on stderr and stop before writing."""
    print(f"rejected: {message}", file=sys.stderr)
    raise SystemExit(1)


def _present(line):
    return bool(line and line.strip())


def _within_limit(line):
    return len(line) <= CHAR_LIMIT


def _free_of_controls(line):
    return all(ord(ch) >= 32 for ch in line)


def _neatly_spaced(line):
    return line == line.strip() and "  " not in line and "\n" not in line


def _contains_letters(line):
    return any(ch.isalpha() for ch in line)


def _more_than_marks(line):
    return not all(ch in MARKS for ch in line)


def _more_than_digits(line):
    return not line.strip().isdigit()


def _properly_finished(line):
    return line.rstrip().endswith(TERMINATORS)


def _mentions_shortcut(line):
    return "shortcut" in line.lower()


def _no_triple_hyphen(line):
    # Three hyphens in a row read as a stutter, not punctuation.
    return "---" not in line


# Each pair is a human-readable complaint plus the predicate that must
# hold. validate() walks the list top to bottom and stops at the first
# rule that fails, so nothing is ever written half-checked.
CHECKS = [
    ("entry is empty", _present),
    ("entry is longer than the 200 character limit", _within_limit),
    ("entry contains control characters", _free_of_controls),
    ("entry has ragged spacing or a newline", _neatly_spaced),
    ("entry contains no letters", _contains_letters),
    ("entry is punctuation only", _more_than_marks),
    ("entry is digits only", _more_than_digits),
    ("entry does not end with punctuation", _properly_finished),
    ("the GPS excuse must mention a shortcut", _mentions_shortcut),
    ("entry must not contain three hyphens in a row", _no_triple_hyphen),
]


def validate(line):
    for complaint, predicate in CHECKS:
        if not predicate(line):
            reject(complaint)


def run():
    validate(ENTRY)
    with open(DESTINATION, "w", encoding="utf-8") as handle:
        handle.write(ENTRY + "\n")


if __name__ == "__main__":
    run()
