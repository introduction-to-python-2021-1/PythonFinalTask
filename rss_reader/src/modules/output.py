import json
from abc import ABC, abstractmethod


class ConsoleOutput(ABC):
    """ Abstract console output class. """

    @abstractmethod
    def output(self, data):
        pass


class DefaultOutput(ConsoleOutput):
    """ Default console output class. """

    def output(self, data) -> None:
        for news in data:
            for key in data[f'{news}'].keys():
                index = f'{key[0].upper()}{key[1:]}'
                if key != 'links':
                    print(f"{index}: {data[f'{news}'][f'{key}']}")
                elif key == 'links':
                    print('Links:')
                    for link in enumerate(data[f'{news}']['links']):
                        print(f"[{link[0] + 1}]: " + f"{data[f'{news}']['links'][f'{link[1]}']['href']} " +
                              f"({data[f'{news}']['links'][f'{link[1]}']['type']})")
            print('\n')


class JSONOutput(ConsoleOutput):
    """ Json console output class. """

    def output(self, data) -> None:
        print(json.dumps(data, ensure_ascii=False, indent=2))
