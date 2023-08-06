"""


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - ambilevous handedness
         - Handedness where the organism exhibits equally poor dexterity in the use of right or left hand or foot in the performance of tasks that require one (dominant) hand or foot.
       * - ambidextrous handedness
         - Handedness where the organism exhibits no overall dominance in the use of right or left hand or foot in the performance of tasks that require one (dominant) hand or foot.
       * - left handedness
         - Handedness where the organism preferentially uses the left hand or foot for tasks requiring the use of a single hand or foot.
       * - right handedness
         - Handedness where the organism preferentially uses the right hand or foot for tasks requiring the use of a single hand or foot.
       * - mixed handedness
         - Handedness where the organism exhibits dominance in the use of right or left hand or foot differently in the performance of different tasks that require one (dominant) hand or foot.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class Handedness(KGObject):
    """


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - ambilevous handedness
         - Handedness where the organism exhibits equally poor dexterity in the use of right or left hand or foot in the performance of tasks that require one (dominant) hand or foot.
       * - ambidextrous handedness
         - Handedness where the organism exhibits no overall dominance in the use of right or left hand or foot in the performance of tasks that require one (dominant) hand or foot.
       * - left handedness
         - Handedness where the organism preferentially uses the left hand or foot for tasks requiring the use of a single hand or foot.
       * - right handedness
         - Handedness where the organism preferentially uses the right hand or foot for tasks requiring the use of a single hand or foot.
       * - mixed handedness
         - Handedness where the organism exhibits dominance in the use of right or left hand or foot differently in the performance of different tasks that require one (dominant) hand or foot.

    """
    default_space = "controlled"
    type = ["https://openminds.ebrains.eu/controlledTerms/Handedness"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the handedness."),
        Field("definition", str, "vocab:definition", multiple=False, required=False,
              doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the handedness."),
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
