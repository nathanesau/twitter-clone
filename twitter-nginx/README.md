# twitter-nginx

flask app should only be accessible from localhost. nginx should be accessible from anywhere.

```bash
# build the image
docker build -t twitter-nginx .

# run the image
docker run -p 80:80 -p 443:443 --name twitter-nginx -d twitter-nginx

# push to docker hub
docker tag twitter-nginx nathanesau/twitter-clone:twitter-nginx
docker push nathanesau/twitter-clone:twitter-nginx
```
