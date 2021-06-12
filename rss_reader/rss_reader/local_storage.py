# Author: Julia Los <los.julia.v@gmail.com>.

"""Python command-line RSS reader

This module contains functions for work with local storage of loaded news.
"""

import json
import os

from contextlib import suppress
from time import strftime, strptime

_date_channel_format = '%Y%m%d'
_date_news_format = '%a, %d %b, %Y %I:%M %p'


def convert_date_format(date, from_format, to_format):
    """Convert date format (for example: from Sun, 23 May, 2021 05:30 PM to 20210523)."""
    format_date = ''
    try:
        format_date = strftime(to_format, strptime(date, from_format))
    except (TypeError, ValueError):
        pass
    return format_date


def load_from_storage(filename, load_date, load_source='', limit=None, logger=None):
    """Load data from local storage."""
    if logger:
        logger.info("Load data from local storage...")

    if load_date is None:
        if logger:
            logger.warning("Argument 'date' is empty.")
        return

    if not os.path.isfile(filename):
        if logger:
            logger.warning("Local storage does not exist.")
        return

    with suppress(OSError):
        with open(filename, 'r') as f:
            try:
                storage_data = json.load(f)
            except (TypeError, ValueError):
                if logger:
                    logger.error("Failed to load data from local storage.")
                return

            if len(storage_data) == 0:
                if logger:
                    logger.info("No data in local storage.")
                return

            load_news = 0
            data = []

            for channel in storage_data:
                if load_source != '':
                    if channel.get('channel_id', '') != load_source:
                        continue

                if channel.get('news') is None:
                    continue

                load_channel = {'channel_id': channel.get('channel_id', ''),
                                'channel_title': channel.get('channel_title', ''),
                                'news': [],
                                }

                for news in channel['news']:
                    news_date = convert_date_format(news.get('date'), _date_news_format, _date_channel_format)

                    if news_date != load_date:
                        continue

                    if limit:
                        if load_news >= limit:
                            break

                    load_news += 1
                    news_copy = news.copy()
                    news_copy['number'] = len(load_channel['news']) + 1
                    load_channel['news'].append(news_copy)

                if len(load_channel['news']) > 0:
                    data.append(load_channel)

            if len(data) == 0:
                if logger:
                    logger.info("No find data in local storage.")
                return

            return data


def save_to_storage(filename, data, logger=None):
    """Save data to local storage."""
    if logger:
        logger.info("Save data to local storage...")

    if data is None:
        if logger:
            logger.warning("Data is None.")
        return

    if len(data) == 0:
        if logger:
            logger.warning("Data is empty.")
        return

    storage_data = []

    with suppress(OSError):
        with open(filename, 'w') as f:
            try:
                storage_data = json.load(f)
            except (TypeError, ValueError):
                if logger:
                    logger.error("Failed to load data from local storage.")

            storage_channel = {'channel_id': data[0]['channel_id'],
                               'channel_title': data[0]['channel_title'],
                               'news': [news.copy() for news in data[0]['news']]
                               }

            if len(storage_data) == 0:
                storage_data.append(storage_channel)
            else:
                for index, channel in enumerate(storage_data, start=0):
                    if channel.get('channel_id') == storage_channel.get('channel_id'):
                        storage_data[index] = storage_channel
                        break

            try:
                json.dump(storage_data, f)
            except (TypeError, ValueError):
                if logger:
                    logger.error("Failed to save data to local storage.")
