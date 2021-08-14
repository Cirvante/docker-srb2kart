# syntax = docker/dockerfile:experimental

#####################################################################
#
# FILE: Dockerfile
#
# DESCRIPTION: Dockerfile for building the SRB2Kart Dedicated Server 
#              base image.
#
# AUTHOR: Cirvante
# 
# LICENSE: GPL 2.0
#
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#####################################################################

# Depends on the Ubuntu 20.04 base image
FROM ubuntu:20.04

# Set working directory
WORKDIR /srb2k-server

# Copy the entrypoint shell script into the container
COPY start_srb2k_server.sh .
COPY filter_wads.py .

# Install the add-apt-repository command, since it does not ship with 
# the Ubuntu base image
RUN --mount=target=/var/lib/apt/lists,type=cache \
    --mount=target=/var/cache/apt,type=cache \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common

# Install the srb2k PPA from the Kart Krew repository
RUN add-apt-repository ppa:kartkrew/srb2kart && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y srb2kart

# Make an empty directory for WADs
# We will bind mount these from the docker-compose file later
RUN mkdir wads

# Make sure startup script is executable
RUN groupadd -r srb2kart && \
    useradd -r -g srb2kart srb2kart && \
    chmod +x start_srb2k_server.sh

# Switch to the application user
USER srb2kart

# Entrypoint for the application
ENTRYPOINT ["/bin/bash", "-i", "/srb2k-server/start_srb2k_server.sh"]
