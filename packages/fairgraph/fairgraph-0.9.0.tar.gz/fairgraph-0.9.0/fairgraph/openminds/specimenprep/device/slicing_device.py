"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class SlicingDevice(KGObject):
    """

    """
    default_space = "in-depth"
    type = ["https://openminds.ebrains.eu/specimenPrep/SlicingDevice"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the slicing device."),
        Field("lookup_label", str, "vocab:lookupLabel", multiple=False, required=False,
              doc="no description available"),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the slicing device."),
        Field("device_type", "openminds.controlledterms.DeviceType", "vocab:deviceType", multiple=False, required=False,
              doc="no description available"),
        Field("digital_identifier", ["openminds.core.DOI", "openminds.core.RRID"], "vocab:digitalIdentifier", multiple=False, required=False,
              doc="Digital handle to identify objects or legal persons."),
        Field("manufacturers", ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"], "vocab:manufacturer", multiple=True, required=True,
              doc="no description available"),
        Field("owners", ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"], "vocab:owner", multiple=True, required=False,
              doc="no description available"),
        Field("serial_number", str, "vocab:serialNumber", multiple=False, required=False,
              doc="no description available"),

    ]
    existence_query_fields = ('lookup_label',)
