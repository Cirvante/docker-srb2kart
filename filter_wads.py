#!/usr/bin/python3

"""

 FILE: filter_wads.py

 DESCRIPTION: Scans for available WADs and returns a filtered list of
              which ones to load depending on certain criteria.

 AUTHOR: Cirvante
 
 LICENSE: GPL 2.0

 This program is free software: you can redistribute it and/or modify  
 it under the terms of the GNU General Public License as published by  
 the Free Software Foundation, version 2.

 This program is distributed in the hope that it will be useful, but 
 WITHOUT ANY WARRANTY; without even the implied warranty of 
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 General Public License for more details.

 You should have received a copy of the GNU General Public License 
 along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os, argparse, re

SRB2K_WAD_FILTER = '^.*[.](pk3|wad|kart)'

class SRB2KWADFilter(object):
    """
    Scans for available WADs and filters them according to specified criteria.

    Attributes
    ----------
    scanned_paths: list
        List of previously scanned paths when discovering WADs.
    available_wads: dict
        Contains entries for all currently available WADs based on filtering rules applied.
    blacklisted_wads
        Contains entries for all blacklisted WADs. These WADs are removed from the available WADs pool.
    prioritized_wads:
        Contains entries for all prioritized WADs. These WADs are loaded first.
    """
    
    # BEGIN SECTION Constructors

    def __init__(self, wads_path: str=None, blacklist_file: str=None, priority_file: str=None):
        """
        Constructor.

        Parameters
        ----------
        wads_path: str
            Path to the directory to scan for SRB2K-compatible WADs.
        blacklist_file: str
            Path to a blacklist file.
        priority_file: str
            Path to a file containing a list of which WADs to move to the front of the list.
        """

        self.scanned_paths = []
        self.blacklist_file = blacklist_file
        self.priority_file = priority_file

        self.available_wads = self.__scan_available_wads(wads_path)
        self.blacklisted_wads = dict()
        self.prioritized_wads = dict()

    @staticmethod
    def from_cmdline_args():
        """
        Constructs an SRB2KWADFilter from the command-line arguments in sys.argv.

        Returns
        -------
        SRB2KWADFilter
            An instance of this class.
        """
        parser = argparse.ArgumentParser(description='Filter WADs based on input criteria')
        parser.add_argument('--wads-dir', dest='wads', type=str, required=True,
                        help='Path to the directory to scan for WADs.')
        parser.add_argument('--blacklist', dest='blacklist', type=str, required=False,
                        help='A file containing a list of WADs that should not be loaded.')
        parser.add_argument('--load-first', dest='load_first', type=str, required=False,
                        help='A file containing a list of WADs to load before all others.')

        args = parser.parse_args()

        return SRB2KWADFilter(args.wads, args.blacklist, args.load_first)

    # END SECTION Constructors

    # BEGIN SECTION Public Methods

    def add_wads(self, wads_path: str):
        """
        Adds any WADs found in the specified path to the dictionary of available WADs.

        Parameters
        ----------
        wads_path: str
            Path to a directory containing one or more WADs.

        Returns
        -------
        result: dict
            A dictionary containing entries for all WADs added from that directory.
        """

        result = self.__scan_available_wads(wads_path)

        if len(result) > 0:
            self.available_wads.update(result)

        return result

    def blacklist_wads(self, blacklist_path: str):
        """
        Given a path to a blacklist file, removes these WADs from the available entries.

        Blacklisted names found in the WAD entries dictionary have their entries removed in-place. 
        Names mentioned in the blacklist but not present in the WAD entries are ignored.

        Parameters
        ----------
        blacklist_path: str
            A string representing the path to a blacklist file.

        Returns
        -------
        result: dict
            A dictionary containing entries for all WADs blacklisted.
        """

        result = {name: self.available_wads.pop(name, None) for name in self.__filter_wad_list(blacklist_path)}

        self.blacklisted_wads.update(result)

        return result

    def prioritize_wads(self, priority_path: str):
        """
        Given a path to a priority file, recreates the available WAD entries with the 
        WADs listed in the priority file as the first elements. 
        Names in the priority file not present in the available entries are ignored.

        Parameters
        ----------
        priority_path: str
            The path to the priority file.

        Returns
        -------
        result: dict
            A dictionary containing all the WAD entries re-ordered appropriately.
        """

        result = {name: self.available_wads.pop(name, None) for name in self.__filter_wad_list(priority_path)}

        self.prioritized_wads.update(result)
        result.update(self.available_wads)
        self.available_wads = result

        return result

    def print_filtered_wads(self):
        """
        Returns a string containing the filtered set of WADs as a space-separated list of paths, ready
        for consumption by `srb2kart -file`. 

        Returns
        -------
        str:
            A space-separated list of paths
        """
        self.blacklist_wads(self.blacklist_file)
        self.prioritize_wads(self.priority_file)

        return ' '.join(self.available_wads.values())
    
    # END SECTION Public Methods

    # BEGIN SECTION Private Methods

    def __filter_wad_list(self, wad_list_path: str):
        """
        Reads a list of WAD filenames (basenames, not full paths) from the specified text file.
        The file must contain one filename per line. This method produces a generator which yields
        only the WAD names that match entries currently in self.available_wads.

        Parameters
        ---------- 
        wad_list_path: str
            Path to a text file containing WAD names

        Returns
        -------
        result: genexpr
            Generator containing only the names of WADs currently availabe
        """

        result = ()

        valid_path = wad_list_path is not None and os.path.isfile(wad_list_path)

        if valid_path:
            with open(wad_list_path) as wad_list:
                name_list = wad_list.read().split()
                result = (name for name in name_list if name in self.available_wads)

        return result

    def __scan_available_wads(self, wads_path: str):
        """
        Collects WADs from the specified directory in the form of a dictionary containing {filename: realpath} 
        key-value pairs. Does not travel directories recursively. 

        Parameters
        ----------
        wads_path: str
            Path to a directory containing one or more WADs.

        Returns
        -------
        result: dict
            The dictionary of available WADs in the directory.
        """

        result = dict()

        if wads_path not in self.scanned_paths and os.path.isdir(wads_path):
            dir_elems = os.scandir(wads_path)
            result = {entry.name: entry.path for entry in dir_elems if re.match(SRB2K_WAD_FILTER, entry.name)}
            self.scanned_paths.append(wads_path)

        return result

    # END SECTION Private Methods

# END class SRB2KWADFilter

if __name__ == '__main__':

    wad_filter = SRB2KWADFilter.from_cmdline_args()
    print(wad_filter.print_filtered_wads())

