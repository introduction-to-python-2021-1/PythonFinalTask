class ConsoleOutput:

    def __init__(self, logger):
        self.__logger = logger

    def __enter__(self):
        self.__logger.debug('News printing has started.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__logger.debug('News printing has finished.')

    @staticmethod
    def output(news):
        """
        Output of news to the console
        :param news: list of news
        """
        for onews in news:
            print('\nFeed: {}'.format(onews['feed']))
            print('\nTitle: {}'.format(onews['title']))
            print('Date: {}'.format(onews['date']))
            print('Link: {}\n'.format(onews['link']))

            if onews.get('description') is not None:
                print(onews['description'])
                print()

            if onews.get('links') is not None:
                links = onews.get('links')
                print('Links:')
                for i in range(len(links)):
                    print('[{}] {} ({})'.format(i + 1, links[i].get('link'), links[i].get('type')))
