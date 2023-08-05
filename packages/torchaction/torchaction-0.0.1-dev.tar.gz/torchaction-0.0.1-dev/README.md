# pytorch basic frame
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

Action for training/test using pytorch.

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

By providing datasets, configuration files, and some scripts, you can use this framework to get results without refactoring the code.

## Getting Started <a name = "getting_started"></a>

### Prerequisites
```
# pip install
PyYAML
tqdm
torch
torchmetrics
tensorboardX
```

### Installing
```
pip install torchaction
```


## Usage <a name = "usage"></a>

### arguments
for datasets:
+ root: root path of dataset relative to cwd, eg. 'datasets/'.
+ classes: a list of class names, eg. [cat,dog,fish]. Put this attribute in your dataset is recommand.
+ split_rate: rate for split datasets, eg. [0.7,0.3]

for train:
+ gpus: gpus that used, default is [] (means cpu), [0] or [0,1] is ok.
+ epochs
+ batch_size
+ lr

for save results:
+ save_name: str for save model name
+ save_suffix: eg. tar, pth

for config in yaml/yml file:
+ config: path of config file, eg. config.yml.

Defining other arguments in your config file is permitted.

priority:
cmd line > config.yml > default

### demo
```python
import torch
from torch.utils.data import Subset
from torchvision.datasets import MNIST
from torchvision.models import resnet34
from torchvision import transforms
import torchmetrics
from torchaction.actions import BasicAction
import random

project = BasicAction()
# prepare data
transform = transforms.ToTensor()
target_transform = lambda x: torch.tensor(x, dtype=torch.long)
project.dataset = MNIST(
    root="datasets",
    train=True,
    download=True,
    transform=transform,
    target_transform=target_transform,
)
indices=list(range(len(project.dataset)))
random.shuffle(indices)
project.dataset = Subset(project.dataset,indices[:100])
# prepare model
project.model = resnet34()
project.model.fc = torch.nn.Linear(
    project.model.fc.in_features, project.NUM_CLASSES
)
project.model = torch.nn.Sequential(torch.nn.Conv2d(1, 3, 3, 1), project.model)
# prepare train
project.loss_fun=torch.nn.CrossEntropyLoss()
project.optimizer=torch.optim.Adam(project.model.parameters(),project.LR)
# prepare metrics
project.output_formater=lambda x: torch.max(x,dim=1).indices
project.train_metrics={
    'acc':torchmetrics.Accuracy(task="multiclass",num_classes=project.NUM_CLASSES),
    'prec':torchmetrics.Precision(task="multiclass",num_classes=project.NUM_CLASSES),
    'recall':torchmetrics.Recall(task="multiclass",num_classes=project.NUM_CLASSES),
    'f1':torchmetrics.F1Score(task="multiclass",num_classes=project.NUM_CLASSES),
}
project.valid_metrics={
    'acc':torchmetrics.Accuracy(task="multiclass",num_classes=project.NUM_CLASSES),
    'prec':torchmetrics.Precision(task="multiclass",num_classes=project.NUM_CLASSES),
    'recall':torchmetrics.Recall(task="multiclass",num_classes=project.NUM_CLASSES),
    'f1':torchmetrics.F1Score(task="multiclass",num_classes=project.NUM_CLASSES),
}
# prepare save
project.best_ckpt_selectors=['acc']
project.train()
```
