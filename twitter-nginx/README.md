# twitter-nginx

to allow hosting multiple docker sites in same droplet, we should create multiple sites exposed on port 80 [dockerhub link](https://hub.docker.com/repository/docker/nathanesau/twitter-clone)

docker instructions:

```bash
# build the image
docker build -t twitter-nginx .

# run the image
docker run -p 80:80 -p 443:443 --name twitter-nginx --restart always -d twitter-nginx

# push to docker hub
docker tag twitter-nginx nathanesau/twitter-clone:twitter-nginx
docker push nathanesau/twitter-clone:twitter-nginx
```

install nginx as service:

```bash
# install nginx
sudo apt-get install nginx

# start nginx
sudo systemctl enable nginx

# configuration
# TODO add site to /etc/nginx/sites-enabled/mysite or similar
# TODO remove /etc/nginx/sites-enabled/default

# check configuration
nginx -t 

# reload
service nginx reload
```
