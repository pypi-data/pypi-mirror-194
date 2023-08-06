"""
Structured information about a relationship between two entities, such as a person and their employer.
"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import EmbeddedMetadata, IRI
from fairgraph.fields import Field




class Affiliation(EmbeddedMetadata):
    """
    Structured information about a relationship between two entities, such as a person and their employer.
    """
    type = ["https://openminds.ebrains.eu/core/Affiliation"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("end_date", date, "vocab:endDate", multiple=False, required=False,
              doc="Date in the Gregorian calendar at which something terminates in time."),
        Field("member_of", ["openminds.core.Consortium", "openminds.core.Organization"], "vocab:memberOf", multiple=False, required=False,
              doc="no description available", alternate_path="vocab:organization"),
        Field("start_date", date, "vocab:startDate", multiple=False, required=False,
              doc="Date in the Gregorian calendar at which something begins in time"),

    ]
