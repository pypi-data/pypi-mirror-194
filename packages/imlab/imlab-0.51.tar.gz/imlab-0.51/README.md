# iMLab - 

Imlab is a library which simplify the use of some image deep learning models such as yolo,resnet, densenet, etc ...

Imlab use [tensorflow](https://www.tensorflow.org/) and [pytorch](https://pytorch.org/).


## Installation


Using [pip](https://pip.pypa.io/en/stable/).


```bash
pip install imlab
```
or
```bash
git clone ...
pip install imlab/
```

## Usage


Default model is [yoloV7](https://github.com/WongKinYiu/yolov7/) trained on coco dataset

```python
from imlab import iml

result=iml(image)
for bouding_box,classe in result:
    print(bounding_box,classe)



```

```bash
imlab image --show
```

## Documentation / Explanation

You can check more information about my projects on my [website](https://thomasportier.com/)

You can check the documentation on [doc](https://doc.thomasportier.com/imlab/)

## License
[MIT](https://github.com/ts0mas/wordbay/blob/master/LICENSE.md)
