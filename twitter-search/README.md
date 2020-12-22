# twitter-app

start up elasticsearch using port 9200 [dockerhub link](https://hub.docker.com/repository/docker/nathanesau/twitter-clone)

```bash
# build the image
docker build -t twitter-search .

# run the image
docker run -p 9200:9200 --name twitter-search -d twitter-search

# push to docker hub
docker tag twitter-search nathanesau/twitter-clone:twitter-search
docker push nathanesau/twitter-clone:twitter-search
```
