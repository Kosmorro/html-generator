#!/usr/bin/env python3

from doctest import testmod, NORMALIZE_WHITESPACE
import kosmorro_pdf_generator


if __name__ == "__main__":
    failures = 0
    tests = 0

    (f, t) = testmod(kosmorro_pdf_generator, optionflags=NORMALIZE_WHITESPACE)
    failures += f
    tests += t

    if failures > 0:
        exit(1)

    if tests == 0:
        print("No tests found")
        exit(2)

    print("All %d tests successfully passed." % tests)
