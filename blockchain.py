import json
import os
from datetime import datetime, timezone
from eth_utils import keccak
from web3 import Web3

# Constants
BLOCKCHAIN_FILE = "blockchain.json"
INFURA_URL = "https://mainnet.infura.io/v3/e8740e4245d64df0bb6d7966a77255c3"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Predefined max word limits for each block (1 to 29), rounded to 50/100, strictly descending, last is 29
_MAX_WORDS_LIST = [
    2000, 1900, 1850, 1800, 1700, 1600, 1550, 1500, 1400, 1300,
    1250, 1200, 1100, 1000, 950, 900, 800, 700, 650, 600,
    500, 450, 400, 350, 300, 200, 150, 100, 29
]

def get_max_words(index):
    """
    Returns the maximum allowed words for a block at the given index (1-based).
    """
    if 1 <= index <= len(_MAX_WORDS_LIST):
        return _MAX_WORDS_LIST[index - 1]
    else:
        return _MAX_WORDS_LIST[-1]

def keccak_hash(data):
    """
    Computes the keccak-256 hash of a string or bytes and returns it as a hex string.
    """
    return keccak(data.encode() if isinstance(data, str) else data).hex()

def calculate_block_hash(block_data):
    """
    Calculates the hash of a block (excluding the hash field itself).
    """
    block_copy = dict(block_data)
    block_copy.pop("hash", None)
    data = json.dumps(block_copy, sort_keys=True, separators=(',', ':')).encode()
    return keccak(data).hex()

def load_blockchain():
    """
    Loads the blockchain from the local file system.
    """
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_blockchain(chain):
    """
    Saves the blockchain to the local file system.
    """
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def get_latest_eth_timestamp():
    """
    Fetches the latest Ethereum block timestamp and block number.
    """
    block = w3.eth.get_block('latest')
    block_time = datetime.fromtimestamp(block["timestamp"], timezone.utc).replace(tzinfo=None).isoformat()
    return block_time, block["number"]

def eth_signed_message(message):
    """
    Formats a message for Ethereum signature verification.
    """
    prefix = f"\x19Ethereum Signed Message:\n{len(message)}"
    return (prefix + message).encode()

