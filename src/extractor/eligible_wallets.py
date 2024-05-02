from extractor.abstract import AbtractExtractor
from consumer.models import Wallet

class EligibleWalletsExtractor(AbtractExtractor):
    def extract(self, block, transaction_details, data):
        addresses = set()
        for _, contract in self.erc20_contracts.items():
            matched_trxs = [trx for trx in transaction_details if trx["to"] == contract.address]
            for trx in matched_trxs:
                for event in contract.events.Transfer().process_receipt(trx):
                    dict_event = dict(event)
                    addresses.add(dict_event["args"]["to"])
                    addresses.add(dict_event["args"]["from"])

        eligible_addresses = Wallet.objects.filter(address__in=addresses)
        data["eligible_wallets"] = eligible_addresses
