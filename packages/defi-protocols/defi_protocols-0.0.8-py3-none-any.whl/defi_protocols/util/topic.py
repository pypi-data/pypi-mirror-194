from dataclasses import dataclass   
from web3 import Web3

@dataclass
class TopicCreator:
    function: str

    def __repr__(self) -> str:
       chunks = self.function.split(' ') 
       types = ['bytes32','uint256','address','uint48']
       type_list = []
       for chunk in chunks:
        if chunk in types:
            type_list.append(chunk)
       return Web3.keccak(text='{}({})'.format(chunks[0],','.join(map(str,type_list)))).hex()

@dataclass
class AddressHexor:
    address: str

    def __repr__(self) -> str:
       return str('{}000000000000000000000000{}'.format(self.address[:2],self.address[2:]))

@dataclass
class DecodeAddressHexor:
    hexor: str

    def __str__(self) -> str:
        return self.hexor.replace('000000000000000000000000','')

    def __repr__(self) -> str:
        return self.__str__()


#wallet = AddressHexor('0x849d52316331967b6ff1198e5e32a0eb168d039d')
#print(wallet)