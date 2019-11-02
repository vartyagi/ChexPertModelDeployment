# X-Ray Image Classification Model Deployment Test
## Files for model deployment

* app.py - flask app
* model_load.py - functions to load model and transform images
* predict.py - function to generate prediction
* static directory - contains test images + labels, model
* templates directory - contains index.html template


## Instructions to start Docker container

docker build -t chexpert_prediction .

docker run --detach -p 5000:5000 chexpert_prediction


## Instructions to start docker service using nginx
Example from https://medium.com/@kmmanoj/deploying-a-scalable-flask-app-using-gunicorn-and-nginx-in-docker-part-2-fb33ec234113

* Initialize a swarm:

docker swarm init

* Create a virtual network:

docker network create web_network \
--driver overlay \
--subnet=192.168.100.0/24

* Create a docker volume

docker volume create web_static

* Create the web application service:

docker service create \
--name webapp \
--replicas 3 \
--mount src=web_static,dst=/app/static \
--network web_network \
varun/chexpert_prediction

* Create the web proxy service:

docker service create \
--name webproxy \
--network web_network \
--mount src=web_static,dst=/var/www-data \
--mount type=bind,src=/path/to/nginx_conf,dst=/etc/nginx/conf.d \
-p 5000:5000 \
nginx

* Verify by running:

docker network inspect web_network

* Open browser to:
http://localhost:5000/
