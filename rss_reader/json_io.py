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
    __init__(self, url, limit=None, dirname=".rss_parser")
    get_base_directory_path(self)
    save_raw_rss(self, raw_json_list)
    load_raw_rss(self, date=None, limit=None)
    download_images(self, raw_json_list)
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
        __init__(self, url, limit=None, dirname=".rss_parser")
            Constructor of JsonIO class instance.
        get_base_directory_path(self)
            Getter for self._base_directory_path
        save_raw_rss(self, raw_json_list)
            Saves to filesystem list of JSON entries.
        load_raw_rss(self, date=None, limit=None)
            Loads from filesystem list of JSON entries.
        download_images(self, raw_json_list)
            Saves images spotted in JSON to filesystem.
    """
    def __init__(self, url, limit=None, dirname=".rss_parser"):
        """Constructor of JsonIO class instance.

        Parameters:
        ----------
        arg1: str
            url - URL of RSS feed to save or load.
        arg2: int
            limit - Number of RSS feed entries to process.
        arg3: str
            dirname - Directory name for the JSON storage. Default directory created in user's home directory.

        Attributes:
        ----------
            self._url - URL of RSS feed to save or load.
            self._limit - Number of RSS feed entries to process.
            self._base_directory_path - Directory name for the JSON storage.
        """
        self._url = "".join([char for char in url.lower() if (97 <= ord(char) <= 122)])
        #  self.date = date  # move date to load_raw_rss ???
        self._limit = limit
        home_path = os.path.expanduser("~")  # in linux /home/username
        self._base_directory_path = os.path.join(home_path, dirname, self._url)  # /home/username/.rss_parser
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
        """
        for entry in raw_json_list:
            date = datetime.datetime.fromisoformat(entry["Date"])
            short_time = date.strftime("%H%M%S")
            short_date = date.strftime("%Y%m%d")

            if len(short_time) != 6 or len(short_date) != 8:
                continue  # date or time not provided in RSS feed - skipping. Not usable for storage.

            date_directory = short_date
            # eg              /home/username/.rss_parser/httpexcom/   20210424
            directory_path = os.path.join(self._base_directory_path, date_directory)

            file_name = short_time + ".json"
            # eg /home/username/.rss_parser/httpexcom/20210424/  114022.json
            file_path = os.path.join(directory_path, file_name)

            try:
                os.makedirs(directory_path)
            except FileExistsError:
                logging.info(f"Directory {directory_path} exists")

            with open(file_path, "w+") as json_outfile:
                json.dump(entry, json_outfile, indent=2)
                logging.info(f"save_raw_rss:File written: {file_path}")

    def load_raw_rss(self, date=None, limit=None) -> list:
        """load_raw_rss() - Loads from filesystem list of JSON entries.

        Parameters:
        ----------
            arg1: str
                date - Date in the format YYYYMMDD from which JSON entries to load.
            arg2: int
                limit - Number of JSON entries to read.

        Returns:
        -------
            raw_json_list - List of JSON entries.
        """

        raw_json_list = []
        directory_path = os.path.join(self._base_directory_path, date)
        files_list = []

        try:
            for filename in os.listdir(directory_path):
                if not os.path.isfile(os.path.join(directory_path, filename)):  # if not file - excluding filename
                    continue

                if not re.match(r"([01]\d|2[0-3])([0-5]\d)([0-5]\d)\.json", filename):  # regexp for 24 hour time hhmmss
                    continue
                files_list.append(filename)
        except FileNotFoundError:
            logging.info(f"load_raw_rss:Directory {directory_path} not exists")
            return raw_json_list

        files_list = sorted(files_list, reverse=True)[:self._limit][::-1]  # printing the latest news.
        logging.info(f"Files list {files_list}")

        for filename in files_list:
            with open(os.path.join(directory_path, filename), "r") as json_infile:
                raw_json_list.append(json.load(json_infile))
                pass

        return raw_json_list

    def download_images(self, raw_json_list) -> None:
        """download_images() - Saves images spotted in JSON to filesystem.

        Parameters:
        ----------
            arg1: list
                raw_json_list - List of JSON entries from which spotted image links are downloaded.

        Returns:
        -------
            None
        """
        all_links_dict = dict()

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
                file_path = os.path.join(self._base_directory_path, date, url.split("/")[-1])
                if os.path.exists(file_path):
                    logging.info(f"File already loaded, skipping:{file_path}")
                    continue
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    logging.info(f"download_images:Downloading file to: {file_path}")
                    with open(file_path, "wb") as graphical_img_file:
                        for chunk in response:
                            graphical_img_file.write(chunk)
