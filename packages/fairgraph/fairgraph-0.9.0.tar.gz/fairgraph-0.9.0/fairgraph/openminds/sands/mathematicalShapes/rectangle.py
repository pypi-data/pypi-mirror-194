"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import EmbeddedMetadata, IRI
from fairgraph.fields import Field




class Rectangle(EmbeddedMetadata):
    """

    """
    type = ["https://openminds.ebrains.eu/sands/Rectangle"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("length", "openminds.core.QuantitativeValue", "vocab:length", multiple=False, required=True,
              doc="no description available"),
        Field("width", "openminds.core.QuantitativeValue", "vocab:width", multiple=False, required=True,
              doc="no description available"),

    ]
