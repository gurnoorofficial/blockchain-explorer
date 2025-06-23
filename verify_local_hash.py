import json
from eth_utils import keccak
import os

def keccak_hash(data):
    """Returns the keccak256 hash (Ethereum-style) as a hex string."""
    if isinstance(data, str):
        data = data.encode()
    return keccak(data).hex()

def calculate_block_hash(block_data):
    """Calculates the hash of a block, excluding the 'hash' field."""
    block_copy = dict(block_data)
    block_copy.pop("hash", None)
    raw = json.dumps(block_copy, sort_keys=True, separators=(',', ':')).encode()
    return keccak(raw).hex()

def main():
    path = input("📄 Enter path to blockchain JSON file: ").strip().strip('"').strip("'")

    if not os.path.isfile(path):
        print(f"❌ File not found: {path}")
        return

    try:
        with open(path, 'r') as f:
            chain = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read JSON: {e}")
        return

    if not isinstance(chain, list):
        print("❌ Expected a list of blocks in the JSON.")
        return

    print("\n🔎 Calculating Keccak-256 hashes for each block...\n")
    for block in chain:
        if "index" not in block:
            print("⚠️  Skipping block (missing 'index')")
            continue
        index = block["index"]
        hash_value = calculate_block_hash(block)
        print(f"Block {index}: {hash_value}")

if __name__ == "__main__":
    main()
