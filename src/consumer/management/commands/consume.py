import warnings
warnings.simplefilter("ignore")

from django.core.management.base import BaseCommand, CommandError
from rollet.settings import BASE_DIR

from extractor.eligible_wallets import EligibleWalletsExtractor
from extractor.erc20 import ERC20BalanceExtractor

from provider.eth import EthProvider
import pathlib
import json
from concurrent.futures import ThreadPoolExecutor


class Command(BaseCommand):
    help = "consume blocks"

    def add_arguments(self, parser):
        parser.add_argument("--config", type=str)

    def handle(self, *args, **options):
        config_path = pathlib.Path(BASE_DIR).joinpath(options["config"])
        config = json.load(open(config_path, "r"))

        provider = EthProvider(config["etherum_endpoints"])

        erc20_contracts = {}
        for erc20 in config["erc20_contracts"]:
            abi = json.load(open(pathlib.Path(BASE_DIR).joinpath(erc20["abi_path"]), "r"))
            erc20_contracts[erc20["address"]] = provider.get_contract(erc20["address"], abi)

        # lastest_block_number = provider.get_block_number()
        lastest_block_number = 19781194
        block = provider.get_block(lastest_block_number)

        transactions = block["transactions"]
        with ThreadPoolExecutor(max_workers=10) as executor:
            transaction_details = list(executor.map(provider.get_transaction_receipt, transactions))

        ex = EligibleWalletsExtractor(provider, erc20_contracts)

        data = {}
        ex.extract(block, transaction_details, data)

        ex = ERC20BalanceExtractor(provider, erc20_contracts)
        ex.extract(block, transaction_details, data)


        pass
