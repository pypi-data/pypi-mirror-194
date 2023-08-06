"""Spectral line data structures."""
from enum import Enum

from pydantic import BaseModel
from pydantic import validator


class Instrument(str, Enum):
    """Controlled list of values for an instrument."""

    VBI_BLUE = "VBI-Blue"
    VBI_RED = "VBI-Red"
    VISP = "VISP"
    CRYO_NIRSP_SP = "CRYO-NIRSP-SPECTROGRAPH"
    CRYO_NIRSP_CI = "CRYO-NIRSP-IMAGER"


class Line(str, Enum):
    """Controlled list of values for a line."""

    CALCIUM_ONE = "Ca I"
    CALCIUM_TWO = "Ca II"
    CALCIUM_TWO_H = "Ca II H"
    CALCIUM_TWO_K = "Ca II K"
    CARBON_MONOXIDE = "CO"
    CONTINUUM = "Continuum"
    IRON_ONE = "Fe I"
    IRON_NINE = "Fe IX"
    IRON_TWELVE = "Fe XII"
    IRON_THIRTEEN = "Fe XIII"
    G_BAND = "G-band"
    HYDROGEN_ALPHA = "H-alpha"
    HYDROGEN_BETA = "H-beta"
    HYDROGEN_DELTA = "H-delta"
    HYDROGEN_GAMMA = "H-gamma"
    HELIUM_ONE = "He I"
    HELIUM_ONE_D_ONE = "He I d1"
    HELIUM_ONE_D_TWO = "He I d2"
    HELIUM_ONE_D_THREE = "He I d3"
    HELIUM_ONE_IRON_THIRTEEN = "He I, Fe XIII"
    J_BAND = "J-band"
    MAGNESIUM_ONE_B_ONE = "Mg I b1"
    MAGNESIUM_ONE_B_TWO = "Mg I b2"
    MAGNESIUM_EIGHT = "Mg VIII"
    PASCHEN_BETA = "Paschen-beta"
    SULFUR_NINE = "S IX"
    SILICON_NINE = "Si IX"
    SILICON_TEN = "Si X"
    TITANIUM_OXIDE = "TiO"


class SpectralLine(BaseModel):
    """
    The SpectralLine data structure encapsulates wavelength metadata that are the result of light observed through filters used in specific DKIST instruments.

    Parameters
    ----------
    instrument
        The instrument the spectral line belongs is for
    line
        The instrument agnostic name of the spectral line
    wavelength
        The center wavelength of the spectral line
    filter_min
        The minimum wavelength of the spectral line filter
    filter_max
        The maximum wavelength of the spectral line filter
    filter_id
        A unique identifier to help distinguish Spectral Lines for the same instrument and filter range
    include_wavelength_in_name
        Flag indicating whether to include the wavelength in the name of the SpectralLine to make it uniquely named. e.g. for CRYO-NIRSP-CONTEXT-Fe-XIII
    """

    instrument: Instrument
    line: Line
    filter_min: float
    filter_max: float
    wavelength: float
    filter_id: str | None = None
    include_wavelength_in_name: bool = False

    @validator("wavelength")
    def logical_filter_wavelength_range(cls, v, values):
        """Validate the wavelength and associated filter boundaries are consistent with each other."""
        if not (values["filter_min"] <= v <= values["filter_max"]):
            raise ValueError(
                "'filter_min' must be smaller than 'wavelength' which must be smaller than 'filter_max'"
            )
        return v

    @property
    def filter_width(self) -> float:
        """Return the width of the wavelength range associated with this spectral line."""
        return self.filter_max - self.filter_min

    @property
    def name(self) -> str:
        """Return the name in a display friendly format."""
        if self.include_wavelength_in_name:
            return f"{self.instrument} {self.line} {self.wavelength} nm"
        return f"{self.instrument} {self.line}"

    @property
    def name_id(self) -> str:
        """Return the name in an id friendly format."""
        return self.name.replace(" ", "-")
