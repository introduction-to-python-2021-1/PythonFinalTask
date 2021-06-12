import sys
import os
import logging
import datetime

import dateparser
import pandas as pd

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def file_open():
    """Open file for caching"""
    return open("data.csv", "a")


class Data:
    def __init__(self):
        """
        Make empty DataFrame from pandas and check file data.csv
        if he have feed read and connect with empty dataframe and
        clear file
        """
        self.df = pd.DataFrame()
        file_open()
        if os.path.getsize("data.csv") == 0:
            pass
        else:
            self.data = pd.read_csv("data.csv")
            self.df = pd.concat([self.data])
            os.remove("data.csv")

    def append_dataframe(self, item: {}):
        """
        Append feed from reader.

        Parameter:
                item = dictionary of feed news
        """
        self.df = self.df.append(item, ignore_index=True)

    def update_cache(self):
        """Update cache and drop duplicate"""
        file_open()
        self.df = self.df.drop_duplicates(subset=["Link"])
        self.df.to_csv("data.csv", index=False)
        if os.path.getsize("data.csv") == 0:
            os.remove("data.csv")
            logger.error("Empty file")
            sys.exit()

    def sort_data(self, date, limit, verbose):
        """
        Prints news for the date.

        Parameters:
             date=Date, limit=quantity news, verbose=if need log, argjson=format json in stdout
        """
        if verbose:
            logger.setLevel(logging.INFO)
        count = 0
        if os.path.getsize("data.csv") == 1:
            logger.error("Empty file")
            os.remove("data.csv")
            sys.exit()
        self.data = pd.read_csv("data.csv")
        all_data = self.data['Date']
        date = datetime.datetime.strptime(date, "%Y%m%d")
        for days in all_data:
            if date.date() == dateparser.parse(days).date():
                break
        else:
            print(f"doesnt have news on this day ({date})")
            sys.exit()
        print(f"News for {date}")
        news_df = pd.DataFrame()
        for data, title, link, img in zip(self.data['Date'], self.data['Title'], self.data['Link'], self.data["img"]):
            if date.date() == dateparser.parse(data).date():
                count += 1
                logger.info(f"{count}")
                patch_data = dict()
                patch_data["Title"] = title
                patch_data["Date"] = data
                patch_data["Link"] = link
                patch_data["img"] = img
                news_df = news_df.append(patch_data, ignore_index=True)

        return dict(news_df[:limit])
