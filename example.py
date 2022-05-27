from datetime import date

from kosmorrolib import get_ephemerides, get_events, get_moon_phase, Position
from kosmorro_pdf_generator import generate_pdf

d = date(2022, 2, 27)

generate_pdf(
    'export.pdf',
    d,
    get_ephemerides(Position(50.5824, 3.0624), d),
    get_moon_phase(d),
    get_events(d)
)
