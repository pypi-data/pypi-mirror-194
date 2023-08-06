import requests
from dataclasses import dataclass,field
from typing import Optional

from defi_protocols.util.explorers import Explorer

#account = '0x849D52316331967b6fF1198e5E32A0eB168D039d'

@dataclass
class RequestFromScan:
    module: str
    action: str
    blockchain: Optional[str] = None
    apikey: Optional[str] = None
    kwargs: field(default_factory=dict) = None

    def __post_init__(self):
        self.apikey = Explorer(self.blockchain).get_private_key()
        self.blockchain = Explorer(self.blockchain).get_explorer()
        [setattr(self, k, v) for k, v in self.kwargs.items()]
    
    def make_request(self):
        params={k: v for k, v in self.__dict__.items() if k != 'kwargs'}
        return params
    
    def request(self):
        request = requests.get(
            'https://api.{}/api?'.format(self.blockchain),
            params={k: v for k, v in self.__dict__.items() if k != 'kwargs'},
        ).json()
        return request

