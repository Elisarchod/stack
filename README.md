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


#### stop all images
``` docker stop $(docker ps -q) ```

#### remove all images
```docker rmi -f $(docker images -q)```

#### init stack
``` docker compose -f llm-compose.yml --stack-name llm-stack up -d  ```

#### restart stack
```find . -name "*.yml" -exec docker-compose -f {} up -d --force-recreate --build \;```

#### full restart stack with volumes and network
```find . -name "*.yml" -exec docker-compose -f {} down \; -exec docker-compose -f {} up -d --build \;```
better than above code - currrent dir files only
```find . -maxdepth 1 -name "*.yml" -exec sh -c 'docker-compose -f "$1" down && docker-compose -f "$1" up -d --build' _ {} \;```

### mount drive
https://www.perplexity.ai/search/premenet-mount-drive-on-linux-BtU2U5YISPqy0lSfiuntJw

lsblk
sudu mkdir /mnt/elements_main
sudo nano /etc/fstab
UUID=<your-drive-uuid> /mnt/mydrive ext4 defaults,uid=1000,gid=1000,rw 0 2



