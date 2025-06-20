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
    try:
        return jsonify(load_blockchain())
    except Exception as e:
        return jsonify({"error": f"Failed to load blockchain: {str(e)}"}), 500

@app.route("/add_block", methods=["POST"])
def add_block():
    data = request.get_json()
    if not data or "message" not in data or "signature" not in data:
        return jsonify({"error": "Missing message or signature"}), 400

    message = data["message"].strip()
    signature_hex = data["signature"].strip()

    if signature_hex.startswith("0x"):
        signature_hex = signature_hex[2:]

    try:
        encoded_msg = encode_defunct(text=message)
        recovered_address = Account.recover_message(encoded_msg, signature=bytes.fromhex(signature_hex)).lower()
    except Exception as e:
        return jsonify({"error": "Invalid signature", "details": str(e)}), 400

    try:
        chain = load_blockchain()
    except Exception as e:
        return jsonify({"error": f"Failed to load blockchain: {str(e)}"}), 500

    if len(chain) >= 29:
        return jsonify({"error": "Chain has reached its limit (29 blocks)"}), 403

    index = len(chain) + 1
    max_words = get_max_words(index)
    if len(message.split()) > max_words:
        return jsonify({"error": f"Message exceeds word limit ({max_words})"}), 400

    try:
        timestamp, eth_block_number = get_latest_eth_timestamp()
    except Exception as e:
        return jsonify({"error": "Ethereum timestamp fetch failed", "details": str(e)}), 500

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

    try:
        save_blockchain(chain)
    except Exception as e:
        return jsonify({"error": f"Failed to save block: {str(e)}"}), 500

    return jsonify(block_data)

@app.route("/verify_chain", methods=["GET"])
def verify_chain():
    try:
        chain = load_blockchain()
    except Exception as e:
        return jsonify({"error": f"Failed to load blockchain: {str(e)}"}), 500

    if not chain:
        return jsonify({"error": "Blockchain is empty"}), 400

    errors = 0
    messages = []

    for i, block in enumerate(chain):
        index = i + 1

        if block["index"] != index:
            messages.append(f"❌ Block {index}: Incorrect index")
            errors += 1

        if i > 0 and block["previous_hash"] != chain[i - 1]["hash"]:
            messages.append(f"❌ Block {index}: Previous hash mismatch")
            errors += 1

        if calculate_block_hash(block) != block["hash"]:
            messages.append(f"❌ Block {index}: Hash mismatch")
            errors += 1

    if errors == 0:
        messages.append("✅ All blocks are valid and consistent.")

    return jsonify({"errors": errors, "messages": messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
