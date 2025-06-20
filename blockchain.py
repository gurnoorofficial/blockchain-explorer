
import json
import os
from datetime import datetime, timezone
from eth_utils import keccak
from web3 import Web3

BLOCKCHAIN_FILE = "blockchain.json"
INFURA_URL = "https://mainnet.infura.io/v3/e8740e4245d64df0bb6d7966a77255c3"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def get_max_words(index):
    if index <= 19:
        return 2000 // (2 ** ((index - 1) // 5))
    elif index <= 23:
        return 300
    elif index <= 26:
        return 250
    elif index <= 28:
        return 150
    else:
        return 29

def keccak_hash(data):
    return keccak(data.encode() if isinstance(data, str) else data).hex()

def calculate_block_hash(block_data):
    block_copy = dict(block_data)
    block_copy.pop("hash", None)
    data = json.dumps(block_copy, sort_keys=True, separators=(',', ':')).encode()
    return keccak(data).hex()

def load_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_blockchain(chain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def get_latest_eth_timestamp():
    block = w3.eth.get_block('latest')
    block_time = datetime.fromtimestamp(block["timestamp"], timezone.utc).replace(tzinfo=None).isoformat()
    return block_time, block["number"]

def eth_signed_message(message):
    prefix = f"\x19Ethereum Signed Message:\n{len(message)}"
    return (prefix + message).encode()
