from datetime import date

import kosmorrolib
from kosmorro_pdf_generator import generate_html

d = date(2022, 2, 27)

generate_html(
    "export.html",
    for_date=d,
    moon_phase=kosmorrolib.get_moon_phase(d),
    events=kosmorrolib.get_events(d),
)
