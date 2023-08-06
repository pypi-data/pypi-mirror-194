"""


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - Kolmogorov-Smirnov statistic
         - Quantification of a distance between the empirical distribution function of the sample and the cumulative distribution function of the reference distribution, or between the empirical distribution functions of two samples.
       * - mean squared error
         - The mean squared difference between two series of values.
       * - z-score
         - The number of standard deviations by which an observed value is above or below the mean value.
       * - Kullback-Leibler divergence
         - A measure of how one probability distribution is different from a second, reference probability distribution.
       * - chi-squared statistic
         - Test statistic resulting from a chi-squared test.
       * - t-statistic
         - The ratio of the departure of the estimated value of a parameter from its hypothesized value to its standard error.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class DifferenceMeasure(KGObject):
    """


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - Kolmogorov-Smirnov statistic
         - Quantification of a distance between the empirical distribution function of the sample and the cumulative distribution function of the reference distribution, or between the empirical distribution functions of two samples.
       * - mean squared error
         - The mean squared difference between two series of values.
       * - z-score
         - The number of standard deviations by which an observed value is above or below the mean value.
       * - Kullback-Leibler divergence
         - A measure of how one probability distribution is different from a second, reference probability distribution.
       * - chi-squared statistic
         - Test statistic resulting from a chi-squared test.
       * - t-statistic
         - The ratio of the departure of the estimated value of a parameter from its hypothesized value to its standard error.

    """
    default_space = "controlled"
    type = ["https://openminds.ebrains.eu/controlledTerms/DifferenceMeasure"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the difference measure."),
        Field("definition", str, "vocab:definition", multiple=False, required=False,
              doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the difference measure."),
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
