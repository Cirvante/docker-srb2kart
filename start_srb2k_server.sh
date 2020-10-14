#!/bin/bash

#####################################################################
#
# FILE: start_srb2k_server.sh
#
# DESCRIPTION: Shell script which serves as the entrypoint for launching
#              the SRB2Kart server within the container.
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

# Set base WAD directory to scan for additional wad/pk3/kart files
SRB2WADDIR=/srb2k-server/wads
WADS=$(find ${SRB2WADDIR} -type f | egrep "*.(pk3|wad|kart)$" | tr '\n' ' ')

echo "SRB2K default WAD directory is ${SRB2WADDIR}"
echo "Initializing SRB2K server on port ${SRB2K_PORT}"

# Construct the startup command for the server
SRB2K_SERVER_CMD="/usr/games/srb2kart -port ${SRB2K_PORT} -dedicated -file ${WADS}"
echo $SRB2K_SERVER_CMD
$SRB2K_SERVER_CMD
