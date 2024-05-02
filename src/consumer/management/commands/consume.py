import warnings
warnings.simplefilter("ignore")

from django.core.management.base import BaseCommand, CommandError
from rollet.settings import BASE_DIR
from provider.eth import EthProvider
import pathlib
import json


class Command(BaseCommand):
    help = "consume blocks"

    def add_arguments(self, parser):
        parser.add_argument("--config", type=str)

    def handle(self, *args, **options):
        config_path = pathlib.Path(BASE_DIR).joinpath(options["config"])
        config = json.load(open(config_path, "r"))

        provider = EthProvider(config["etherum_endpoints"])
        lastest_block_number = provider.get_block_number()
        block = provider.get_block(lastest_block_number)

        transactions = block["transactions"]

        contracts = []
        for erc20 in config["erc20_contracts"]:
            abi = json.load(open(pathlib.Path(BASE_DIR).joinpath(erc20["abi_path"]), "r"))
            contracts.append(provider.get_contract(erc20["address"], abi))

        print(contracts)

        pass
