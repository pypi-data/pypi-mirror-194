import os
from glob import glob
from random import randint
from typing import Any, Callable, Generator, Iterable, List, Optional, Tuple, cast

import cv2  # type: ignore
from olympipe import Pipeline

from olympict.files.o_image import OlympImage
from olympict.files.o_video import OlympVid
from olympict.image_tools import ImTools
from olympict.pipeline import OPipeline
from olympict.types import (
    BBoxAbsolute,
    BBoxRelative,
    Color,
    Img,
    ImgFormat,
    LineAbsolute,
    LineRelative,
    PolygonAbsolute,
    PolygonRelative,
    Size,
)
from olympict.video_saver import PipelineVideoSaver


class ImagePipeline(OPipeline[OlympImage]):
    def __init__(self, data: Optional[Iterable[OlympImage]] = None):
        self.pipeline: Optional[Pipeline[OlympImage]] = None

        if data is not None:
            self.pipeline = Pipeline(data)

    @staticmethod
    def load_folder(
        path: str,
        extensions: List[str] = ["png", "jpg", "jpeg", "bmp"],
        recursive: bool = False,
        order_func: Optional[Callable[[str], int]] = None,
        reverse: bool = False,
        metadata_function: Optional[Callable[[str], Any]] = None,
    ) -> "ImagePipeline":
        paths: List[str] = glob(os.path.join(path, "**"), recursive=recursive)

        paths = [p for p in paths if os.path.splitext(p)[1].strip(".") in extensions]

        if order_func is not None:
            paths.sort(key=order_func, reverse=reverse)

        data = [OlympImage(p) for p in paths]

        if metadata_function is not None:
            for d in data:
                d.metadata = metadata_function(d.path)

        return ImagePipeline(data)

    @staticmethod
    def load_folders(
        paths: List[str],
        extensions: List[str] = ["png", "jpg", "jpeg", "bmp"],
        recursive: bool = False,
        order_func: Optional[Callable[[str], int]] = None,
        reverse: bool = False,
        metadata_function: Optional[Callable[[str], Any]] = None,
    ) -> "ImagePipeline":
        all_data: List[OlympImage] = []
        for path in paths:
            sub_paths: List[str] = glob(os.path.join(path, "**"), recursive=recursive)

            sub_paths = [
                p for p in sub_paths if os.path.splitext(p)[1].strip(".") in extensions
            ]

            if order_func is not None:
                sub_paths.sort(key=order_func, reverse=reverse)

            data = [OlympImage(p) for p in sub_paths]

            if metadata_function is not None:
                for d in data:
                    d.metadata = metadata_function(d.path)

            all_data.extend(data)

        return ImagePipeline(all_data)

    def task(
        self, func: Callable[[OlympImage], OlympImage], count: int = 1
    ) -> "ImagePipeline":
        output = ImagePipeline()
        if self.pipeline is None:
            raise Exception("Undefined pipeline")
        output.pipeline = self.pipeline.task(func, count)

        return output

    def task_img(self, func: Callable[[Img], Img], count: int = 1) -> "ImagePipeline":
        def r(o: OlympImage) -> OlympImage:
            o.img = func(o.img)
            return o

        return self.task(r, count)

    def task_path(self, func: Callable[[str], str], count: int = 1) -> "ImagePipeline":
        def r(o: OlympImage) -> OlympImage:
            o.path = func(o.path)
            return o

        return self.task(r, count)

    def rescale(
        self,
        size: Tuple[float, float],
        pad_color: Optional[Tuple[int, int, int]] = None,
        count: int = 1,
    ) -> "ImagePipeline":
        return self.task(OlympImage.rescale(size, pad_color), count)

    def resize(
        self,
        size: Tuple[int, int],
        pad_color: Optional[Tuple[int, int, int]] = None,
        interpolation: int = cv2.INTER_LINEAR,
        count: int = 1,
    ) -> "ImagePipeline":
        return self.task(OlympImage.resize(size, pad_color, interpolation), count)

    def crop(
        self,
        left: int = 0,
        top: int = 0,
        right: int = 0,
        bottom: int = 0,
        pad_color: Color = (0, 0, 0),
    ) -> "ImagePipeline":
        def r(img: Img) -> Img:
            return ImTools.crop_image(
                img, top=top, left=left, bottom=bottom, right=right, pad_color=pad_color
            )

        return self.task_img(r)

    def random_crop(
        self,
        output_size: Size,
    ) -> "ImagePipeline":
        def r(img: Img) -> Img:
            h, w, _ = img.shape
            t_w, t_h = output_size

            off_x = randint(0, w - t_w - 1)
            off_y = randint(0, h - t_h - 1)

            return img[off_y : off_y + t_h, off_x : off_x + t_w, :]

        return self.task_img(r)

    def keep_each_frame_in(
        self, keep_n: int = 1, discard_n: int = 0
    ) -> "ImagePipeline":
        if self.pipeline is None:
            raise Exception("No defined pipeline")

        def discarder():
            while True:
                for _ in range(keep_n):
                    yield True
                for _ in range(discard_n):
                    yield False

        d = discarder()

        def get_next(_: Any) -> bool:
            return next(d)

        output = ImagePipeline()
        output.pipeline = self.pipeline.filter(get_next)

        return output

    def debug_window(self, name: str) -> "ImagePipeline":
        def d(o: "OlympImage") -> "OlympImage":
            cv2.imshow(name, o.img)
            cv2.waitKey(1)
            return o

        return self.task(d)

    def to_video(
        self, img_to_video_path: Callable[[OlympImage], str]
    ) -> "VideoPipeline":
        output: VideoPipeline = VideoPipeline()
        output.pipeline = self.pipeline.class_task(  # type: ignore
            PipelineVideoSaver,
            PipelineVideoSaver.process_file,
            [img_to_video_path],
            PipelineVideoSaver.finish,
        )

        return output

    def to_format(self, format: ImgFormat) -> "ImagePipeline":
        def change_format(path: str) -> str:
            base, _ = os.path.splitext(path)

            fmt = f".{format}" if "." != format[0] else format

            return base + fmt

        return self.task_path(change_format)

    def save_to_folder(self, folder_path: str) -> "ImagePipeline":
        os.makedirs(folder_path, exist_ok=True)

        def s(o: "OlympImage") -> "OlympImage":
            o.change_folder_path(folder_path)
            o.save()
            return o

        return self.task(s)

    def save(self) -> "ImagePipeline":
        def s(o: "OlympImage") -> "OlympImage":
            o.save()
            return o

        return self.task(s)

    def draw_relative_polygons(
        self,
        polygon_function: Callable[[OlympImage], List[Tuple[PolygonRelative, Color]]],
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = polygon_function(o)
            for polygon, color in outputs:
                o.img = ImTools.draw_relative_polygon(o.img, polygon, color)
            return o

        return self.task(p)

    def draw_polygons(
        self,
        polygon_function: Callable[[OlympImage], List[Tuple[PolygonAbsolute, Color]]],
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = polygon_function(o)
            for polygon, color in outputs:
                o.img = ImTools.draw_polygon(o.img, polygon, color)
            return o

        return self.task(p)

    def draw_relative_bboxes(
        self, bbox_function: Callable[[OlympImage], List[Tuple[BBoxRelative, Color]]]
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = bbox_function(o)
            for polygon, color in outputs:
                o.img = ImTools.draw_relative_bbox(o.img, polygon, color)
            return o

        return self.task(p)

    def draw_bboxes(
        self, bbox_function: Callable[[OlympImage], List[Tuple[BBoxAbsolute, Color]]]
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            for polygon, color in bbox_function(o):
                o.img = ImTools.draw_bbox(o.img, polygon, color)
            return o

        return self.task(p)

    def draw_relative_lines(
        self,
        polyline_function: Callable[[OlympImage], List[Tuple[LineRelative, Color]]],
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = polyline_function(o)
            for line, color in outputs:
                o.img = ImTools.draw_relative_line(o.img, line, color)
            return o

        return self.task(p)

    def draw_lines(
        self,
        polyline_function: Callable[[OlympImage], List[Tuple[LineAbsolute, Color]]],
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = polyline_function(o)
            for line, color in outputs:
                o.img = ImTools.draw_line(o.img, line, color)
            return o

        return self.task(p)

    def draw_heatmap(
        self, heatmap_function: Callable[[OlympImage], Img]
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            outputs = heatmap_function(o)
            o.img = ImTools.draw_heatmap(o.img, outputs)
            return o

        return self.task(p)

    def draw_segmentation_maps(
        self, segmentation_map: Callable[[OlympImage], Img], color: Color
    ) -> "ImagePipeline":
        def p(o: "OlympImage") -> "OlympImage":
            seg_map = segmentation_map(o)
            o.img = ImTools.draw_segmentation_map(o.img, seg_map, color)
            return o

        return self.task(p)


class VideoPipeline(OPipeline[OlympVid]):
    def __init__(self, data: Optional[Iterable[OlympVid]] = None):
        self.pipeline: Optional[Pipeline[OlympVid]] = None
        if data is not None:
            self.pipeline = Pipeline(data)

    @staticmethod
    def load_folder(
        path: str,
        extensions: List[str] = ["mkv", "mp4"],
        recursive: bool = False,
        order_func: Optional[Callable[[str], int]] = None,
        reverse: bool = False,
    ) -> "VideoPipeline":
        paths: List[str] = glob(os.path.join(path, "**"), recursive=recursive)
        paths = [p for p in paths if os.path.splitext(p)[1].strip(".") in extensions]

        if order_func is not None:
            paths.sort(key=order_func, reverse=reverse)

        data = [OlympVid(p) for p in paths]

        return VideoPipeline(data)

    def task(
        self, func: Callable[[OlympVid], OlympVid], count: int = 1
    ) -> "VideoPipeline":
        return self.task(func, count)

    def move_to_folder(self, folder_path: str) -> "VideoPipeline":
        os.makedirs(folder_path, exist_ok=True)

        def s(o: "OlympVid") -> "OlympVid":
            o.change_folder_path(folder_path)
            return o

        return self.task(s)

    def to_sequence(self) -> "ImagePipeline":
        if self.pipeline is None:
            raise Exception("No defined pipeline")

        def generator(o: "OlympVid") -> Generator[OlympImage, None, None]:
            capture: Any = cv2.VideoCapture(o.path)
            res, frame = cast(Tuple[bool, Img], capture.read())
            idx = 0
            while res:
                new_path = f"{o.path}_{idx}.png"
                yield OlympImage.from_buffer(
                    frame, new_path, {"video_path": o.path, "video_frame": idx}
                )
                res, frame = cast(Tuple[bool, Img], capture.read())
                idx += 1

        output = ImagePipeline()
        output.pipeline = self.pipeline.explode(generator)

        return output
