# docker-srb2kart: Sonic Robo Blast 2 Kart server base image

[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/cirvante/srb2kart-server)](https://hub.docker.com/r/cirvante/srb2kart-server)
[![Docker Image Version](https://img.shields.io/docker/v/cirvante/srb2kart-server)](https://hub.docker.com/r/cirvante/srb2kart-server)
[![Docker Image Size](https://img.shields.io/docker/image-size/cirvante/srb2kart-server)](https://hub.docker.com/r/cirvante/srb2kart-server)

Docker image for SRB2Kart, a multiplayer kart racing mod based off the Sonic Robo Blast 2 fangame. This image allows for spinning up multiple containerized instances of an SRB2Kart dedicated server ready to deploy on a user's local machine or cloud hosting platform of their choice with minimal setup.

The docker-srb2kart image is built as a layer on top of the Ubuntu 20.04 base image, and pulls the latest version of the SRB2Kart package from the official KartKrew PPA repository. This base image provides a vanilla SRB2Kart install; no additional WADs or .pk3 files are included. However, users are free to supply their own add-ons by modifying the included docker-compose file to provide a bind mount pointing to the appropriate WADs directory.
