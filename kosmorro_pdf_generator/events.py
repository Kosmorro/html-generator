#!/usr/bin/env python3

from .template import parse_template
from .strings import get_event_description, get_object_img

from kosmorrolib import Event, EventType
from babel.dates import format_time


def fmt_events(the_events: [Event]) -> (str, Event):
    template = "<li><strong>{{ event_hour }}</strong> {{ event_description }}</li>"
    html = ""

    highest_weight, highest_event = -1, None

    for event in the_events:
        weight, description = get_event_description(event)

        if weight > highest_weight:
            highest_weight = weight
            highest_event = event

        html += parse_template(
            template,
            event_hour=format_time(event.start_time, 'short'),
            event_description=description
        )

    return html, highest_event


def get_event_illustration(event: Event) -> str:
    return {
        EventType.OPPOSITION: lambda e: '',
        EventType.CONJUNCTION: lambda e: f'{get_object_img(e.objects[0].identifier)}{get_object_img(e.objects[1].identifier)}',
        EventType.OCCULTATION: lambda e: '',
        EventType.MAXIMAL_ELONGATION: lambda e: '',
        EventType.SEASON_CHANGE: lambda e: '',
        EventType.LUNAR_ECLIPSE: lambda e: '',
    }.get(event.event_type, lambda e: "")(event)
