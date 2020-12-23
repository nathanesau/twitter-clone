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

for digitalocean, the docker-compose configuration doesn't work well. instead, use:

```bash
# install elasticsearch
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt update
sudo apt install elasticsearch

# elasticsearch config
sudo nano /etc/elasticsearch/elasticsearch.yml # change network.host to localhost
sudo nano /etc/elasticsearch/jvm.options # change jvm mem limits

# start elasticsearch
sudo systemctl enable elasticsearch

# check service
systemctl status elasticsearch.service

# enable service on restart
sudo systemctl enable elasticsearch

# make sure it is running
curl -X GET "localhost:9200"
```

a quick python test to make sure es is working:

```python
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200/'])
print(es.ping())
```