"""Tests for the line definitions"""
from collections import Counter

import pytest

from dkist_spectral_lines import SpectralLine


@pytest.fixture()
def spectral_lines() -> tuple[SpectralLine]:
    """Import of spectral lines to capture validation errors in test setup vs collection"""
    from dkist_spectral_lines.lines import SPECTRAL_LINES

    return SPECTRAL_LINES


def test_lines_are_valid(spectral_lines):
    """
    :Given: Spectral line data structures
    :When: Instantiating the data structures
    :Then: Validation doesn't raise s pydantic.ValidationError
    """
    # Then
    assert spectral_lines


def test_lines_are_uniquely_named(spectral_lines):
    """
    :Given: Spectral line data structures
    :When: Inspecting name_id
    :Then: All name ids are unique
    """
    name_ids = [l.name_id for l in spectral_lines]
    name_id_counts = Counter(name_ids)
    assert not ({k: v for k, v in name_id_counts.items() if v > 1})
    # failing here probably means the SpectralLine needs include_wavelength_in_name=True
