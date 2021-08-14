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
echo "SRB2K default WAD directory is ${SRB2WADDIR}"

# Set configuration directory to scan for blacklist/priority files
CFGDIR=/home/srb2kart/.srb2kart
if [[ -z ${BLACKLIST_FILE} ]]; then
    BLACKLIST_FILE="${CFGDIR}/blacklist.cfg"
fi
echo "Blacklisted WADs file: ${BLACKLIST_FILE}"

if [[ -z ${PRIORITY_FILE} ]]; then
    PRIORITY_FILE="${CFGDIR}/priority.cfg"
fi
echo "Priority WADs file: ${PRIORITY_FILE}"

# Configure the set of WADs to load on server startup
WADS=$(python3 filter_wads.py --wads-dir="${SRB2WADDIR}" --blacklist="${BLACKLIST_FILE}" --load-first="${PRIORITY_FILE}")

# If base port was not set, use the default (5029)
if [[ -z ${SRB2K_PORT} ]]; then
   SRB2K_PORT=5029
fi
echo "Initializing SRB2K server on port ${SRB2K_PORT}"

# Construct the startup command for the server
SRB2K_SERVER_CMD="/usr/games/srb2kart -port ${SRB2K_PORT} -dedicated -file ${WADS}"
echo $SRB2K_SERVER_CMD
$SRB2K_SERVER_CMD
