import json


class ConsoleOutput:
    """ Class for printing news to console in human readable format """

    def __init__(self, logger):
        self.__logger = logger

    def __enter__(self):
        self.__logger.debug('News printing has started.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__logger.debug('News printing has finished.')

    def __validate_limit(self, news, limit):
        """
        Validation a given limit
        :param limit: given limit
        :return: validated limit
        """
        if limit <= 0 or limit > len(news):
            return len(news)
        else:
            self.__logger.debug('Limit on the number of news: {}.'.format(limit))
            return limit

    def output(self, data, limit):
        """
        Output of news to the console
        :param data: list of news
        """
        limit = self.__validate_limit(data, limit)
        news = data[:limit]

        for onews in news:
            print('\nFeed: {}'.format(onews['feed']))
            print('\nTitle: {}'.format(onews['title']))
            print('Date: {}'.format(onews['date']))
            print('Link: {}\n'.format(onews['link']))

            if onews.get('description'):
                print(onews['description'])
                print()

            if onews.get('links'):
                links = onews.get('links')
                print('Links:')
                for i in range(len(links)):
                    print('[{}] {} ({})'.format(i + 1, links[i].get('link'), links[i].get('type')))

    def output_json(self, data, limit):

        limit = self.__validate_limit(data, limit)
        news = data[:limit]
        print(json.dumps(news, ensure_ascii=False, indent=3))
