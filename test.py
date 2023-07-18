import docker
from dockerFunctions import get_user_hash
client = docker.from_env()

## for listing
# allContainers = client.containers.list()
# print(allContainers)

# ## for creating a container
labels = {
    "traefik.enable": "true",
    "traefik.http.routers.nginx.entrypoints":"web",
    "traefik.http.routers.nginx.rule": "Host(`nginx.localhost`)"
}

nginx_container = client.containers.run(image="nginx",detach=True,network="venkatasatya_default",labels=labels)
print(nginx_container.logs())

### for testing hash
# hash = get_user_hash("satya5202@gmail.com")

# print(hash)