"""Test spectral line discovery functions."""
import pytest

from dkist_spectral_lines import find_spectral_lines
from dkist_spectral_lines import identify_spectral_line
from dkist_spectral_lines import Instrument
from dkist_spectral_lines import Line
from dkist_spectral_lines import SpectralLine


@pytest.fixture(autouse=True)
def spectral_line_data(mocker):
    """Spectral Line test data to use when validating the find functions."""
    lines = (
        SpectralLine(
            line=Line.IRON_ONE,
            wavelength=630.2,
            filter_min=630.195,
            filter_max=630.206,
            instrument=Instrument.VISP,
        ),
        SpectralLine(
            line=Line.HYDROGEN_ALPHA,
            wavelength=656.28,
            filter_min=656.13,
            filter_max=656.43,
            instrument=Instrument.VISP,
        ),
        SpectralLine(
            line=Line.CALCIUM_TWO,
            wavelength=854.21,
            filter_min=854.11,
            filter_max=854.31,
            instrument=Instrument.VISP,
            filter_id="visp_filter_name",
        ),
        # Cryp SP
        SpectralLine(
            line=Line.CALCIUM_TWO,
            wavelength=854.000,
            filter_min=848.000,
            filter_max=860.000,
            instrument=Instrument.CRYO_NIRSP_SP,
        ),
        SpectralLine(
            line=Line.CALCIUM_TWO_K,
            wavelength=854.000,
            filter_min=848.000,
            filter_max=860.000,
            instrument=Instrument.CRYO_NIRSP_SP,
            filter_id="cryo_filter_name",
        ),
        SpectralLine(
            line=Line.HELIUM_ONE_IRON_THIRTEEN,
            wavelength=1077.000,
            filter_min=1067.000,
            filter_max=1087.000,
            instrument=Instrument.CRYO_NIRSP_SP,
        ),
    )
    mocker.patch("dkist_spectral_lines.find.SPECTRAL_LINES", new=lines)


@pytest.mark.parametrize(
    "instrument, wavelength, filter_id, expected_record_count",
    [
        pytest.param(Instrument.VISP.value, None, None, 3, id="instrument_str_found"),
        pytest.param(None, 854.12, None, 3, id="wavelength_found"),
        pytest.param(
            Instrument.VISP.value, 854.12, None, 1, id="instrument_str_plus_wavelength_found"
        ),
        pytest.param(Instrument.VBI_BLUE.value, None, None, 0, id="instrument_str_not_found"),
        pytest.param(None, 99, None, 0, id="wavelength_not_found"),
        pytest.param(
            Instrument.VBI_BLUE.value, 99, None, 0, id="instrument_str_plus_wavelength_not_found"
        ),
        pytest.param(Instrument.VISP, None, None, 3, id="instrument_enum_found"),
        pytest.param(
            Instrument.VISP, None, "visp_filter_name", 1, id="instrument_enum_plus_filter_id_found"
        ),
        pytest.param(Instrument.VISP, 854.12, None, 1, id="instrument_enum_plus_wavelength_found"),
        pytest.param(Instrument.VBI_BLUE, None, None, 0, id="instrument_enum_not_found"),
        pytest.param(
            Instrument.VBI_BLUE, 99, None, 0, id="instrument_enum_plus_wavelength_not_found"
        ),
    ],
)
def test_find_spectral_lines(
    instrument: str, wavelength: float, filter_id: str, expected_record_count
):
    """
    :Given: Spectral line data and Spectral line filter parameters
    :When: Finding spectral lines
    :Then: The expected number of SpectralLine records are retrieved
    """
    lines = find_spectral_lines(instrument=instrument, wavelength=wavelength, filter_id=filter_id)
    assert all([isinstance(l, SpectralLine) for l in lines])
    assert len(lines) == expected_record_count


@pytest.mark.parametrize(
    "instrument, wavelength, filter_id",
    [
        pytest.param(
            Instrument.CRYO_NIRSP_SP, 1077.0, None, id="unique_instrument_plus_wavelength"
        ),
        pytest.param(
            Instrument.CRYO_NIRSP_SP,
            850.0,
            "cryo_filter_name",
            id="unique_instrument_plus_wavelength_plus_filter_id",
        ),
    ],
)
def test_identify_spectral_line(instrument: str, wavelength: float, filter_id: str):
    """
    :Given: Spectral line data and Spectral line filter parameters
    :When: Filtering for a single spectral line
    :Then: A single Spectral line record is retrieved
    """
    line = identify_spectral_line(instrument=instrument, wavelength=wavelength, filter_id=filter_id)
    assert isinstance(line, SpectralLine)


def test_identify_spectral_line_too_many():
    """
    :Given: Spectral line data and Spectral line filter parameters
    :When: Filtering for a single spectral line but expecting >1
    :Then: A ValueError is raised
    """
    with pytest.raises(ValueError):
        identify_spectral_line(instrument=Instrument.VISP)


def test_identify_spectral_line_none():
    """
    :Given: Spectral line data and Spectral line filter parameters
    :When: Filtering for a single spectral line but expecting noe to be found
    :Then: None is returned
    """
    with pytest.raises(ValueError):
        identify_spectral_line(instrument=Instrument.VBI_BLUE)
