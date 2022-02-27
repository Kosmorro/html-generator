#!/usr/bin/env python3

from datetime import date
from kosmorrolib import AsterEphemerides, Event, MoonPhaseType, EventType, ObjectIdentifier
from kosmorrolib.ephemerides import MoonPhase
from os.path import dirname
from babel.dates import format_date, format_time


ASSETS_DIR = "%s/../assets" % dirname(__file__)

OBJECTS_IDENTIFIER_TO_NAME = {
    ObjectIdentifier.SUN: "Sun",
    ObjectIdentifier.MOON: "Moon",
    ObjectIdentifier.MERCURY: "Mercury",
    ObjectIdentifier.VENUS: "Venus",
    ObjectIdentifier.MARS: "Mars",
    ObjectIdentifier.JUPITER: "Jupiter",
    ObjectIdentifier.SATURN: "Saturn",
    ObjectIdentifier.URANUS: "Uranus",
    ObjectIdentifier.NEPTUNE: "Neptune",
    ObjectIdentifier.PLUTO: "Pluto",
}

OBJECTS_KEY_TO_NAME = {
    "sun": "Sun",
    "moon": "Moon",
    "mercury": "Mercury",
    "venus": "Venus",
    "mars": "Mars",
    "jupiter": "Jupiter",
    "saturn": "Saturn",
    "uranus": "Uranus",
    "neptune": "Neptune",
    "pluto": "Pluto",
}

EVENTS_TYPES = {
    EventType.PERIGEE: (0, lambda e: "%s is at its periapsis" % OBJECTS_IDENTIFIER_TO_NAME.get(e.objects[0].identifier)),
    EventType.APOGEE: (0, lambda e: "%s is at its apoapsis" % OBJECTS_IDENTIFIER_TO_NAME.get(e.objects[0].identifier)),
    EventType.SEASON_CHANGE: (0, lambda e: "Season change"),
    EventType.CONJUNCTION: (5, lambda e: "%s and %s are in conjunction" % (OBJECTS_IDENTIFIER_TO_NAME.get(e.objects[0].identifier), OBJECTS_IDENTIFIER_TO_NAME.get(e.objects[1].identifier))),
    EventType.MAXIMAL_ELONGATION: (10, lambda e: "Maximum elongation of %s" % OBJECTS_IDENTIFIER_TO_NAME.get(e.objects[0].identifier)),
    EventType.OCCULTATION: (20, lambda e: "%s occults %s" % (OBJECTS_IDENTIFIER_TO_NAME.get(e.objects[0].identifier), OBJECTS_IDENTIFIER_TO_NAME.get(e.objects[1].identifier))),
    EventType.OPPOSITION: (50, lambda e: "%s is in opposition" % OBJECTS_IDENTIFIER_TO_NAME.get(e.objects[0].identifier)),
    EventType.LUNAR_ECLIPSE: (100, lambda e: "Lunar eclipse"),
}

OBJECTS_IMAGES = {
    ObjectIdentifier.SUN: f'<img src="{ASSETS_DIR}/img/objects/sun.png" alt="" aria-hidden="true" />',
    ObjectIdentifier.MOON: f'<img src="{ASSETS_DIR}/img/objects/moon.png" alt="" aria-hidden="true" />',
    ObjectIdentifier.MERCURY: f'<img src="{ASSETS_DIR}/img/objects/mercury.png" alt="" aria-hidden="true" />',
    ObjectIdentifier.VENUS: f'<img src="{ASSETS_DIR}/img/objects/venus.png" alt="" aria-hidden="true" />',
    ObjectIdentifier.MARS: f'<img src="{ASSETS_DIR}/img/objects/mars.png" alt="" aria-hidden="true" />',
    ObjectIdentifier.JUPITER: f'<img src="{ASSETS_DIR}/img/objects/jupiter.png" alt="" aria-hidden="true" />',
    ObjectIdentifier.SATURN: f'<img src="{ASSETS_DIR}/img/objects/saturn.png" alt="" aria-hidden="true" />',
    ObjectIdentifier.URANUS: f'<img src="{ASSETS_DIR}/img/objects/uranus.png" alt="" aria-hidden="true" />',
    ObjectIdentifier.NEPTUNE: f'<img src="{ASSETS_DIR}/img/objects/neptune.png" alt="" aria-hidden="true" />',
    ObjectIdentifier.PLUTO: f'<img src="{ASSETS_DIR}/img/objects/pluto.png" alt="" aria-hidden="true" />',
}


def generate_pdf(for_date: date, ephemerides: [AsterEphemerides], moon_phase: MoonPhase, events: [Event], timezone: int = 0, locale: str = 'en'):
    with open('assets/template.html', 'r') as file:
        template = file.read()

    def parse_template(template: str, **kwargs: {str: str}) -> str:
        print(kwargs)
        for arg in kwargs:
            template = template.replace("{{ %s }}" % arg, kwargs[arg])

        return template

    def fmt_date(the_date, the_locale):
        return format_date(the_date, 'full', the_locale)

    def fmt_events(the_events: [Event]) -> (str, Event):
        template = "<li><strong>{{ event_hour }}</strong> {{ event_description }}</li>"
        html = ""

        highest_weight, highest_event = -1, None

        for event in the_events:
            print(event)
            weight, description = EVENTS_TYPES.get(event.event_type)

            if weight > highest_weight:
                highest_weight = weight
                highest_event = event

            html += parse_template(
                template,
                event_hour=format_time(event.start_time, 'short'),
                event_description=description(event)
            )

        return html, highest_event

    images_objects = {}

    for object_name in ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]:
        images_objects[f"image_{object_name}"] = f"{ASSETS_DIR}/img/objects/{object_name}.png"

    formated_events, highest_event = fmt_events(events)
    event_illustration = lambda e: ""

    if highest_event is not None:
        event_illustration = {
            EventType.OPPOSITION: lambda e: '',
            EventType.CONJUNCTION: lambda e: f'{OBJECTS_IMAGES[e.objects[0].identifier]}{OBJECTS_IMAGES[e.objects[1].identifier]}',
            EventType.OCCULTATION: lambda e: '',
            EventType.MAXIMAL_ELONGATION: lambda e: '',
            EventType.SEASON_CHANGE: lambda e: '',
            EventType.LUNAR_ECLIPSE: lambda e: '',
        }.get(highest_event.event_type, lambda e: "")
        print(highest_event.objects[0].identifier)
        print(event_illustration(highest_event))

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
        moon_phase={
            MoonPhaseType.NEW_MOON: "New Moon",
            MoonPhaseType.WAXING_CRESCENT: "Waxing Crescent",
            MoonPhaseType.FIRST_QUARTER: "First Quarter",
            MoonPhaseType.WAXING_GIBBOUS: "Waxing Gibbous",
            MoonPhaseType.FULL_MOON: "Full Moon",
            MoonPhaseType.WANING_GIBBOUS: "Waning Gibbous",
            MoonPhaseType.LAST_QUARTER: "Last Quarter",
            MoonPhaseType.WANING_CRESCENT: "Waning Crescent"
        }.get(moon_phase.phase_type),
        events_list=formated_events,
        event_illustration=event_illustration(highest_event),
        **OBJECTS_KEY_TO_NAME,
        **images_objects,
    )

    with open('/tmp/truc.html', 'w') as file:
        file.write(html)


from kosmorrolib import get_ephemerides, get_events, get_moon_phase, Position

d = date(2022, 2, 27)

generate_pdf(d, get_ephemerides(Position(50.5824, 3.0624), d), get_moon_phase(d), get_events(d))
