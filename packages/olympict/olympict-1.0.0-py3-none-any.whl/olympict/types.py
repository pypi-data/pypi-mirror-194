import sys
from typing import Any, List, Literal, Tuple, Type, TypeVar, Union

import cv2  # type: ignore
import numpy as np

PointRelative = Tuple[float, float]
"""PointRelative
is a tuple composed of:
x: [0-1] float
y: [0-1] float
"""

PointAbsolute = Tuple[int, int]
"""PointAbsolute
is a tuple composed of:
x: [0-width] int
y: [0-height] int
"""

BBoxRelative = Tuple[float, float, float, float, str, float]
"""BBoxRelative
is a tuple composed of:
x1: [0-1] float
y1: [0-1] float
x2: [0-1] float
y2: [0-1] float
class: str
confidence: [0-1] float
"""

BBoxAbsolute = Tuple[int, int, int, int, str, float]
"""BBoxAbsolute
is a tuple composed of:
x1: [0-width] int
y1: [0-height] int
x2: [0-width] int
y2: [0-height] int
class: str
confidence: [0-1] float
"""

PolygonRelative = List[PointRelative]
"""PolygonRelative
A list of PointsRelative to draw a filled shape
"""


PolygonAbsolute = List[PointAbsolute]
"""PolygonAbsolute
A list of PointsAbsolute to draw a filled shape
"""


LineRelative = List[PointRelative]
"""LineRelative
A list of PointsRelative to be joined by a segment
"""

LineAbsolute = List[PointAbsolute]
"""LineAbsolute
A list of PointsAbsolute to be joined by a segment
"""


ImgFormat = Literal["png", "jpeg", "bmp"]
VidFormat = Literal["mp4", "mkv", "avi"]

Size = Tuple[int, int]
"""Size
is a tuple dedicated to image sizing:
w: int image width in pixels
h: int image height in pixels
"""

Color = Tuple[int, int, int]
"""Color
is a tuple dedicated to color representation using BGR format
b: [0-255] int blue channel
g: [0-255] int green channel
r: [0-255] int red channel
"""

TYPE_CHECKING = False
ScalarType = TypeVar("ScalarType", bound=np.generic, covariant=True)

if TYPE_CHECKING or sys.version_info >= (3, 9):
    _DType = np.dtype[ScalarType]
    NDArray = np.ndarray[Any, np.dtype[ScalarType]]
    Img = Union[cv2.Mat, NDArray[np.uint8]]
else:
    Img = Type[cv2.Mat]
"""Img
represents the image format, usually a numpy uint8 array or a cv2.Mat
"""
