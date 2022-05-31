#!/usr/bin/env python3

from .strings import ASSETS_DIR

from kosmorrolib import AsterEphemerides


def generate_ephemerides(ephemerides: [AsterEphemerides], graph: bool = True) -> str:
    if len(ephemerides) == 0:
        return ""

    with open(f"{ASSETS_DIR}/ephemerides-graph.svg") as file:
        template = file.read()

    return template
