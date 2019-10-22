from model_load import get_model, transform_image
import torch
import numpy as np

model = get_model()
model.eval()
labels_list = ['Cardiomegaly', 'Edema', 'Atelectasis', 'Pleural Effusion', 'Consolidation']
thresholds = [0.37, 0.65, 0.43, 0.43, 0.52]


def get_prediction(image_read):
    tensor = transform_image(image_read)
    outputs = model(tensor.reshape((1, 1, 320, 320)))
    outputs = torch.sigmoid(outputs)
    outputs = np.array(outputs.detach().numpy())
    y_hat = (outputs[0] / thresholds) - 0.5
    y_hat = torch.sigmoid(torch.tensor(y_hat))
    return {labels_list[i]: float(y_hat[i].numpy()) for i in range(len(labels_list))}

