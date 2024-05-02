from extractor.abstract import AbtractExtractor
from consumer.models import Wallet
import web3

class ERC20BalanceExtractor(AbtractExtractor):
    def extract(self, block, transaction_details, data: dict):
        eligible_addresses = data.get("eligible_wallets", [])
        addresses = set([wallet.address for wallet in eligible_addresses])
        wallet_by_address = {el.address: el for el in eligible_addresses}
        for _, contract in self.erc20_contracts.items():
            updates = []
            vis = set()
            matched_trxs = [trx for trx in transaction_details if trx["to"] == contract.address]
            for trx in matched_trxs:
                for event in contract.events.Transfer().process_receipt(trx):
                    dict_event = dict(event)
                    dict_event.update({
                        "args": dict(event.args), 
                        "transactionHash": str(event["transactionHash"]),
                        "blockHash": str(event["blockHash"]),
                    })

                    if dict_event["args"]["to"] in addresses and dict_event["args"]["to"] not in vis:
                        vis.add(dict_event["args"]["to"])
                        balance = contract.functions.balanceOf(dict_event["args"]["to"]).call()
                        wallet = wallet_by_address[dict_event["args"]["to"]]
                        data = wallet.data
                        balances = data.get(contract.address, [])
                        balances.append((block.number, balance))
                        data[contract.address] = balances
                        wallet.data = data
                        updates.append(wallet)
                        wallet_by_address[dict_event["args"]["to"]] = wallet

                    if dict_event["args"]["from"] in addresses and dict_event["args"]["from"] not in vis:
                        vis.add(dict_event["args"]["from"])
                        balance = contract.functions.balanceOf(dict_event["args"]["from"]).call()
                        wallet = wallet_by_address[dict_event["args"]["from"]]
                        data = wallet.data
                        balances = data.get(contract.address, [])
                        balances.append((block.number, balance))
                        data[contract.address] = balances
                        wallet.data = data
                        updates.append(wallet)
                        wallet_by_address[dict_event["args"]["from"]] = wallet

            Wallet.objects.bulk_update(updates, ["data"])
