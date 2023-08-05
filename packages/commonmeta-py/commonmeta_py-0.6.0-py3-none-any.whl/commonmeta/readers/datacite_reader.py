"""datacite reader for Commonmeta"""
from typing import Optional
from functools import reduce
import requests
from pydash import py_

from ..utils import normalize_url, normalize_doi
from ..base_utils import compact, wrap, presence
from ..author_utils import get_authors
from ..date_utils import strip_milliseconds
from ..doi_utils import doi_as_url, doi_from_url, datacite_api_url
from ..constants import (
    CR_TO_SO_TRANSLATIONS,
    CR_TO_CP_TRANSLATIONS,
    CR_TO_BIB_TRANSLATIONS,
    CR_TO_RIS_TRANSLATIONS,
    DC_TO_RIS_TRANSLATIONS,
    DC_TO_SO_TRANSLATIONS,
    SO_TO_CP_TRANSLATIONS,
    SO_TO_BIB_TRANSLATIONS,
    Commonmeta,
)


def get_datacite(pid: str, **kwargs) -> dict:
    """get_datacite"""
    doi = doi_from_url(pid)
    if doi is None:
        return {"state": "not_found"}
    url = datacite_api_url(doi)
    response = requests.get(url, kwargs, timeout=5)
    if response.status_code != 200:
        return {"state": "not_found"}
    return py_.get(response.json(), "data.attributes", {})


def read_datacite(data: dict, **kwargs) -> Commonmeta:
    """read_datacite"""
    meta = data

    read_options = kwargs or {}

    pid = doi_as_url(meta.get("doi", None))
    resource_type_general = py_.get(meta, "types.resourceTypeGeneral")
    resource_type = py_.get(meta, "types.resourceType")
    schema_org = (
        CR_TO_SO_TRANSLATIONS.get(py_.camel_case(resource_type), None)
        or DC_TO_SO_TRANSLATIONS.get(resource_type_general, None)
        or "CreativeWork"
    )
    types = compact(
        {
            "resourceTypeGeneral": resource_type_general,
            "resourceType": resource_type,
            "schemaOrg": schema_org,
            "citeproc": CR_TO_CP_TRANSLATIONS.get(py_.camel_case(resource_type), None)
            or SO_TO_CP_TRANSLATIONS.get(schema_org, None)
            or "article",
            "bibtex": CR_TO_BIB_TRANSLATIONS.get(py_.camel_case(resource_type), None)
            or SO_TO_BIB_TRANSLATIONS.get(schema_org, None)
            or "misc",
            "ris": CR_TO_RIS_TRANSLATIONS.get(py_.camel_case(resource_type), None)
            or DC_TO_RIS_TRANSLATIONS.get(resource_type_general, None)
            or "GEN",
        }
    )

    rights = meta.get("rightsList", None)

    references = get_references(wrap(meta.get("relatedItems", None) or meta.get("relatedIdentifiers", None)))

    return {
        # required properties
        "pid": pid,
        "doi": doi_from_url(pid),
        "url": normalize_url(meta.get("url", None)),
        "creators": get_authors(wrap(meta.get("creators", None))),
        "titles": compact(meta.get("titles", None)),
        "publisher": meta.get("publisher", None),
        "publication_year": int(meta.get("publicationYear", None)),
        "types": types,
        # recommended and optional properties
        "subjects": presence(meta.get("subjects", None)),
        "contributors": get_authors(wrap(meta.get("contributors", None))),
        "dates": presence(meta.get("dates", None))
        or [{"date": meta.get("publicationYear", None), "dateType": "Issued"}],
        "language": meta.get("language", None),
        "alternate_identifiers": presence(meta.get("alternateIdentifiers", None)),
        "sizes": presence(meta.get("sizes", None)),
        "formats": presence(meta.get("formats", None)),
        "version": meta.get("version", None),
        "rights": presence(rights),
        "descriptions": meta.get("descriptions", None),
        "geo_locations": wrap(meta.get("geoLocations", None)),
        "funding_references": meta.get("fundingReferences", None),
        "references": presence(references),
        # other properties
        "date_created": strip_milliseconds(meta.get("created", None)),
        "date_registered": strip_milliseconds(meta.get("registered", None)),
        "date_published": strip_milliseconds(meta.get("published", None)),
        "date_updated": strip_milliseconds(meta.get("updated", None)),
        "content_url": presence(meta.get("contentUrl", None)),
        "container": presence(meta.get("container", None)),
        "agency": "DataCite",
        "state": "findable",
        "schema_version": meta.get("schemaVersion", None),
    } | read_options


def get_references(references: list) -> list:
    """get_references"""
    print(references)
    def is_reference(reference):
        """is_reference"""
        return reference.get("relationType", None) in ["Cites", "References"]
    
    def map_reference(reference):
        """map_reference"""
        identifier = reference.get("relatedIdentifier", None)
        identifier_type = reference.get("relatedIdentifierType", None)
        if identifier and identifier_type == "DOI":
            reference["doi"] = normalize_doi(identifier)
        elif identifier and identifier_type == "URL":
            reference["url"] = normalize_url(identifier)
        reference = py_.omit(
            reference,
            [
                "relationType",
                "relatedIdentifier",
                "relatedIdentifierType",
                "resourceTypeGeneral",
                "schemeType",
                "schemeUri",
                "relatedMetadataScheme"
            ])
        return reference
    return [map_reference(i) for i in references if is_reference(i)]
