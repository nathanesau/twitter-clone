# twitter-search

start up elasticsearch server using docker on port 9200 and 9300. [dockerhub link](https://hub.docker.com/repository/docker/nathanesau/twitter-clone)

```bash
# build the image
docker build -t twitter-search .

# run the image
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name twitter-search -d twitter-search

# push to docker hub
docker tag twitter-search nathanesau/twitter-clone:twitter-search
docker push nathanesau/twitter-clone:twitter-search
```