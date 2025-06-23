import json
import os
from datetime import datetime, timezone
from eth_utils import keccak
from web3 import Web3

# === Constants ===
BLOCKCHAIN_FILE = "/root/TimeChain/blockchain.json"
FINGERPRINT_FILE = "/root/TimeChain/chain_fingerprint.txt"
INFURA_URL = "https://mainnet.infura.io/v3/e8740e4245d64df0bb6d7966a77255c3"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# === Max word limits per block index ===
_MAX_WORDS_LIST = [
    2000, 1900, 1850, 1800, 1700, 1600, 1550, 1500, 1400, 1300,
    1250, 1200, 1100, 1000, 950, 900, 800, 700, 650, 600,
    500, 450, 400, 350, 300, 200, 150, 100, 29
]

def get_max_words(index):
    return _MAX_WORDS_LIST[index - 1] if 1 <= index <= len(_MAX_WORDS_LIST) else _MAX_WORDS_LIST[-1]

def keccak_hash(data):
    return keccak(data.encode() if isinstance(data, str) else data).hex()

def calculate_block_hash(block_data):
    block_copy = dict(block_data)
    block_copy.pop("hash", None)
    data = json.dumps(block_copy, sort_keys=True, separators=(',', ':')).encode()
    return keccak(data).hex()

def is_chain_valid(chain):
    for i in range(1, len(chain)):
        prev = chain[i - 1]
        curr = chain[i]
        if curr["previous_hash"] != calculate_block_hash(prev):
            print(f"❌ Tampering: block {i} has invalid previous hash")
            return False
        if curr["hash"] != calculate_block_hash(curr):
            print(f"❌ Tampering: block {i} has invalid current hash")
            return False
    return True

def load_blockchain():
    if not os.path.exists(BLOCKCHAIN_FILE):
        if os.path.exists(FINGERPRINT_FILE):
            raise Exception("❌ blockchain.json is missing — possible tampering or accidental deletion.")
        print("🆕 Starting new blockchain (empty).")
        return []

    with open(BLOCKCHAIN_FILE, "r") as f:
        chain = json.load(f)

    if not is_chain_valid(chain):
        raise Exception("❌ Blockchain integrity check failed!")

    if os.path.exists(FINGERPRINT_FILE):
        with open(FINGERPRINT_FILE, "r") as f:
            expected_hash = f.read().strip()
            if chain[-1]["hash"] != expected_hash:
                raise Exception("❌ Chain fingerprint mismatch — possible rollback.")

    return chain

def save_chain_fingerprint(chain):
    with open(FINGERPRINT_FILE, "w") as f:
        f.write(chain[-1]["hash"])

def save_blockchain(chain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)
    save_chain_fingerprint(chain)

def add_block(message, signature):
    chain = load_blockchain()
    index = len(chain)
    if len(message.split()) > get_max_words(index + 1):
        raise ValueError("❌ Message exceeds max word limit for this block")

    timestamp, eth_block = get_latest_eth_timestamp()
    previous_hash = calculate_block_hash(chain[-1]) if chain else "0"

    new_block = {
        "index": index,
        "message": message,
        "timestamp": timestamp,
        "eth_block": eth_block,
        "signature": signature,
        "previous_hash": previous_hash
    }
    new_block["hash"] = calculate_block_hash(new_block)

    chain.append(new_block)
    save_blockchain(chain)
    return new_block

def get_latest_eth_timestamp():
    block = w3.eth.get_block('latest')
    block_time = datetime.fromtimestamp(block["timestamp"], timezone.utc).replace(tzinfo=None).isoformat()
    return block_time, block["number"]

def eth_signed_message(message):
    prefix = f"\x19Ethereum Signed Message:\n{len(message)}"
    return (prefix + message).encode()
