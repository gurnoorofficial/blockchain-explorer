# 🧱 Blockchain Explorer (TimeChain)

A lightweight, Ethereum-aware blockchain app that:

- Allows message signing using Ethereum keys
- Verifies signatures on-chain using Flask backend
- Enforces dynamic word limits per block (29 → 29 max)
- Stores blocks with Ethereum timestamp & signature
- Built with Python, Flask, Web3.py, and eth-account

---

## 🚀 Features

- Ethereum signature verification
- 29-block cap with strict word limits per block
- Block hashing using Keccak-256
- Timestamping with real Ethereum Mainnet data
- JSON storage (`blockchain.json`)

---

## 🛠️ Installation

### 🔧 Requirements

- Python 3.10+ recommended
- `pip`, `venv`

### 📦 Setup Instructions

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
Once running, open http://localhost:5000 in your browser.

Routes
URL	Method	Description
/	GET	Home page (frontend)
/chain	GET	View the full blockchain
/add_block	POST	Add a new block (JSON format)
/verify_chain	GET	Validate chain integrity

📁 Project Structure
bash
Copy
Edit
blockchain-explorer/
├── app.py                # Flask app
├── blockchain.py         # Core blockchain logic
├── blockchain.json       # Blockchain data
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Frontend UI
└── venv/                 # Virtual environment (ignored by .git)
🔒 Word Limit Logic
The word limit per block decreases across 29 blocks, starting at 2000 and ending at 29. Controlled in blockchain.py.

📝 License
MIT License
