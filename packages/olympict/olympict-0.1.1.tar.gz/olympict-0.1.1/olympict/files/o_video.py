from typing import Optional
from olympict.files.o_file import OlympFile
from olympict.files.o_image import OlympImage
from olympict.types import VidFormat


class OlympVid(OlympFile):
    __id = 0

    def __init__(self, path: Optional[str] = None):
        super().__init__(path)
        if path is None:
            self._tmp_path = f"./{self.__id}.mp4"
            self.__id += 1
        self._tmp_path = ""
        self._fps = 25

    def get_fps(
        self,
    ) -> int:
        raise NotImplementedError()

    def to_format(self, fmt: VidFormat) -> "OlympImage":
        raise NotImplementedError()

    def get_temp_path(self) -> str:
        raise NotImplementedError()
