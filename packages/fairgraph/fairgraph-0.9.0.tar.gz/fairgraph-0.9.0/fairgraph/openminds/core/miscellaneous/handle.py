"""
A persistent identifier for an information resource provided by the Handle System of the Corporation for National Research Initiatives.
"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class HANDLE(KGObject):
    """
    A persistent identifier for an information resource provided by the Handle System of the Corporation for National Research Initiatives.
    """
    default_space = "common"
    type = ["https://openminds.ebrains.eu/core/HANDLE"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("identifier", str, "vocab:identifier", multiple=False, required=True,
              doc="Term or code used to identify the HANDLE."),

    ]
    existence_query_fields = ('identifier',)
