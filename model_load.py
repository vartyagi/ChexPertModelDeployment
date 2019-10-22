import torch
from torchvision import models, transforms
import torch.nn as nn


def get_model():
    num_classes = 5
    model = 'static/densenet_model.mdl'
    model_ft = models.densenet121()
    num_ftrs = model_ft.classifier.in_features
    model_ft.classifier = nn.Linear(num_ftrs, num_classes)
    model_ft.features[0] = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
    model_ft.load_state_dict(torch.load(model, map_location=torch.device('cpu')))

    return model_ft


def transform_image(image_read):
    my_transforms = transforms.Compose([
                    transforms.Resize((320, 320)),
                    transforms.ToTensor(),
                    transforms.Normalize([0.5247], [0.2769])
                    ])
    image = image_read
    return my_transforms(image)





