# ⛓️ TimeChain – Ethereum-Powered Message Blockchain

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
  Each block fetches real Mainnet timestamp + block number.

- **Dynamic Word Limit**  
  Enforces a decreasing word limit across 29 blocks (from 2000 → 29).

- **Lightweight & Local**  
  No database needed — all data is stored in `blockchain.json`.

---

## 📦 Installation

### Requirements

- Python 3.10+
- `pip`, `venv`

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/blockchain-explorer.git
cd blockchain-explorer

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # (or venv\Scripts\activate on Windows)

# Install dependencies
pip install -r requirements.txt

# Start the app
python app.py
🌐 Web Interface
Once running, visit: http://localhost:5000

Available Endpoints
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

Configured in blockchain.py, this mechanism prevents long messages from dominating the chain and enforces increasing compression and value per word.

📜 License
MIT License

👤 Author
Gurnoor Singh – https://github.com/gurnoorofficial
