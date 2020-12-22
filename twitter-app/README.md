# twitter-app

start up flask app using port 5000 [dockerhub link](https://hub.docker.com/repository/docker/nathanesau/twitter-clone)

```bash
# build the image
docker build -t twitter-app .

# run the image
docker run -p 5000:5000 --name twitter-app -d twitter-app

# push to docker hub
docker tag twitter-app nathanesau/twitter-clone:twitter-app
docker push nathanesau/twitter-clone:twitter-app
```
