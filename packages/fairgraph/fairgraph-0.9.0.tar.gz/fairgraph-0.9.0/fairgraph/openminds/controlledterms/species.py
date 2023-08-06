"""
Structured information on the species.

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - `Mustela putorius furo <http://purl.obolibrary.org/obo/NCBITaxon_9669>`_
         - The species *Mustela putorius furo* (domestic ferret) belongs to the family of *mustelidae* (mustelids).
       * - `Macaca fascicularis <http://purl.obolibrary.org/obo/NCBITaxon_9541>`_
         - The species *Macaca fascicularis* (crab-eating macaque) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Chlorocebus pygerythrus <http://purl.obolibrary.org/obo/NCBITaxon_60710>`_
         - The species *Chlorocebus pygerythrus* (vervet marmoset) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Macaca fuscata <http://purl.obolibrary.org/obo/NCBITaxon_9542>`_
         - The species *Macaca fuscata* (Japanese macaque) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Macaca mulatta <http://purl.obolibrary.org/obo/NCBITaxon_9544>`_
         - The species *Macaca mulatta* (rhesus macaque) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Sus scrofa domesticus <http://purl.obolibrary.org/obo/NCBITaxon_9825>`_
         - The species *Sus scrofa domesticus* (domestic pig) belongs to the family of suidae (suids).
       * - `Monodelphis domestica <http://purl.obolibrary.org/obo/NCBITaxon_13616>`_
         - The species *Monodelphis domestica* (gray short-tailed opossum) belongs to the family of *didelphidae* (American possums).
       * - `Callithrix jacchus <http://purl.obolibrary.org/obo/NCBITaxon_9483>`_
         - The species *Callithrix jacchus* (common marmoset) belongs to the family of *callitrichidae* (new world monkeys).
       * - `Homo sapiens <http://purl.obolibrary.org/obo/NCBITaxon_9606>`_
         - The species *Homo sapiens* (humans) belongs to the family of *hominidae* (great apes).
       * - `Danio rerio <http://purl.obolibrary.org/obo/NCBITaxon_7955>`_
         - The species *Danio rerio* (zebrafish) belongs to the family of *cyprinidae* (cyprinids, freshwater fish).
       * - `Rattus norvegicus <http://purl.obolibrary.org/obo/NCBITaxon_10116>`_
         - The species *Rattus norvegicus* (brown rat) belongs to the family of *muridae* (murids).
       * - `Berghia stephanieae <http://purl.obolibrary.org/obo/NCBITaxon_1287507>`_
         - The species *Berghia stephanieae* belongs to the family of *aeolidiidae* (family of sea slugs, shell-less marine gastropod molluscs).
       * - `Chlorocebus aethiops sabaeus <http://purl.obolibrary.org/obo/NCBITaxon_60711>`_
         - The species *Chlorocebus aethiops sabaeus* (green monkey) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Ovis aries <http://purl.obolibrary.org/obo/NCBITaxon_9940>`_
         - The species *Ovis aries* (domestic sheep) belongs to the family of bovidae (bovids).
       * - `Mus musculus <http://purl.obolibrary.org/obo/NCBITaxon_10090>`_
         - The species *Mus musculus* (house mouse) belongs to the family of *muridae* (murids).
       * - `Mustela putorius <http://purl.obolibrary.org/obo/NCBITaxon_9668>`_
         - The species *Mustela putorius* (European polecat) belongs to the family of *mustelidae* (mustelids).

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class Species(KGObject):
    """
    Structured information on the species.

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - `Mustela putorius furo <http://purl.obolibrary.org/obo/NCBITaxon_9669>`_
         - The species *Mustela putorius furo* (domestic ferret) belongs to the family of *mustelidae* (mustelids).
       * - `Macaca fascicularis <http://purl.obolibrary.org/obo/NCBITaxon_9541>`_
         - The species *Macaca fascicularis* (crab-eating macaque) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Chlorocebus pygerythrus <http://purl.obolibrary.org/obo/NCBITaxon_60710>`_
         - The species *Chlorocebus pygerythrus* (vervet marmoset) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Macaca fuscata <http://purl.obolibrary.org/obo/NCBITaxon_9542>`_
         - The species *Macaca fuscata* (Japanese macaque) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Macaca mulatta <http://purl.obolibrary.org/obo/NCBITaxon_9544>`_
         - The species *Macaca mulatta* (rhesus macaque) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Sus scrofa domesticus <http://purl.obolibrary.org/obo/NCBITaxon_9825>`_
         - The species *Sus scrofa domesticus* (domestic pig) belongs to the family of suidae (suids).
       * - `Monodelphis domestica <http://purl.obolibrary.org/obo/NCBITaxon_13616>`_
         - The species *Monodelphis domestica* (gray short-tailed opossum) belongs to the family of *didelphidae* (American possums).
       * - `Callithrix jacchus <http://purl.obolibrary.org/obo/NCBITaxon_9483>`_
         - The species *Callithrix jacchus* (common marmoset) belongs to the family of *callitrichidae* (new world monkeys).
       * - `Homo sapiens <http://purl.obolibrary.org/obo/NCBITaxon_9606>`_
         - The species *Homo sapiens* (humans) belongs to the family of *hominidae* (great apes).
       * - `Danio rerio <http://purl.obolibrary.org/obo/NCBITaxon_7955>`_
         - The species *Danio rerio* (zebrafish) belongs to the family of *cyprinidae* (cyprinids, freshwater fish).
       * - `Rattus norvegicus <http://purl.obolibrary.org/obo/NCBITaxon_10116>`_
         - The species *Rattus norvegicus* (brown rat) belongs to the family of *muridae* (murids).
       * - `Berghia stephanieae <http://purl.obolibrary.org/obo/NCBITaxon_1287507>`_
         - The species *Berghia stephanieae* belongs to the family of *aeolidiidae* (family of sea slugs, shell-less marine gastropod molluscs).
       * - `Chlorocebus aethiops sabaeus <http://purl.obolibrary.org/obo/NCBITaxon_60711>`_
         - The species *Chlorocebus aethiops sabaeus* (green monkey) belongs to the family of *cercopithecidae* (old world monkeys).
       * - `Ovis aries <http://purl.obolibrary.org/obo/NCBITaxon_9940>`_
         - The species *Ovis aries* (domestic sheep) belongs to the family of bovidae (bovids).
       * - `Mus musculus <http://purl.obolibrary.org/obo/NCBITaxon_10090>`_
         - The species *Mus musculus* (house mouse) belongs to the family of *muridae* (murids).
       * - `Mustela putorius <http://purl.obolibrary.org/obo/NCBITaxon_9668>`_
         - The species *Mustela putorius* (European polecat) belongs to the family of *mustelidae* (mustelids).

    """
    default_space = "controlled"
    type = ["https://openminds.ebrains.eu/controlledTerms/Species"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the species."),
        Field("definition", str, "vocab:definition", multiple=False, required=False,
              doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the species."),
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
