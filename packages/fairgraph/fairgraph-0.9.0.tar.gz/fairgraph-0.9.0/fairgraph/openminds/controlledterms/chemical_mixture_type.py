"""


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - colloid
         - A 'colloid' is a heterogeneous mixture in which one substance consisting of microscopically dispersed insoluble particles is suspended throughout another substance. [adapted from [wikipedia](https://en.wikipedia.org/wiki/Colloid)]
       * - solution
         - A 'solution' is a special type of homogeneous mixture where at least one substance, called solute, is fully dissolved in another substance, known as a solvent. [adapted from [wikipedia](https://en.wikipedia.org/wiki/Solution_(chemistry))
       * - suspension
         - A 'suspension' is a heterogeneous mixture of a fluid that contains solid particles sufficiently large for sedimentation and may even be visible to the naked eye. [adapted from [wikipedia](https://en.wikipedia.org/wiki/Suspension_(chemistry))]

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class ChemicalMixtureType(KGObject):
    """


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - colloid
         - A 'colloid' is a heterogeneous mixture in which one substance consisting of microscopically dispersed insoluble particles is suspended throughout another substance. [adapted from [wikipedia](https://en.wikipedia.org/wiki/Colloid)]
       * - solution
         - A 'solution' is a special type of homogeneous mixture where at least one substance, called solute, is fully dissolved in another substance, known as a solvent. [adapted from [wikipedia](https://en.wikipedia.org/wiki/Solution_(chemistry))
       * - suspension
         - A 'suspension' is a heterogeneous mixture of a fluid that contains solid particles sufficiently large for sedimentation and may even be visible to the naked eye. [adapted from [wikipedia](https://en.wikipedia.org/wiki/Suspension_(chemistry))]

    """
    default_space = "controlled"
    type = ["https://openminds.ebrains.eu/controlledTerms/ChemicalMixtureType"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the chemical mixture type."),
        Field("definition", str, "vocab:definition", multiple=False, required=False,
              doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the chemical mixture type."),
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
