"""Retrieval functions for spectral line discovery."""
from dkist_spectral_lines.lines import SPECTRAL_LINES
from dkist_spectral_lines.models import Instrument
from dkist_spectral_lines.models import SpectralLine


def _parse_instrument(instrument: Instrument | str | None) -> str | None:
    """Convert enum of instrument into a string."""
    if instrument is None:
        return
    if type(instrument) == str:
        return instrument
    return instrument.value


def find_spectral_lines(
    instrument: Instrument | str | None = None,
    wavelength: float | None = None,
    filter_id: str | None = None,
) -> list[SpectralLine]:
    """
    Retrieve all spectral lines that match the filter parameters.

    Parameters
    ----------
    instrument
        The instrument to filter by
    wavelength
        The wavelength to filter by where wavelength_min <= wavelength <= wavelength_max
    filter_id
        The filter id to filter by
    """
    result = [line for line in SPECTRAL_LINES]
    instrument = _parse_instrument(instrument=instrument)
    if instrument:
        result = [line for line in result if line.instrument == instrument]
    if wavelength:
        result = [line for line in result if line.filter_min <= wavelength <= line.filter_max]
    if filter_id:
        result = [line for line in result if line.filter_id == filter_id]
    return result


def identify_spectral_line(
    instrument: Instrument | str | None = None,
    wavelength: float | None = None,
    filter_id: str | None = None,
) -> SpectralLine | None:
    """
    Retrieve a single spectral line that match the filter parameters, raising an error if more than one is found.

    Parameters
    ----------
    instrument
        The instrument to filter by
    wavelength
        The wavelength to filter by where wavelength_min <= wavelength <= wavelength_max
    filter_id
        The filter id to filter by
    """
    lines = find_spectral_lines(instrument=instrument, wavelength=wavelength, filter_id=filter_id)
    line_count = len(lines)
    if line_count == 1:
        return lines[0]
    raise ValueError(f"{line_count} lines found matching the criteria.  Expected 1.")
