import sys
import os
import logging

import pandas as pd

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


class Data:
    def __init__(self):
        """
        Make empty DataFrame from pandas and check file data.csv
        if he have feed read and connect with empty dataframe and
        clear file
        """
        self.df = pd.DataFrame()
        file = open("data.csv", "a")
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

    def append_cache(self):
        """Delete duplicate from DataFrame and write to csv"""
        with open("data.csv", "a") as f:
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
        for days in all_data:
            if date == days[:10].replace('-', ''):
                break
        else:
            print(f"doesnt have news on this day ({date})")
            sys.exit()
        if not limit:
            limit = len(all_data)
        elif limit < 0:
            logger.error("Negative limit")
            sys.exit()
        print(f"News for {date}")
        news_df = pd.DataFrame()
        for data, title, link in zip(self.data['Date'], self.data['Title'], self.data['Link']):
            if int(date) == int(data[:10].replace('-', '')):
                logger.info(f"{count + 1}")
                count += 1
                patch_data = dict()
                patch_data["Title"] = title
                patch_data["Date"] = data
                patch_data["Link"] = link
                news_df = news_df.append(patch_data, ignore_index=True)

        return news_df[:limit]
