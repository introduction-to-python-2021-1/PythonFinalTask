import json
from abc import ABC, abstractmethod


class ConsoleOutput(ABC):
    """ Abstract console output class. """

    @abstractmethod
    def output(self, data):
        pass


class DefaultOutput(ConsoleOutput):
    """ Default console output class. """

    def __init__(self, limit):
        self.limit = limit

    def output(self, data) -> None:
        if self.limit <= 0 or self.limit >= len(data):
            self.limit = len(data)
        for news in enumerate(data):
            if self.limit == news[0]:
                break
            for key in data[f'{news[1]}'].keys():
                index = f'{key[0].upper()}{key[1:]}'
                if key != 'links':
                    print(f"{index}: {data[f'{news[1]}'][f'{key}']}")
                elif key == 'links':
                    print('Links:')
                    for link in enumerate(data[f'{news[1]}']['links']):
                        print(f"[{link[0] + 1}]: " + f"{data[f'{news[1]}']['links'][f'{link[1]}']['href']} " +
                              f"({data[f'{news[1]}']['links'][f'{link[1]}']['type']})")
            print('\n')


class JSONOutput(ConsoleOutput):
    """ Json console output class. """

    def __init__(self, limit):
        self.limit = limit

    def output(self, data) -> None:
        if self.limit <= 0 or self.limit >= len(data):
            self.limit = len(data)
        keys = [f'new {index}' for index in range(self.limit, len(data))]
        list(map(data.__delitem__, filter(data.__contains__, keys)))
        print(json.dumps(data, ensure_ascii=False, indent=2))
