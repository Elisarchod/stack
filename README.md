# stack

[portainer templates / images for example](https://github.com/xneo1/portainer_templates/blob/master/Template/template.json)

[poratainer compose example](https://github.com/docker/awesome-compose/tree/master/portainer)



```
services:
  portainer:
    image: portainer/portainer-ce:alpine
    container_name: portainer
    command: -H unix:///var/run/docker.sock
    ports:
      - "9000:9000"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "portainer_data:/data"
    restart: always

volumes:
  portainer_data:
```
