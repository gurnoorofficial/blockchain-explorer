# TimeChain – Ethereum-Powered Message Blockchain

**TimeChain** is a minimal blockchain system that lets anyone:

- 📝 Submit messages signed with Ethereum keys
- 🔐 Store them immutably and irreversibly on a custom chain
- ⏳ Anchor each block to a real Ethereum Mainnet block time
- 🧾 Enforce trustless, time-proof logging of statements
- 🚫 Prevent tampering, rewrites, or unauthorized inserts

Each message becomes part of a permanent public history — ideal for proof-of-existence, timestamping, declarations, or censorship-resistant records.

---

## ✅ Key Features

- **Ethereum Signature Verification**  
  Every message must be signed with a valid Ethereum private key.

- **Immutable Message Ledger**  
  Blocks cannot be altered once added — verified by Keccak-256 hashing.

- **Ethereum Time Anchoring**  
  Each block fetches a real Ethereum Mainnet timestamp and block number.

- **Dynamic Word Limit**  
  Enforces a decreasing word limit across 29 blocks (from 2000 → 29).

- **Lightweight & Local**  
  No database required — messages are stored in `blockchain.json`.

---

## 🔐 Cryptographic Authorship, Forgery Resistance & Immutable Chain

TimeChain is designed to ensure **message authenticity, immutability, and tamper-proof permanence**:

- **Proves Ownership of Message**  
  Each block requires a valid Ethereum signature. Only the **real owner of the private key** can submit a valid message — no impersonation possible.

- **Detects Duplicates & Tampering**  
  Every block includes a Keccak-256 hash of its data. If any block is altered or copied dishonestly, `verify_chain` will catch it instantly.

- **Trustless & Auditable**  
  There is no admin or manual approval. All verification is done by cryptography and chain logic. Anyone can audit it.

- **Dismisses Copy Attempts**  
  Because messages are signed and timestamps are real Ethereum block times, even if someone copies a message, they cannot claim ownership or replay it.

- **Time-Proof and Permanent**  
  Each block is anchored to a real Ethereum Mainnet timestamp. Once written, it is **forever bound to that moment** — immutable, undeletable, and cryptographically permanent.

---

## 📦 Installation

### Requirements

- Python 3.10+
- `pip`, `venv`

### Setup on windows # windows + R then enter cmd

# 1. Change to a non-system drive (optional but recommended)
cd /d D:\

# 2. Clone the repository
git clone https://github.com/gurnoorofficial/TimeChain.git
cd TimeChain

# 3. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 4. Install required dependencies
pip install -r requirements.txt

🛠️ Available Utilities
Once your virtual environment is active, you can run the following tools:

✍️ Sign Message (with timestamp)
Generates an Ethereum signature with the current UTC timestamp included.

**python sign_message.py**
You'll be prompted to:

Enter the message to sign
Enter the private key (starts with 0x)
The output includes:

Ethereum address
Full message (with timestamp)
Signature (0x prefixed)

🧾 Verify Signature Ownership
Checks if a signature belongs to the claimed Ethereum address.

**python check_ownership.py**
You'll be prompted to:

Enter the Ethereum address
Enter the message
Enter the signature

The script will confirm if the signature is valid for that address and message.

🔎 Verify Blockchain File Integrity
Validates the blockchain.json file by recalculating and comparing each block's hash using Keccak-256.

**python verify_local_hash.py**
You'll be prompted to:

Paste the full path to your blockchain.json file (quotes optional)
The script outputs:
Keccak hash for each block
Any inconsistencies or verification failures


# Start the app
python app.py
🌐 Web Interface
Once running, open: http://localhost:5000

Routes
Route	Method	Description
/	GET	Frontend message UI
/chain	GET	View full blockchain data
/add_block	POST	Submit signed message (JSON)
/verify_chain	GET	Validate all blocks + hashes

📁 Project Structure
bash
Copy
Edit
blockchain-explorer/
├── app.py                # Flask API logic
├── blockchain.py         # Core blockchain logic (hashing, limits, timestamp)
├── blockchain.json       # Stored block history
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Frontend UI
└── venv/                 # Virtual environment (excluded from Git)
🔒 Word Limit Per Block
The word limit is enforced using a strict, descending list:

Block 1: 2000 words

Block 2: 1900

…

Block 29: 29 words

This mechanism prevents long messages from dominating the chain and enforces increasing compression and value per word. Defined in blockchain.py.

📜 License
MIT License

git pull --rebase origin main
git push origin main

👤 Author
Gurnoor Singh – https://github.com/gurnoorofficial
