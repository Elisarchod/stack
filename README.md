# stack

[portainer templates / images for example](https://github.com/xneo1/portainer_templates/blob/master/Template/template.json)

[poratainer compose example](https://github.com/docker/awesome-compose/tree/master/portainer)

# jelly fin reset
https://community.synology.com/enu/forum/1/post/187787

```
services:
  portainer:
    image: portainer/portainer-ce:alpine
    container_name: portainer
    command: -H unix:///var/run/docker.sock
    ports:
      - "9000:9000"
      - "8000:8000" # Add this line to expose Chisel server port
      - "9443:9443" # Add this line to expose HTTPS port
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "portainer_data:/data"
    restart: always

volumes:
  portainer_data:
```


#### Stop all images
``` docker stop $(docker ps -q) ```
