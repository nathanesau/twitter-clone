FROM nginx:latest

# copy configuration files to the container
COPY twitter-app /etc/nginx/conf.d/default.conf

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]