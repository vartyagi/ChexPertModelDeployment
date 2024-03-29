from flask import Flask, jsonify, request, render_template
from predict import get_prediction
import pandas as pd
import os
from PIL import Image
from io import BytesIO
import requests


dir_ = 'static/CheXpert-v1.0-small'
df_valid = pd.read_csv(dir_+'/'+'valid.csv')
a = df_valid['Path'].str.split("/", expand=True)
df_valid['patient']=a[2].str.replace('patient', '').astype(int)
df_valid['study'] = a[3].str.replace('study', '').astype(int)
df_valid['view'] = a[4].str.split('_', expand=True)[0].str.replace('view', '').astype(int)
df_valid = df_valid[df_valid['Frontal/Lateral'] == 'Frontal']
df_valid['NewPath'] = df_valid['Path']
df_valid = df_valid[['NewPath', 'Cardiomegaly', 'Edema', 'Atelectasis',
         'Pleural Effusion', 'Consolidation']]

files = df_valid['NewPath'].values
application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = 'static'
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@application.route("/")
def hello():
    listStatus = [(id, filename) for id, filename in enumerate(files)]
    default = 201
    img = os.path.join('static', files[0])
    return render_template('index.html', listStatus=listStatus, default=default, img1=img)


@application.route('/predict', methods=['POST'])
def predict():
    # for external API calls
    if request.method == 'POST':
        file = request.files['file']
        file = Image.open(file).convert('L')
        class_pred = get_prediction(file)
        return jsonify(class_pred)


@application.route("/test", methods=['GET', 'POST'])
def test():
    # for test images
    listStatus = [(id, filename) for id, filename in enumerate(files)]
    select = request.form.get('image_select')
    select = int(select)
    file = os.path.join('static', files[select])
    class_pred = get_prediction(Image.open(file).convert('L'))
    true_label = df_valid.iloc[select].drop(['NewPath']).to_dict()
    model_output = [(key, class_pred[key], true_label[key]) for key in class_pred.keys()]
    return render_template('index.html', listStatus=listStatus, default=select, img1=file, model_output=model_output)


@application.route("/url_input" , methods=['GET', 'POST'])
def url_input():
    # for URL inputs
    select = request.form.get('url_select')
    response = requests.get(select)
    file = BytesIO(response.content)
    class_pred = get_prediction(Image.open(file).convert('L'))
    model_output = [(key, class_pred[key], '?') for key in class_pred.keys()]
    listStatus = [(id, filename) for id, filename in enumerate(files)]
    default = 201
    return render_template('index.html', listStatus=listStatus, default=default, img1=select, model_output=model_output)


@application.route("/file_input" , methods=['GET', 'POST'])
def file_input():
    # for file inputs

    file = request.files['file_select']
    file.save(os.path.join(application.config['UPLOAD_FOLDER'], 'tmp.jpg'))
    class_pred = get_prediction(Image.open(file).convert('L'))
    select2 = os.path.join(application.config['UPLOAD_FOLDER'], 'tmp.jpg')

    model_output = [(key, class_pred[key], '?') for key in class_pred.keys()]
    listStatus = [(id, filename) for id, filename in enumerate(files)]
    default = 201
    return render_template('index.html', listStatus=listStatus, default=default, img1=select2, model_output=model_output)

if __name__ == '__main__':
    application.run(debug=False, port=int(os.environ.get('PORT', 5000)), extra_files=['./static/tmp.jpg'])
