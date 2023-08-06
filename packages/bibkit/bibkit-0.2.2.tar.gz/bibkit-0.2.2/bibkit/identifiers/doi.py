import re
from enum import Enum
from typing import Union
from ..utils import ValidationResult, ValidationFailure


doi_short_re = re.compile(r"^10\.\d{4,6}(\.\d{1,15}){0,5}\/\S+$")
doi_handbook_re = re.compile(r"^doi:10\.\d{4,6}(\.\d{1,15}){0,5}\/\S+$")
doi_handle_re = re.compile(r"^info:doi\/10\.\d{4,6}(\.\d{1,15}){0,5}\/\S+$")
doi_crossref_re = re.compile(r"^https:\/\/doi.org/10\.\d{4,6}(\.\d{1,15}){0,5}\/\S+$")
doi_legacy_url_re = re.compile(
    r"^(http[s]{0,1}:\/\/){0,1}(dx\.){0,1}doi\.org\/10\.\d{4,6}(\.\d{1,15}){0,5}\/\S+$"
)

doi_search_re = re.compile(r"10\.\d{4,6}(\.\d{1,15}){0,5}\/\S+")


class DoiFormat(Enum):
    """DOI format"""

    CROSSREF = 1
    """``https://doi.org/10.1000/123`` URL form, recommended by Crossref"""
    HANDBOOK = 2
    """``doi:10.1000/123`` short form, but prefixed with "``doi:``", recommended by the DOI Handbook"""
    HANDLE = 3
    """``info:doi/10.1000/123`` URI format in the Handle system"""
    SHORT = 4
    """``10.1000/123`` short form consisting only of prefix and suffix"""


def format(doi: str, format: DoiFormat) -> Union[str, None]:
    """Format DOI to specified format

    Args:
        doi (str): DOI to format
        format (DoiFormat): Format to use

    Returns:
        (str): Formatted DOI
        (None): If formatting was not possible
    """

    if type(doi) != str:
        return None

    if type(format) != DoiFormat:
        return None

    if (match := doi_search_re.search(doi)) is not None:
        doi = match.group(0)

        if format is DoiFormat.SHORT:
            return doi

        if format is DoiFormat.CROSSREF:
            return f"https://doi.org/{doi}"

        if format is DoiFormat.HANDBOOK:
            return f"doi:{doi}"

        if format is DoiFormat.HANDLE:
            return f"info:doi/{doi}"

    return None


format_re_map = {
    DoiFormat.CROSSREF: doi_crossref_re,
    DoiFormat.HANDBOOK: doi_handbook_re,
    DoiFormat.HANDLE: doi_handle_re,
    DoiFormat.SHORT: doi_short_re,
}


def validate(doi: str, format: DoiFormat) -> ValidationResult:
    """
    Validates DOI is in the given format

    :param str doi: DOI to validate
    :param format: Format to use
    :type format: DoiFormat

    :return: validation result
    :rtype: `ValidationResult`
    """

    if type(doi) != str:
        return ValidationResult(False, ValidationFailure.WRONG_TYPE)

    if type(format) != DoiFormat:
        for regexp in format_re_map.values():
            if regexp.match(doi):
                return ValidationResult(True, None)

        return ValidationResult(False, ValidationFailure.WRONG_FORMAT)

    if not format_re_map[format].match(doi):
        return ValidationResult(False, ValidationFailure.WRONG_FORMAT)

    return ValidationResult(True, None)
