"""


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - common data elements
         - Common Data Elements (CDEs) define standardized key terms or concepts for diseases in form of a data dictionary that can be used in both relational and graph metadata models.
       * - data repository model
         - A data repository model defines the file and folder naming and structure as well as partially the file content (metadata definitions) and preferred format.
       * - relational metadata model
         - A relational metadata model defines a set of tabular metadata schemas (including their relations) as architectural base of a relational database for describing the products represented in that database.
       * - graph metadata model
         - A graph metadata model defines a set of modular metadata schemas (including their relations) as architectural base of a graph database for describing the products represented in that database.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class MetaDataModelType(KGObject):
    """


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - common data elements
         - Common Data Elements (CDEs) define standardized key terms or concepts for diseases in form of a data dictionary that can be used in both relational and graph metadata models.
       * - data repository model
         - A data repository model defines the file and folder naming and structure as well as partially the file content (metadata definitions) and preferred format.
       * - relational metadata model
         - A relational metadata model defines a set of tabular metadata schemas (including their relations) as architectural base of a relational database for describing the products represented in that database.
       * - graph metadata model
         - A graph metadata model defines a set of modular metadata schemas (including their relations) as architectural base of a graph database for describing the products represented in that database.

    """
    default_space = "controlled"
    type = ["https://openminds.ebrains.eu/controlledTerms/MetaDataModelType"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the meta data model type."),
        Field("definition", str, "vocab:definition", multiple=False, required=False,
              doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the meta data model type."),
        Field("interlex_identifier", IRI, "vocab:interlexIdentifier", multiple=False, required=False,
              doc="Persistent identifier for a term registered in the InterLex project."),
        Field("knowledge_space_link", IRI, "vocab:knowledgeSpaceLink", multiple=False, required=False,
              doc="Persistent link to an encyclopedia entry in the Knowledge Space project."),
        Field("preferred_ontology_identifier", IRI, "vocab:preferredOntologyIdentifier", multiple=False, required=False,
              doc="Persistent identifier of a preferred ontological term."),
        Field("synonyms", str, "vocab:synonym", multiple=True, required=False,
              doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses."),

    ]
    existence_query_fields = ('name',)
