#!/usr/bin/env python3

from .events import fmt_events, get_event_illustration
from .template import parse_template
from .strings import ASSETS_DIR, get_moon_phase_description, get_object_names_from_keys

from datetime import date
from kosmorrolib import AsterEphemerides, Event
from kosmorrolib.ephemerides import MoonPhase
from babel.dates import format_date


def generate_pdf(
    output_file: str,
    for_date: date,
    ephemerides: [AsterEphemerides],
    moon_phase: MoonPhase,
    events: [Event],
    timezone: int = 0,
    locale: str = "en",
):
    with open("assets/template.html", "r") as file:
        template = file.read()

    def fmt_date(the_date, the_locale):
        return format_date(the_date, "full", the_locale)

    images_objects = {}

    for object_name in get_object_names_from_keys().keys():
        images_objects[
            f"image_{object_name}"
        ] = f"{ASSETS_DIR}/img/objects/{object_name}.png"

    formated_events, highest_event = fmt_events(events)

    if timezone != 0:
        timezone_text = f"UTC{'+' if timezone > 0 else ''}{timezone}"
    else:
        timezone_text = "UTC timezone"

    html = parse_template(
        template,
        css_template=f"{ASSETS_DIR}/template.css",
        page_title="Overview of your sky",
        date=fmt_date(for_date, locale),
        introduction_1=(
            f"This document summarizes the ephemerides and the events of {fmt_date(for_date, locale)}."
            f" It aims to help you to prepare your observation session. All the hours are given in {timezone_text}."
        ),
        introduction_2="Don’t forget to check the weather forecast before you go out with your equipment.",
        moon_phase_title="Moon phase",
        events_title="Expected events",
        moon_phase=get_moon_phase_description(moon_phase.phase_type),
        events_list=formated_events,
        event_illustration=get_event_illustration(highest_event),
        **get_object_names_from_keys(),
        **images_objects,
    )

    with open(f"{output_file}.html", "w") as file:
        file.write(html)
