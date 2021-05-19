import sys
import os
import logging

import pandas as pd

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


class Data:
    def __init__(self):
        """Make empty DataFrame from pandas and check file data.csv
           if he have feed read and connect with empty dataframe and
            clear file"""
        self.df = pd.DataFrame()
        file = open("data.csv", "a")
        if os.path.getsize("data.csv") == 0:
            pass
        else:
            self.data = pd.read_csv("data.csv")
            self.df = pd.concat([self.data])
            f = open("data.csv", "w")
            f.close()

    def make_dataframe(self, item: []):
        """Append feed from reader"""
        dict_ = dict()
        dict_['Title'] = item[0]
        dict_['Date'] = item[1]
        dict_['Link'] = item[2]
        self.df = self.df.append(dict_, ignore_index=True)

    def make_csv(self):
        """Delete duplicate from DataFrame and write to csv"""
        with open("data.csv", "a") as f:
            self.df = self.df.drop_duplicates(subset=["Link"])
            self.df.to_csv(f, index=False)

    def print_data(self, date, limit, verbose):
        """Prints news for the date
        :param date=Date, limit=quantity news, verbose=if need log
        """
        if verbose:
            logger.setLevel(logging.INFO)

        count = 0
        print(f"News for {date}")
        if os.path.getsize("data.csv") == 0:
            print("Empty file")
            sys.exit()
        self.data = pd.read_csv("data.csv")
        all_data = self.data['Date']
        for i in all_data:
            if date == i[:10].replace('-', ''):
                break
        else:
            print(f"doesnt have news on this day ({date})")
        for data, title, link in zip(self.data['Date'], self.data['Title'], self.data['Link']):
            if int(date) == int(data[:10].replace('-', '')):
                logger.info(f"{count + 1}")
                print(f"Title :{title}")
                print(f"Date : {data}")
                print(f"Link : {link}\n")
                count += 1
                if count == limit:
                    break


