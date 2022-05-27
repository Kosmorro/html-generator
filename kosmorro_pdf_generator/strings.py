#!/usr/bin/env python3

from os.path import dirname
from kosmorrolib import Event, ObjectIdentifier, EventType, MoonPhaseType


ASSETS_DIR = "%s/../assets" % dirname(__file__)


def get_object_name(identifier: ObjectIdentifier) -> str:
    return {
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
    }.get(identifier)


def get_object_names_from_keys() -> {str: str}:
    d = {
        "sun": ObjectIdentifier.SUN,
        "moon": ObjectIdentifier.MOON,
        "mercury": ObjectIdentifier.MERCURY,
        "venus": ObjectIdentifier.VENUS,
        "mars": ObjectIdentifier.MARS,
        "jupiter": ObjectIdentifier.JUPITER,
        "saturn": ObjectIdentifier.SATURN,
        "uranus": ObjectIdentifier.URANUS,
        "neptune": ObjectIdentifier.NEPTUNE,
        "pluto": ObjectIdentifier.PLUTO,
    }

    return {k: get_object_name(d[k]) for k in d}


def get_event_description(event: Event) -> (int, str):
    weight, description = {
        EventType.PERIGEE: (0, lambda e: "%s is at its periapsis" % get_object_name(e.objects[0].identifier)),
        EventType.APOGEE: (0, lambda e: "%s is at its apoapsis" % get_object_name(e.objects[0].identifier)),
        EventType.SEASON_CHANGE: (0, lambda e: "Season change"),
        EventType.CONJUNCTION: (5, lambda e: "%s and %s are in conjunction" % (get_object_name(e.objects[0].identifier), get_object_name(e.objects[1].identifier))),
        EventType.MAXIMAL_ELONGATION: (10, lambda e: "Maximum elongation of %s" % get_object_name(e.objects[0].identifier)),
        EventType.OCCULTATION: (20, lambda e: "%s occults %s" % (get_object_name(e.objects[0].identifier), get_object_name(e.objects[1].identifier))),
        EventType.OPPOSITION: (50, lambda e: "%s is in opposition" % get_object_name(e.objects[0].identifier)),
        EventType.LUNAR_ECLIPSE: (100, lambda e: "Lunar eclipse"),
    }.get(event.event_type)

    return weight, description(event)


def get_moon_phase_description(moon_phase: MoonPhaseType) -> str:
    return {
        MoonPhaseType.NEW_MOON: "New Moon",
        MoonPhaseType.WAXING_CRESCENT: "Waxing Crescent",
        MoonPhaseType.FIRST_QUARTER: "First Quarter",
        MoonPhaseType.WAXING_GIBBOUS: "Waxing Gibbous",
        MoonPhaseType.FULL_MOON: "Full Moon",
        MoonPhaseType.WANING_GIBBOUS: "Waning Gibbous",
        MoonPhaseType.LAST_QUARTER: "Last Quarter",
        MoonPhaseType.WANING_CRESCENT: "Waning Crescent"
    }.get(moon_phase)


def get_object_img(identifier: ObjectIdentifier) -> str:
    return {
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
    }.get(identifier)
