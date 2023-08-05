"""Spectral line data structures."""
from enum import Enum

from pydantic import BaseModel
from pydantic import validator


class Instrument(str, Enum):
    """Controlled list of values for an instrument."""

    VBI_BLUE = "VBI-Blue"
    VBI_RED = "VBI-Red"
    VISP = "VISP"
    CRYO_NIRSP_SP = "CRYO-NIRSP-SPECTRAL"
    CRYO_NIRSP_CI = "CRYO-NIRSP-CONTEXT"


class Line(str, Enum):
    """Controlled list of values for a line."""

    CALCIUM_ONE = "Ca I"
    CALCIUM_TWO = "Ca II"
    CALCIUM_TWO_HYDROGEN = "Ca II H"
    CALCIUM_TWO_POTASSIUM = "Ca II K"
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
    wavelength_min
        The minimum wavelength of the spectral line
    wavelength_max
        The maximum wavelength of the spectral line
    include_wavelength_in_name
        Flag indicating whether to include the wavelength in the name of the SpectralLine to make it uniquely named. e.g. for CRYO-NIRSP-CONTEXT-Fe-XIII
    """

    instrument: Instrument
    line: Line
    wavelength_min: float
    wavelength_max: float
    wavelength: float
    include_wavelength_in_name: bool = False

    @validator("wavelength")
    def logical_wavelength_range(cls, v, values):
        """Validate the wavelength and associated boundaries are consistent with each other."""
        if not (values["wavelength_min"] <= v <= values["wavelength_max"]):
            raise ValueError(
                "'wavelength_min' must be smaller than 'wavelength' which must be smaller than 'wavelength_max'"
            )
        return v

    @property
    def wavelength_width(self) -> float:
        """Return the width of the wavelength range associated with this spectral line."""
        return self.wavelength_max - self.wavelength_min

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
