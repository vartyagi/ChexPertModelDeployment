from model_load import get_model, transform_image
import numpy as np
import torch

model = get_model()
model.eval()
labels_list = ['Cardiomegaly', 'Edema', 'Atelectasis', 'Pleural Effusion', 'Consolidation']
thresholds = [0.22, 0.56, 0.38, 0.31, 0.43]


def weighted_sig(x, thresholds):
    return [1 / (1 + np.exp(-1*(x[i] - 1*np.log((thresholds[i])/(1-thresholds[i]))))) for i in range(len(x))]


def get_prediction(image_read):
    tensor = transform_image(image_read)
    outputs = model(tensor.reshape((1, 1, 320, 320)))
    #outputs = torch.sigmoid(outputs)
    outputs = outputs.detach().numpy()
    outputs = weighted_sig(outputs, thresholds)
    y_hat = outputs[0]
    print({labels_list[i]: y_hat[i] for i in range(len(labels_list))})
    return {labels_list[i]: round(y_hat[i].item(),3) for i in range(len(labels_list))}
