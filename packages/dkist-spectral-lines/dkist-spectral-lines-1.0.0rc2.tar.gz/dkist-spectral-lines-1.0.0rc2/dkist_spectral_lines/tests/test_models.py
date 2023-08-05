"""Tests for the SpectralLine data structure and validation"""
import random

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


@pytest.fixture()
def valid_wavelength_metadata() -> dict:
    """Valid wavelength metadata"""
    wavelength = random.random()
    wavelength_max = wavelength + 1
    wavelength_min = wavelength - 1
    result = {
        "wavelength": wavelength,
        "wavelength_max": wavelength_max,
        "wavelength_min": wavelength_min,
    }
    return result


@pytest.fixture()
def valid_spectral_line(
    include_wavelength_name, valid_instrument, valid_line, valid_wavelength_metadata
) -> dict:
    """A valid spectral line definition"""

    result = {
        "instrument": valid_instrument,
        "line": valid_line,
        "include_wavelength_name": include_wavelength_name,
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
    expected_wavelength_min = valid_spectral_line["wavelength_min"]
    expected_wavelength_max = valid_spectral_line["wavelength_max"]
    expected_wavelength_width = expected_wavelength_max - expected_wavelength_min
    assert line.instrument == expected_instrument
    assert line.line == expected_line
    assert line.wavelength == expected_wavelength
    assert line.wavelength_min == expected_wavelength_min
    assert line.wavelength_max == expected_wavelength_max
    assert line.wavelength_width == expected_wavelength_width
    assert isinstance(line.name, str)
    assert isinstance(line.name_id, str)


@pytest.fixture()
def single_valid_spectral_line(valid_wavelength_metadata) -> dict:
    """A single valid set of spectral line data to be used as the baseline for negative tests"""
    result = {
        "instrument": instrument_enums[0],
        "line": line_enums[0],
        "include_wavelength_name": False,
    } | valid_wavelength_metadata
    return result


@pytest.mark.parametrize(
    "args",
    [
        pytest.param({"instrument": "FAKE_INSTRUMENT"}, id="invalid_instrument"),
        pytest.param({"line": "FAKE_LINE"}, id="invalid_line"),
        pytest.param(
            {"wavelength": 10, "wavelength_min": 11, "wavelength_max": 12},
            id="invalid_wavelength_min_combination",
        ),
        pytest.param(
            {"wavelength": 10, "wavelength_min": 8, "wavelength_max": 9},
            id="invalid_wavelength_max_combination",
        ),
        pytest.param(
            {"wavelength": 10, "wavelength_min": 11, "wavelength_max": 9},
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
