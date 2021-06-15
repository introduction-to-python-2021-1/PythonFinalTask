"""json_io module

Classes:
-------
    JsonIO

Attributes:
----------
    _url
    _limit
    _base_directory_path

Methods:
-------
    __init__(self, dirname=".rss_reader")
    get_base_directory_path(self)
    save_raw_rss(self, raw_json_list)
    find_raw_rss(self, date: str, url: str = None, limit: int = None)
    load_raw_rss(self, date: str, url: str)
    (self, raw_json_list: list, url_dir)
"""
import json
import os
import datetime
import logging
import re
import requests


class JsonIO:
    """Class JsonIO provides JSON storage in the files. Downloads and saves to filesystem images spotted in JSON.

    Classes:
    -------
        JsonIO

    Attributes:
    ----------
        _url
        _limit
        _base_directory_path

    Methods:
    -------
        __init__(self, dirname=".rss_reader")
            Constructor of JsonIO class instance.
        get_base_directory_path(self)
            Getter for self._base_directory_path
        save_raw_rss(self, raw_json_list)
            Saves to filesystem list of JSON entries.
        find_raw_rss(self, date: str, url: str = None, limit: int = None)
            Seeking all saved JSON files on given date if url argument not provided.
        load_raw_rss(self, date: str, url: str)
            Loads from filesystem list of JSON entries.
        (self, raw_json_list: list, url_dir)
            Saves images spotted in JSON to filesystem.
    """

    def __init__(self, dirname=".rss_reader"):
        """Constructor of JsonIO class instance.

        Parameters:
        ----------
        arg1: str
            dirname - Directory name for the JSON storage. Default directory created in user's home directory.

        Attributes:
        ----------
            self._base_directory_path - Directory name for the JSON storage.
        """

        #  self._limit = limit
        home_path = os.path.expanduser("~")  # in linux /home/username
        self._base_directory_path = os.path.join(home_path, dirname)  # /home/username/.rss_reader
        logging.info(f"JsonIO:Base directory path:{self._base_directory_path}")

    def get_base_directory_path(self) -> str:
        """get_base_directory_path() - Getter for self._base_directory_path"""
        return self._base_directory_path

    def save_raw_rss(self, raw_json_list) -> None:
        """save_raw_rss() - Saves to filesystem list of JSON entries.

        Parameters:
        ----------
            arg1: list
                raw_json_list - List of JSON entries (dictionaries) to save.

        Returns:
        -------
            None

        Side effects:
            Reads self._base_directory_path
        """
        for entry in raw_json_list:
            # Processing Date
            try:  # When no date provided - not saving this dictionary as JSON
                date = datetime.datetime.fromisoformat(entry["Date"])
            except ValueError:
                logging.info("save_raw_rss: JSON entry has no [Date] attribute - skipping")
                continue

            short_time = date.strftime("%H%M%S")
            short_date = date.strftime("%Y%m%d")

            if len(short_time) != 6 or len(short_date) != 8:
                logging.info(f"save_raw_rss: JSON entry has faulty attribute [Date]={entry['Date']} - skipping")
                continue  # date or time not provided in RSS feed - skipping. Not usable for storage.

            # Processing URL
            try:  # Make URL lower case and remove all non-letter characters
                url_dir = "".join([char for char in entry["URL"].lower() if (97 <= ord(char) <= 122)])
            except AttributeError:
                logging.info("save_raw_rss: JSON entry has no [URL] attribute - skipping")
                continue

            if not url_dir:
                logging.info("save_raw_rss: JSON entry has empty [URL] attribute - skipping")
                continue

            # Collecting the path to save file
            # eg                         /home/username/.rss_reader/httpexcom/20210424
            directory_path = os.path.join(self._base_directory_path, url_dir, short_date)

            file_name = short_time + ".json"
            # eg /home/username/.rss_reader/httpexcom/20210424/  114022.json
            file_path = os.path.join(directory_path, file_name)

            try:
                os.makedirs(directory_path)
                logging.info(f"save_raw_rss: Making directory - {directory_path}")
            except FileExistsError:
                logging.info(f"save_raw_rss: Directory exists - {directory_path} ")

            with open(file_path, "w+") as json_outfile:
                json.dump(entry, json_outfile, indent=2)
                logging.info(f"save_raw_rss:File written: {file_path}")

    def find_raw_rss(self, date: str, url: str = None, limit: int = None):
        """save_raw_rss() - Seeking all saved JSON files on given date if url argument not provided.

        Parameters:
        ----------
        arg1: date
            date - Date in the format YYYYMMDD from which JSON entries to load.
        arg2: str
            url - URL of RSS feed.
        arg3: int
            limit - Number of dictionaries to return.

        Returns:
        -------
            big_raw_json_list: list - List of dictionaries found in JSON storage. Number of entries limited by
            limit parameter

        Side effects:
            Calls self.load_raw_rss()
            Reads self._base_directory_path
        """
        if url:  # Seeking JSON files only in URL directory.
            return self.load_raw_rss(date, url)[:limit]

        # When only date provided, seeking JSON entries for this date in all available directories.
        url_dir = []  # Making list of all available URL directories.
        for d in os.listdir(self._base_directory_path):
            if os.path.isdir(os.path.join(self._base_directory_path, d)):
                url_dir.append(d)

        big_raw_json_list = []
        for U in url_dir:  # Collecting JSON entries from all available URL directories.
            raw_json_list = self.load_raw_rss(date, U)
            big_raw_json_list.extend(raw_json_list)
        return big_raw_json_list[:limit]

    def load_raw_rss(self, date: str, url: str) -> list:
        """load_raw_rss() - Loads from filesystem list of JSON entries.

        Parameters:
        ----------
            arg1: str
                date - Date in the format YYYYMMDD from which JSON entries to load.
            arg2: str
                url - URL of RSS feed.

        Returns:
        -------
            raw_json_list - List of JSON entries.

        Side effects:
            Reads: self._base_directory_path
        """
        #  Converting URL to lower register and removing all non-letter characters
        url_dir = "".join([char for char in url.lower() if (97 <= ord(char) <= 122)])

        raw_json_list = []
        directory_path = os.path.join(self._base_directory_path, url_dir, date)
        files_list = []

        try:  # finding all files in directory
            for filename in os.listdir(directory_path):
                if not os.path.isfile(os.path.join(directory_path, filename)):  # if not file - excluding filename
                    continue

                if not re.match(r"([01]\d|2[0-3])([0-5]\d)([0-5]\d)\.json", filename):  # regexp for 24 hour time hhmmss
                    continue
                files_list.append(filename)
        except FileNotFoundError:
            logging.info(f"load_raw_rss:Directory {directory_path} not exists")
            return raw_json_list

        files_list = sorted(files_list, reverse=True)[:][::-1]  # printing the latest news.
        logging.info(f"Files list {files_list}")

        for filename in files_list:
            with open(os.path.join(directory_path, filename), "r") as json_infile:
                raw_json_list.append(json.load(json_infile))
                pass

        return raw_json_list

    def download_images(self, raw_json_list: list, url_dir) -> None:
        """download_images() - Saves images spotted in JSON to filesystem.

        Parameters:
        ----------
            arg1: list
                raw_json_list - List of JSON entries from which spotted image links are downloaded.
            arg2: str
                url - URL of RSS feed.
        Returns:
        -------
            None

        Side effects:
            Reads self._base_directory_path
        """
        all_links_dict = dict()

        url_dir = "".join([char for char in url_dir.lower() if (97 <= ord(char) <= 122)])

        for entry in raw_json_list:  # for reference in entry["Links"].keys():

            for link in entry["Links"].keys():
                try:
                    url, description = link.split()
                except ValueError as e:
                    logging.info(f"download_images:Error: {e} - Faulty value: {link}")
                    continue

                if description == "(image)" and re.match(r".*\.(gif|jpe?g|bmp|png|apng|avif|svg|webp"
                                                         r"|ico|cur|tif|tiff)", url):

                    short_date = datetime.datetime.fromisoformat(entry["Date"]).strftime("%Y%m%d")
                    if short_date in all_links_dict.keys():
                        all_links_dict[short_date].append(url)
                    else:
                        all_links_dict[short_date] = []
                        all_links_dict[short_date].append(url)

        logging.info(f"download_images:Reference: {all_links_dict}")

        for key in all_links_dict.keys():
            all_links_dict[key] = list(dict.fromkeys(all_links_dict[key]))  # preserve order and remove duplicates
        logging.info(f"download_images:Unique reference: {all_links_dict}")

        for date, url_list in all_links_dict.items():
            for url in url_list:
                file_path = os.path.join(self._base_directory_path, url_dir, date, url.split("/")[-1])
                if os.path.exists(file_path):
                    logging.info(f"File already loaded, skipping:{file_path}")
                    continue
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    logging.info(f"download_images:Downloading file to: {file_path}")
                    with open(file_path, "wb") as graphical_img_file:
                        for chunk in response:
                            graphical_img_file.write(chunk)
