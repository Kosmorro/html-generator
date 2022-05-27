#!/usr/bin/env python3


def parse_template(template: str, **kwargs: {str: str}) -> str:
    for arg in kwargs:
        template = template.replace("{{ %s }}" % arg, kwargs[arg])

    return template
