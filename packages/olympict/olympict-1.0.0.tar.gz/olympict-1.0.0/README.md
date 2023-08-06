# Olympict

![coverage](https://gitlab.com/gabraken/olympict/badges/master/coverage.svg?job=tests)![status](https://gitlab.com/gabraken/olympict/badges/master/pipeline.svg)

![Olympict](https://gitlab.com/gabraken/olympict/-/raw/master/Olympict.png)


Based on [olympipe](https://pypi.org/project/olympipe/), this project will make image processing pipelines easy to use using the basic multiprocessing module. 
This module uses type checking to ensure your data process validity from the start.

## Basic image processing pipeline

### Loading images from a folder and resize them to a new folder

```python
from olympict import ImagePipeline

p0 = ImagePipeline.load_folder("./examples") # path containing the images
p1 = p0.resize((150, 250)) # new width, new height
p2 = p1.save_to_folder("./resized_examples") # path to save the images
p2.wait_for_completion() # the code blocks here until all images are processed

print("Finished resizing")
```

### Loading images from a folder and overwrite them with a new size

```python
from olympict import ImagePipeline

p0 = ImagePipeline.load_folder("./examples") # path containing the images
p1 = p0.resize((150, 250))
p2 = p1.save() # overwrite the images
p2.wait_for_completion()
```

### Loading images from a folder and resize them keeping the aspect ratio using a padding color

```python
from olympict import ImagePipeline
blue = (255, 0, 0) # Colors are BGR to match opencv format

p0 = ImagePipeline.load_folder("./examples")
p1 = p0.resize((150, 250), pad_color=blue)
p2 = p1.save() # overwrite the images
p2.wait_for_completion()
```

### Load image to make a specific operation

```python
from olympict import ImagePipeline, Img

def operation(image: Img) -> Img:
    # set the green channel as a mean of blue and red channels
    img[:, :, 1] = (img[:, :, 0] + img[:, :, 2]) / 2
    return img

p0 = ImagePipeline.load_folder("./examples")
p1 = p0.task_img(operation)
p2 = p1.save() # overwrite the images
p2.wait_for_completion()
```


### Check ongoing operation

```python
from olympict import ImagePipeline, Img

def operation(image: Img) -> Img:
    # set the green channel as a mean of blue and red channels
    img[:, :, 1] = (img[:, :, 0] + img[:, :, 2]) / 2
    return img

p0 = ImagePipeline.load_folder("./examples").debug_window("Raw image")
p1 = p0.task_img(operation).debug_window("Processed image")
p2 = p1.save() # overwrite the images
p2.wait_for_completion()
```

### Load a video and process each individual frame

```python
from olympict import VideoPipeline

p0 = VideoPipeline.load_folder("./examples") # will load .mp4 and .mkv files

p1 = p0.to_sequence() # split each video frame into a basic image

p2 = p1.resize((100, 3), (255, 255, 255)) # resize each image with white padding

p3 = p2.save_to_folder("./sequence") # save images individually

p3.wait_for_completion()

img_paths = glob("./sequence/*.png") # count images

print("Number of images:", len(img_paths))
```


### Complex example with preview windows
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

    def generator():
        for i in range(96):
            img = np.zeros((256, 256, 3), np.uint8)
            img[i, :, :] = (255, 255, 255)

            o = OlympImage()
            o.path = f'/tmp/{i}.png'
            o.img = img
            yield o
        return

    p = (
        ImagePipeline(generator())
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


## Basic usage

Each pipeline starts from an interator as a source of packets (a list, tuple, or any complex iterator). This pipeline will then be extended by adding basic `.task(<function>)`. The pipeline process join the main process when using the `.wait_for_results()` or `.wait_for_completion()` functions.

```python

from olympict import Pipeline

def times_2(x: int) -> int:
    return x * 2

p = Pipeline(range(10))

p1 = p.task(times_2) # Multiply each packet by 2
# or 
p1 = p.task(lambda x: x * 2) # using a lambda function

res = p1.wait_for_results()

print(res) # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

```


## Filtering

You can choose which packets to `.filter(<keep_function>)` by passing them a function returning True or False when applied to this packet.

```python

from olympict import Pipeline

p = Pipeline(range(20))
p1 = p.filter(lambda x: x % 2 == 0) # Keep pair numbers
p2 = p1.batch(2) # Group in arrays of 2 elements

res = p2.wait_for_results()

print(res) # [[0, 2], [4, 6], [8, 10], [12, 14], [16, 18]]

```

## In line formalization

You can chain declarations to have a more readable pipeline.

```python

from olympict import Pipeline

res = Pipeline(range(20)).filter(lambda x: x % 2 == 0).batch(2).wait_for_results()

print(res) # [[0, 2], [4, 6], [8, 10], [12, 14], [16, 18]]

```

## Debugging

Interpolate `.debug()` function anywhere in the pipe to print packets as they arrive in the pipe.

```python
from olympict import Pipeline

p = Pipeline(range(20))
p1 = p.filter(lambda x: x % 2 == 0).debug() # Keep pair numbers
p2 = p1.batch(2).debug() # Group in arrays of 2 elements

p2.wait_for_completion()
```

## Pipeline forking

For the time being, you have to adapt the code a little bit if you wish to get several outputs for a same pipeline. [This section might be updated soon]

```python
from olympict import Pipeline

p1 = Pipeline(range(10))
p2 = p1.filter(lambda x: x % 2 == 0)
p3 = p1.filter(lambda x: x % 2 == 1)

q2 = p2.prepare_output_buffer()
q3 = p3.prepare_output_buffer()

res3 = p3.wait_for_results(q3)
res2 = p2.wait_for_results(q2)

print(res3) # [1, 3, 5, 7, 9]
print(res2) # [0, 2, 4, 6, 8]

```

## Real time processing (for sound, video...)

Use the `.temporal_batch(<seconds_float>)` pipe to aggregate packets received at this point each <seconds_float> seconds.

```python
import time
from olympict import Pipeline

def delay(x: int) -> int:
    time.sleep(0.1)
    return x

p = Pipeline(range(20)).task(delay) # Wait 0.1 s for each queue element
p1 = p.filter(lambda x: x % 2 == 0) # Keep pair numbers
p2 = p1.temporal_batch(1.0) # Group in arrays of 2 elements

res = p2.wait_for_results()

print(res) # [[0, 2, 4, 6, 8], [10, 12, 14, 16, 18], []]
```

## Using classes in a pipeline

You can add a stateful class instance to a pipeline. The method used will be typecheked as well to ensure data coherence. You just have to use the `.class_task(<Class>, <Class.method>, ...)` method where Class.method is the actual method you will use to process each packet.

```python
item_count  = 5

class StockPile:
    def __init__(self, mul:int):
        self.mul = mul
        self.last = 0
        
    def pile(self, num: int) -> int:
        out = self.last
        self.last = num * self.mul
        return out
        

p1 = Pipeline(range(item_count))

p2 = p1.class_task(StockPile, StockPile.pile, [3])

res = p2.wait_for_results()

print(res) # [0, 0, 3, 6, 9]

```


This project is still an early version, feedback is very helpful.