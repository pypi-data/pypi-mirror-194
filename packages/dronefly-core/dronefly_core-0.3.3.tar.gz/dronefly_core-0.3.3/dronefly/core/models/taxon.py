"""Taxon model module."""
from pyinaturalist.models import Taxon as PyiNatTaxon

PLANTAE_ID = 47126
TRACHEOPHYTA_ID = 211194

# RANK_LEVELS and RANK_EQUIVALENTS are from:
# - https://github.com/inaturalist/inaturalist/blob/master/app/models/taxon.rb
RANK_LEVELS = {
    "stateofmatter": 100,
    "unranked": 90,  # Invented to make parent check work (this is null in the db)
    "kingdom": 70,
    "phylum": 60,
    "subphylum": 57,
    "superclass": 53,
    "class": 50,
    "subclass": 47,
    "infraclass": 45,
    "subterclass": 44,
    "superorder": 43,
    "order": 40,
    "suborder": 37,
    "infraorder": 35,
    "parvorder": 34.5,
    "zoosection": 34,
    "zoosubsection": 33.5,
    "superfamily": 33,
    "epifamily": 32,
    "family": 30,
    "subfamily": 27,
    "supertribe": 26,
    "tribe": 25,
    "subtribe": 24,
    "genus": 20,
    "genushybrid": 20,
    "subgenus": 15,
    "section": 13,
    "subsection": 12,
    "complex": 11,
    "species": 10,
    "hybrid": 10,
    "subspecies": 5,
    "variety": 5,
    "form": 5,
    "infrahybrid": 5,
}

RANK_EQUIVALENTS = {
    "division": "phylum",
    "sub-class": "subclass",
    "super-order": "superorder",
    "sub-order": "suborder",
    "super-family": "superfamily",
    "sub-family": "subfamily",
    "gen": "genus",
    "sp": "species",
    "spp": "species",
    "infraspecies": "subspecies",
    "ssp": "subspecies",
    "sub-species": "subspecies",
    "subsp": "subspecies",
    "trinomial": "subspecies",
    "var": "variety",
    # 'unranked': None,
}

RANK_KEYWORDS = tuple(RANK_LEVELS.keys()) + tuple(RANK_EQUIVALENTS.keys())
TAXON_PRIMARY_RANKS = ["kingdom", "phylum", "class", "order", "family"]
TRINOMIAL_ABBR = {"variety": "var.", "subspecies": "ssp.", "form": "f."}


def taxon_ancestor_ranks(taxon: PyiNatTaxon):
    return (
        ["stateofmatter"] + [ancestor.rank for ancestor in taxon.ancestors]
        if taxon.ancestors
        else []
    )


class Taxon(PyiNatTaxon):
    """Public class for Taxon model."""

    # Deprecated. Use taxon_ancestor_ranks directly instead.
    def ancestor_ranks(self):
        return taxon_ancestor_ranks(self)
