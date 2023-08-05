"""Renumics Licensing"""
import sys
from pathlib import Path

from loguru import logger

from renumics.spotlight.settings import settings

from .terms_and_conditions import (
    TermsAndConditionsNotAccepted,
    verify_terms_and_conditions,
)
from .verification import FeatureNotLicensed, LicensedFeature, verify_feature


license_path = Path(settings.license_path).expanduser().resolve()


def verify_license_or_exit() -> LicensedFeature:
    """
    Check if Renumics license is valid.
    Otherwise, close Spotlight.
    """
    try:
        return verify_feature("spotlight", license_path)
    except FeatureNotLicensed as e:
        logger.error(e)
        sys.exit(1)


def verify_terms_and_conditions_or_exit() -> None:
    """
    Force to accept Renumics Spotlight terms and conditions.
    Otherwise, close Spotlight.
    """
    try:
        verify_terms_and_conditions()
    except TermsAndConditionsNotAccepted as e:
        logger.error(e)
        sys.exit(1)


spotlight_license = verify_license_or_exit()
verify_terms_and_conditions_or_exit()
username = spotlight_license.users[0]
