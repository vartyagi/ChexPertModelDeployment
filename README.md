# X-Ray Image Classification Model Deployment Test
## Files for model deployment

* app.py - flask app
* model_load.py - functions to load model and transform images
* predict.py - function to generate prediction
* static directory - contains test images + labels, model
* templates directory - contains index.html template


## Instructions to start Docker container
```
docker build -t chexpert_prediction .
docker run --detach -p 5000:5000 chexpert_prediction
```

* Open browser to:

http://localhost:5000/


## API prediction for local X-Ray image file:
```
curl -X POST -F image=@<file-path> 'http://localhost:5000/predict'
```
