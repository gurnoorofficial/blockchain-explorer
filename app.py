from flask import Flask, request, jsonify, render_template
from blockchain import (
    load_blockchain, save_blockchain, calculate_block_hash,
    get_latest_eth_timestamp, get_max_words
)
from eth_account.messages import encode_defunct
from eth_account import Account

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(load_blockchain())

@app.route("/add_block", methods=["POST"])
def add_block():
    data = request.get_json()
    if not data or "message" not in data or "signature" not in data:
        return jsonify({"error": "Missing fields"}), 400

    message = data["message"].strip()
    signature_hex = data["signature"].strip()

    if signature_hex.startswith("0x"):
        signature_hex = signature_hex[2:]

    try:
        encoded_msg = encode_defunct(text=message)
        recovered_address = Account.recover_message(encoded_msg, signature=bytes.fromhex(signature_hex)).lower()
    except Exception as e:
        return jsonify({"error": "Invalid signature or message mismatch", "details": str(e)}), 400

    chain = load_blockchain()
    if len(chain) >= 29:
        return jsonify({"error": "Chain limit reached"}), 403

    index = len(chain) + 1
    max_words = get_max_words(index)
    if len(message.split()) > max_words:
        return jsonify({"error": f"Message exceeds word limit ({max_words})"}), 400

    try:
        timestamp, eth_block_number = get_latest_eth_timestamp()
    except Exception as e:
        return jsonify({"error": "Ethereum timestamp failed", "details": str(e)}), 500

    previous_hash = chain[-1]["hash"] if chain else "0" * 64

    block_data = {
        "index": index,
        "message": message,
        "eth_address": recovered_address,
        "signature": signature_hex,
        "timestamp": timestamp,
        "eth_block_number": eth_block_number,
        "previous_hash": previous_hash,
    }

    block_data["hash"] = calculate_block_hash(block_data)
    chain.append(block_data)
    save_blockchain(chain)

    return jsonify(block_data)

@app.route("/verify_chain", methods=["GET"])
def verify_chain():
    chain = load_blockchain()
    if not chain:
        return jsonify({"error": "Blockchain is empty or missing"}), 400

    errors = 0
    messages = []

    for i, block in enumerate(chain):
        expected_index = i + 1

        if block["index"] != expected_index:
            messages.append(f"❌ Block {expected_index}: Incorrect index.")
            errors += 1

        if i > 0 and block["previous_hash"] != chain[i-1]["hash"]:
            messages.append(f"❌ Block {expected_index}: Previous hash mismatch.")
            errors += 1

        computed_hash = calculate_block_hash(block)
        if block["hash"] != computed_hash:
            messages.append(f"❌ Block {expected_index}: Hash mismatch.")
            errors += 1

    if errors == 0:
        messages.append("✅ All blocks are valid and consistent.")

    return jsonify({"errors": errors, "messages": messages})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
