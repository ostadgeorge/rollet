import web3
import random


class EthProvider:
    def __init__(self, endpoints):
        self.endpoints = set(endpoints)
        self.w3s = []
        for endpoint in self.endpoints:
            self.w3s.append(web3.Web3(web3.HTTPProvider(endpoint)))

    @property
    def w3(self):
        return random.choice(self.w3s)

    def get_block(self, identifier):
        return self.w3.eth.get_block(identifier)

    def get_transaction_receipt(self, identifier):
        return self.w3.eth.get_transaction_receipt(identifier)
    
    def get_block_number(self):
        return self.w3.eth.block_number
    
    def get_contract(self, address, abi):
        if not web3.Web3.is_checksum_address(address):
            address = web3.Web3.to_checksum_address(address)
        return self.w3.eth.contract(address=address, abi=abi)