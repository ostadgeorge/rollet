import web3

class AbtractExtractor:
    def __init__(self, provider, erc20_contracts):
        self.provider = provider
        self.erc20_contracts = erc20_contracts

    def extract(self, block: web3.datastructures.AttributeDict, data: dict):
        raise NotImplementedError("extract method is not implemented")