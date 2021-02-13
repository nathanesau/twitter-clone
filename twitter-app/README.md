# twitter-app

start up flask app using port 5000 [dockerhub link](https://hub.docker.com/repository/docker/nathanesau/twitter-clone)

```bash
# build the image
docker build -t twitter-app .

# run the image
docker run -p 5000:5000 --name twitter-app -d twitter-app

# first generate a personal access token using "Settings / Developer Settings"
# save the token to ~/.tokens/GH_TOKEN
# then  login to github container registry
# run using git bash
cat ~/.tokens/GH_TOKEN | docker login https://docker.pkg.github.com --username nathanesau --password-stdin

# push to github container registry
# run using git bash
docker tag twitter-app docker.pkg.github.com/nathanesau/twitter-clone/twitter-app:1.0
docker push docker.pkg.github.com/nathanesau/twitter-clone/twitter-app:1.0
```
