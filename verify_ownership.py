from eth_account import Account
from eth_account.messages import encode_defunct

def verify():
    message = input("📨 Enter message: ").strip()
    signature = input("✍️ Enter signature (0x...): ").strip()
    expected_address = input("🔗 Enter expected Ethereum address: ").strip().lower()

    try:
        encoded_msg = encode_defunct(text=message)
        recovered = Account.recover_message(encoded_msg, signature=signature).lower()

        print("\n🔍 Verifying...")
        if recovered == expected_address:
            print("✅ Signature is valid. Matches the provided address.")
        else:
            print("❌ Signature is invalid or forged.")
            print(f"🔎 Recovered address: {recovered}")

    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    verify()
