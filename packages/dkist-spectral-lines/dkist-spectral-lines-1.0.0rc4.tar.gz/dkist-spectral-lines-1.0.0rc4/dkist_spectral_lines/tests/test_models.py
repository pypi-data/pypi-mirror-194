"""Tests for the SpectralLine data structure and validation"""
import random
from uuid import uuid4

import pytest
from pydantic import ValidationError

from dkist_spectral_lines import Instrument
from dkist_spectral_lines import Line
from dkist_spectral_lines import SpectralLine

# Instrument parameters
instrument_strings = [element.value for element in Instrument]
instrument_enums = [element for element in Instrument]
instruments = instrument_strings + instrument_enums
# Line parameters
line_strings = [element.value for element in Line]
line_enums = [element for element in Line]
lines = line_strings + line_enums


@pytest.fixture(params=instruments)
def valid_instrument(request):
    """Parametrized list of Instruments"""
    return request.param


@pytest.fixture(params=lines)
def valid_line(request):
    """Parametrized list of lines"""
    return request.param


@pytest.fixture(
    params=[
        pytest.param(True, id="include_wavelength_name"),
        pytest.param(False, id="no_include_wavelength_name"),
    ]
)
def include_wavelength_name(request):
    """Parametrized values for include_wavelength_name"""
    return request.param


@pytest.fixture(
    params=[
        pytest.param(True, id="has_filter_id"),
        pytest.param(False, id="no_filter_id"),
    ]
)
def filter_id(request):
    """Parametrized values for filter_id"""
    has_filter_id = request.param
    if has_filter_id:
        return uuid4().hex[:6]
    return None


@pytest.fixture()
def valid_wavelength_metadata() -> dict:
    """Valid wavelength metadata"""
    wavelength = random.random()
    filter_max = wavelength + 1
    filter_min = wavelength - 1
    result = {
        "wavelength": wavelength,
        "filter_max": filter_max,
        "filter_min": filter_min,
    }
    return result


@pytest.fixture()
def valid_spectral_line(
    include_wavelength_name, valid_instrument, valid_line, valid_wavelength_metadata, filter_id
) -> dict:
    """A valid spectral line definition"""

    result = {
        "instrument": valid_instrument,
        "line": valid_line,
        "include_wavelength_name": include_wavelength_name,
        "filter_id": filter_id,
    } | valid_wavelength_metadata
    return result


def test_validation_pass(valid_spectral_line):
    """
    :Given: Valid metadata for a SpectralLine
    :When: Instantiating a SpectralLine
    :Then: Validation is passed
    """
    line: SpectralLine = SpectralLine.parse_obj(valid_spectral_line)
    expected_instrument = valid_spectral_line["instrument"]
    expected_line = valid_spectral_line["line"]
    expected_wavelength = valid_spectral_line["wavelength"]
    expected_filter_min = valid_spectral_line["filter_min"]
    expected_filter_max = valid_spectral_line["filter_max"]
    expected_filter_id = valid_spectral_line["filter_id"]
    expected_wavelength_width = expected_filter_max - expected_filter_min
    assert line.instrument == expected_instrument
    assert line.line == expected_line
    assert line.wavelength == expected_wavelength
    assert line.filter_min == expected_filter_min
    assert line.filter_max == expected_filter_max
    assert line.filter_width == expected_wavelength_width
    assert line.filter_id == expected_filter_id
    assert isinstance(line.name, str)
    assert isinstance(line.name_id, str)


@pytest.fixture()
def single_valid_spectral_line(valid_wavelength_metadata) -> dict:
    """A single valid set of spectral line data to be used as the baseline for negative tests"""
    result = {
        "instrument": instrument_enums[0],
        "line": line_enums[0],
        "include_wavelength_name": False,
        "filter_id": None,
    } | valid_wavelength_metadata
    return result


@pytest.mark.parametrize(
    "args",
    [
        pytest.param({"instrument": "FAKE_INSTRUMENT"}, id="invalid_instrument"),
        pytest.param({"line": "FAKE_LINE"}, id="invalid_line"),
        pytest.param(
            {"wavelength": 10, "filter_min": 11, "filter_max": 12},
            id="invalid_filter_min_combination",
        ),
        pytest.param(
            {"wavelength": 10, "filter_min": 8, "filter_max": 9},
            id="invalid_filter_max_combination",
        ),
        pytest.param(
            {"wavelength": 10, "filter_min": 11, "filter_max": 9},
            id="invalid_wavelength_bounds_combination",
        ),
    ],
)
def test_validation_fail(args: dict, single_valid_spectral_line: dict):
    """
    :Given: Invalid metadata for a SpectralLine
    :When: Instantiating a SpectralLine
    :Then: Validation error is raised
    """
    invalid_spectral_line = single_valid_spectral_line | args
    with pytest.raises(ValidationError):
        SpectralLine.parse_obj(invalid_spectral_line)
