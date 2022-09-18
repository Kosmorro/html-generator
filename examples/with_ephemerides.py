from datetime import date

import kosmorrolib
from kosmorro_pdf_generator import generate_html

d = date(2022, 2, 27)

generate_html(
    "export.html",
    ephemerides=kosmorrolib.get_ephemerides(kosmorrolib.Position(50.5824, 3.0624), d),
    moon_phase=kosmorrolib.get_moon_phase(d),
    events=kosmorrolib.get_events(d),
    for_date=d,
)
