"""Package initialization."""
try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version

from wetsuit.models import WetsuitClassifier, WetsuitRegressor
from wetsuit.transforms import H2oFrameTransformer

__version__ = version("wetsuit")
