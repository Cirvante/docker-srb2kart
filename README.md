# docker-srb2kart: Sonic Robo Blast 2 Kart server base image

[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/cirvante/srb2kart-server)](https://hub.docker.com/r/cirvante/srb2kart-server)
[![Docker Image Version](https://img.shields.io/docker/v/cirvante/srb2kart-server)](https://hub.docker.com/r/cirvante/srb2kart-server)
[![Docker Image Size](https://img.shields.io/docker/image-size/cirvante/srb2kart-server)](https://hub.docker.com/r/cirvante/srb2kart-server)

## Description
Docker image for [SRB2Kart](https://mb.srb2.org/showthread.php?t=43708), a multiplayer kart racing mod based off the [Sonic Robo Blast 2](https://www.srb2.org/) fangame. This image allows for spinning up multiple containerized instances of an SRB2Kart dedicated server ready to deploy on a user's local machine or cloud hosting platform of their choice with minimal setup.

## Requirements
* Docker Engine 18.09+ (BuildKit support)

## Overview
The ``docker-srb2kart`` image is built as a layer on top of the Ubuntu 20.04 base image, and pulls the latest version of the SRB2Kart package from the [official KartKrew PPA repository](https://launchpad.net/~wolfy852/+archive/ubuntu/kart-public). This base image provides a vanilla SRB2Kart install; no additional WADs or .pk3 files are included. However, users are free to supply their own add-ons by modifying the included docker-compose file to provide a bind mount pointing to the appropriate WADs directory.

## Usage
### Basic deployment
The simplest way to spin up the SRB2K container is via [Docker Compose](https://docs.docker.com/compose/). Download the [Compose file](https://github.com/Cirvante/docker-srb2kart/blob/main/docker-compose.yml) from the repository, then open a terminal and run the following command:
```
$ docker-compose -f path/to/docker-compose.yml up -d
```
This will pull the ``cirvante/srb2kart-server:latest``  image from the Docker Hub registry and spin up a single server container running as a daemon. If successful, you should see output similar to the following:
```
Pulling srb2k-server (cirvante/srb2kart-server:latest)...
latest: Pulling from cirvante/srb2kart-server
d72e567cc804: Already exists
0f3630e5ff08: Already exists
b6a83d81d1f4: Already exists
cefd81749968: Pull complete
3e8b3cab29aa: Pull complete
6aab2a80210f: Pull complete
873a14aa3f7d: Pull complete
00f066f3e928: Pull complete
4384f21247da: Pull complete
Digest: sha256:d803f635ee44b6179907c244e23406ed2a3d830897c4c4ac8f81242d99934804
Status: Downloaded newer image for cirvante/srb2kart-server:latest
Creating srb2k-server ... done
```
You may verify that the container is up and running via the following:
```
$ docker ps
```
```
CONTAINER ID        IMAGE                             COMMAND                  CREATED              STATUS              PORTS               NAMES
0add84a3383f        cirvante/srb2kart-server:latest   "/bin/sh -c /srb2k-s…"   About a minute ago   Up About a minute                       srb2k-server
```
Note that since the container is running in the background, there is no interactive console. You can still perform server management in-game as normal by configuring a password in the ``kartserv.cfg`` and logging in. You can also inspect the server logs via the ``docker logs`` command:
```
$ docker logs srb2k-server -f
```
```
(...output omitted...)
M_Init(): Init miscellaneous info.
R_Init(): Init SRB2 refresh daemon.
R_LoadTextures()...
P_InitPicAnims()...
R_InitSprites()...
srb2.srb added 2975 frames in 232 sprites
gfx.kart added 1030 frames in 148 sprites
chars.kart added 87 frames in 1 sprites
patch.kart added 5 frames in 2 sprites
Added skin 'tails'
Added skin 'knuckles'
Added skin 'eggman'
Added skin 'metalsonic'
R_InitColormaps()...
ST_Init(): Init status bar.
D_CheckNetGame(): Checking network game status.
Starting Server....
Binding to 0.0.0.0
Network system buffer: 208Kb
couldn't execute file /home/srb2kart/.srb2kart/kartserv.cfg
Entering main game loop...
===========================================================================
                   We hope you enjoy this game as
                     much as we did making it!
===========================================================================
SRB2Kart v1.3 (Oct  4 2020 20:06:24 illegal)
SDL Linux 64-bit
Speeding off to level...
Map is now "MAP01: Green Hills Zone"
```
The above command works identical to ``tail -f`` on any Linux distro; to exit out of the log, press ``Ctrl-C``.

### Pulling specific versions
Users may specify which version of the ``srb2kart-server`` image to pull when running ``docker-compose`` by passing in the appropriate tag via the ``SRB2K_VERSION`` environment variable:
```
$ SRB2K_VERSION="1.3" docker-compose -f path/to/docker-compose.yml up -d
```

### Port configuration
SRB2K servers use UDP port 5029 by default. Users are free to change this by setting the container's ``SRB2K_PORT`` environment variable to any valid port. To set this environment variable, open the ``docker-compose.yml`` file in a text editor, replace the ``ports`` section with the new value, and insert an ``environment`` section in the service declaration:
```
    ports:
        - "5030"
    environment:
        - SRB2K_PORT=5030
```
This will set the container's ``SRB2K_PORT`` to 5030 on the next launch. Restart the container with ``docker-compose restart`` and inspect the logs to verify the server is binding on the new port:
```
$ docker logs srb2k-server -f
```
```
(...output omitted...)
R_InitColormaps()...
ST_Init(): Init status bar.
D_CheckNetGame(): Checking network game status.
Starting Server....
Binding to 0.0.0.0:5030
(...rest of output omitted...)
```
Users are encouraged to verify that their firewall is properly configured to allow incoming connections to the desired port.

### Customizing the server
Users may provide their own ``kartserv.cfg`` configuration files by bind-mounting a host folder containing said file to ``/home/srb2kart/.srb2kart/``.  Similarly, custom tracks, characters and add-ons may be loaded by bind-mounting a host folder containing the desired WADs to ``/srb2k-server/wads``.

First, make sure the container is stopped:
```
$ docker-compose down
```
```
Stopping srb2k-server ... done
Removing srb2k-server ... done
```
Next, open the ``docker-compose.yml`` file in a text editor, and add the following lines after the ``image`` and ``ports`` section of your service declaratios:
```
    volumes:
        - ./cfg:/home/srb2kart/.srb2kart:ro
        - ./wads:/srb2k-server/wads:ro
```
This tells Docker Compose to mount the host folders ``./cfg`` and ``./wads`` (note the relative path!) to ``/home/srb2kart/.srb2kart`` and ``/srb2k-server/wads`` respectively the next time we create the server container. The ``:ro`` at the end of the container path tells Docker to mount that folder as read-only, for security purposes. 

### Multiple server instances
To spawn multiple SRB2K server containers, simply edit the ``docker-compose.yml`` and add a new service declaration under ``services`` for each desired instance. Users should make sure each server instance is configured for different ports to avoid network conflicts. In general, users can spawn as many containers as their system resources permit. A single instance of the SRB2K server with no custom addons uses approximately 145MB of physical memory, as shown by the example ``top`` output below:
```
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 850312 999       20   0  353492 144484   5308 S   2.0   0.5   0:02.35 srb2kart
```
Users may provide different configuration files and add-ons for different server instances launched from the same Compose file. The repository includes an example [``multiple-servers.yml`` ](https://github.com/Cirvante/docker-srb2kart/blob/main/examples/multiple-servers.yml) which launches two server instances, one of which is configured to always start in Encore Mode. Both servers also have their own MOTD banner. Note that this example assumes the user provides a copy of ``KL_HOSTMOD_V13`` , which can be found [here](https://mb.srb2.org/attachment.php?attachmentid=38765&d=1600065005).

### Swarm deployment
Deploying multiple server containers as a [Docker Swarm](https://docs.docker.com/compose/swarm/overview.md) *should* be possible, but is not tested in the current release and no examples are provided. In theory, this would allow enforcing CPU and memory quotas via additional configuration in the Compose file, which would be useful when deploying to a CSP.

## Build
For those who wish to experiment manually building the ``srb2kart-server`` image, whether they wish to bundle their WADs into the image itself or use this as a base image for more elaborate modding, they may do so by cloning the repository and using the following build command:
```
$ git clone https://github.com/cirvante/srb2kart-server
$ DOCKER_BUILDKIT=1 docker build --tag srb2kart-server:my_custom_tag .
```
The ``DOCKER_BUILDKIT`` is necessary; this tells Docker to use its new BuildKit build system for improved caching and better performance when adding layers in future rebuilds.

## Contact
Bug reports and suggestions for improvements are always welcome. Feel free to [open an issue](https://github.com/Cirvante/docker-srb2kart/issues) on the GitHub repository.

