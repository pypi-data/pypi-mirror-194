# Olympict

![coverage](https://gitlab.com/superjambon/olympict/badges/master/coverage.svg?job=tests)![status](https://gitlab.com/superjambon/olympict/badges/master/pipeline.svg)

![Olympict](https://gitlab.com/superjambon/olympict/-/raw/master/Olympict.png)


This project will make image processing pipelines 
easy to use using the basic multiprocessing module. This module uses type checking to ensure your data process validity from the start.


###



```python
import os
from random import randint
import re
import time
from olympict import ImagePipeline
from olympict.files.o_image import OlympImage


def img_simple_order(path: str) -> int:
    number_pattern = r"\d+"
    res = re.findall(number_pattern, os.path.basename(path))

    return int(res[0])


if __name__ == "__main__":

    def wait(x: OlympImage):
        time.sleep(0.1)
        print(x.path)
        return x

    p = (
        ImagePipeline.load_folder("./examples", order_func=img_simple_order)
        .task(wait)
        .debug_window("start it")
        .task_img(lambda x: x[::-1, :, :])
        .debug_window("flip it")
        .keep_each_frame_in(1, 3)
        .debug_window("stuttered")
        .draw_bboxes(
            lambda x: [
                (
                    (
                        randint(0, 50),
                        randint(0, 50),
                        randint(100, 200),
                        randint(100, 200),
                        "change",
                        0.5,
                    ),
                    (randint(0, 255), 25, 245),
                )
            ]
        )
        .debug_window("bboxed")
    )

    p.wait_for_completion()

```


