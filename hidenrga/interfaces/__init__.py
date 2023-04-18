from .stream_interface import HidenRGAStreamInterface
from ..devices import SimulatedHidenRGA

__all__ = ['HidenRGAStreamInterface']
setups = dict(
    scanning=dict(
        device_type=SimulatedHidenRGA,
    )
)