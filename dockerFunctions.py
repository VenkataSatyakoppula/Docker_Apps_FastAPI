import docker
from database import schemas
import hashlib

client = docker.from_env()

def get_user_hash(email: str):
    return hashlib.sha512(bytes(email, encoding='utf-8')).hexdigest()[:10]


def getallContainers():
    allContainers = client.containers.list()
    container_names = []
    for container in allContainers:
        container_names.append(container.attrs)
    return container_names

def createContainer(app : schemas.AppCreate,user_email: str):
    labels = {
    "traefik.enable": "true",
    f"traefik.http.routers.{app.name}.entrypoints":"web",
    f"traefik.http.routers.{app.name}.rule": f"Host(`{app.name}.{get_user_hash(user_email)}.localhost`)"
    }
    container = client.containers.run(image=app.image,detach=True,network="venkatasatya_default",labels=labels)
    
