#!/usr/bin/env python3

from .events import fmt_events, get_event_illustration
from .ephemerides import generate_ephemerides
from .template import parse_template
from .strings import (
    ASSETS_DIR,
    ASSETS_DIR_URI,
    get_moon_phase_description,
    get_object_names_from_keys,
)

from datetime import date
from kosmorrolib import AsterEphemerides, Event
from kosmorrolib.ephemerides import MoonPhase
from babel.dates import format_date

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


def generate_pdf(
    output_file: str,
    moon_phase: MoonPhase,
    events: [Event],
    for_date: date = date.today(),
    ephemerides: [AsterEphemerides] = None,
    timezone: int = 0,
    locale: str = "en",
    debug: bool = False,
):
    with open(f"{ASSETS_DIR}/template.html", "r") as file:
        template = file.read()

    def fmt_date(the_date, the_locale):
        return format_date(the_date, "full", the_locale)

    images_objects = {}

    for object_name in get_object_names_from_keys().keys():
        images_objects[
            f"image_{object_name}"
        ] = f"{ASSETS_DIR_URI}/img/objects/{object_name}.png"

    if len(events) > 0:
        formated_events, highest_event = fmt_events(events)
    else:
        formated_events, highest_event = "No event at this date", None

    if timezone != 0:
        timezone_text = f"UTC{'+' if timezone > 0 else ''}{timezone}"
    else:
        timezone_text = "UTC timezone"

    with open(f"{ASSETS_DIR}/template.css", "r") as file:
        stylesheet = parse_template(file.read(), media_folder=ASSETS_DIR_URI)

    html = parse_template(
        template,
        stylesheet=stylesheet,
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
        ephemerides=generate_ephemerides(ephemerides)
        if ephemerides is not None
        else "",
        events_list=formated_events,
        event_illustration=get_event_illustration(highest_event)
        if highest_event is not None
        else "",
        **get_object_names_from_keys(),
        **images_objects,
    )

    if debug:
        with open(f"{output_file}.html", "w") as file:
            file.write(html)

    # Load fonts
    font_config = FontConfiguration()
    CSS(string=stylesheet, font_config=font_config)

    HTML(string=html).write_pdf(
        output_file, font_config=font_config, optimize_size=("fonts", "images")
    )
