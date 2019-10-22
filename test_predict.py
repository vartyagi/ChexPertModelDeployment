import pandas as pd
from predict import get_prediction
import requests
from PIL import Image
from io import BytesIO

dir_ = '../CheXpert-v1.0-small'
df_valid = pd.read_csv(dir_+'/'+'valid.csv')
a = df_valid['Path'].str.split("/",expand=True)
df_valid['patient']=a[2].str.replace('patient','').astype(int)
df_valid['study'] = a[3].str.replace('study','').astype(int)
df_valid['view'] = a[4].str.split('_', expand=True)[0].str.replace('view','').astype(int)
df_valid = df_valid[df_valid['Frontal/Lateral'] == 'Frontal']
df_valid['NewPath'] = df_valid['Path']
df_valid = df_valid[['NewPath', 'Cardiomegaly', 'Edema', 'Atelectasis',
         'Pleural Effusion', 'Consolidation']]

file = '../' + df_valid.loc[226]['NewPath']

class_pred = get_prediction(Image.open(file).convert('L'))
print(class_pred)

url = "http://www.meddean.luc.edu/lumen/meded/medicine/pulmonar/cxr/atlas/images/318i.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-1/question_1_big.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-1/question_2_big.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-1/question_3_big.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-1/question_4_big.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-1/question_5_big.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-1/question_6_big.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-2/question_01_big.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-2/question_06_big.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-2/question_07_big.jpg"
url = "https://www.radiologymasterclass.co.uk/images/quizzes/Quiz-Images-Chest-2/question_09_big.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content)).convert('L')

class_pred = get_prediction(img)
print(class_pred)
