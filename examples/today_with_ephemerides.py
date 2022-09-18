import kosmorrolib
from kosmorro_pdf_generator import generate_html

generate_html(
    "export.html",
    ephemerides=kosmorrolib.get_ephemerides(kosmorrolib.Position(50.5824, 3.0624)),
    moon_phase=kosmorrolib.get_moon_phase(),
    events=kosmorrolib.get_events(),
)
