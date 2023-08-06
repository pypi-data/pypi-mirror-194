from typing import Generic, Iterable, List, Optional, TypeVar

from olympipe import Pipeline

T = TypeVar("T")


class OPipeline(Generic[T]):
    def __init__(self, source: Iterable[T]):
        self._data = source
        self.pipeline: Optional[Pipeline[T]] = None

    @staticmethod
    def load_folder(
        path: str, extensions: List[str] = [""], recursive: bool = False
    ) -> "OPipeline[T]":
        raise NotImplementedError()

    def wait_for_completion(self) -> None:
        if self.pipeline is None:
            return
        return self.pipeline.wait_for_completion()

    def wait_for_results(self) -> List[T]:
        if self.pipeline is None:
            return []
        return self.pipeline.wait_for_results()
