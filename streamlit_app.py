import streamlit as st
from web3 import Web3
import json

# --- SECTION 1: BLOCKCHAIN CONNECTION ---
# Replace with your actual Infura/Alchemy URL
INFURA_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_ID" 
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# --- SECTION 2: SMART CONTRACT DETAILS ---
# Replace with your deployed Contract Address and ABI
CONTRACT_ADDRESS = "0xYourContractAddressHere"
CONTRACT_ABI = json.loads('[YOUR_CONTRACT_ABI_JSON_HERE]')

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# --- SECTION 3: USER AUTHENTICATION (Optional) ---
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Admin Login")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
        return False
    return True

# --- SECTION 4: MAIN APP INTERFACE ---
if check_login():
    st.set_page_config(page_title="AI Carbon Tracker", layout="wide")
    
    st.title("🌱 AI-Based Carbon Credit Tracking System")
    st.write("Securely record environmental offsets on the Ethereum Blockchain.")

    # Sidebar for logout
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Layout: Two Columns
    col1, col2 = st.columns(2)

    with col1:
        st.header("📝 Register New Credit")
        company_name = st.text_input("Company Name", placeholder="e.g., Tata Motors")
        amount = st.number_input("Carbon Amount (Tons)", min_value=1)

        # --- SUBMIT BUTTON WITH HASH DISPLAY LOGIC ---
        if st.button("Register on Blockchain"):
            if company_name and amount > 0:
                try:
                    with st.spinner("Processing transaction on Sepolia..."):
                        # Sending the transaction
                        # Note: Ensure your private key is handled securely in a real app
                        tx_hash = contract.functions.addCredit(company_name, int(amount)).transact()
                        
                        # Wait for confirmation
                        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                        
                        # Success UI
                        st.success("Data successfully mined into the Block!")
                        st.balloons()
                        
                        # Display Hash ID directly on frontend
                        hash_id = tx_hash.hex()
                        st.subheader("🔗 Blockchain Receipt")
                        st.info("Transaction Hash:")
                        st.code(hash_id) # Adds a copy button automatically
                        
                        # Link to Etherscan
                        etherscan_url = f"https://sepolia.etherscan.io/tx/{hash_id}"
                        st.link_button("Verify on Etherscan", etherscan_url)
                
                except Exception as e:
                    st.error(f"Blockchain Error: {e}")
            else:
                st.warning("Please fill in all details before submitting.")

    with col2:
        st.header("📜 Carbon Credit Logs")
        if st.button("Refresh History"):
            try:
                # Fetching data from the Smart Contract
                history = contract.functions.getHistory().call()
                if history:
                    # Displaying as a professional table
                    import pandas as pd
                    df = pd.DataFrame(history, columns=["Company Name", "Tons", "Timestamp"])
                    st.table(df)
                else:
                    st.info("No records found on the blockchain.")
            except Exception as e:
                st.error(f"Failed to fetch history: {e}")

# --- FOOTER ---
st.divider()
st.caption("Developed by Ayushri Dhunde | B.Tech CSE (AI) | GHRCE Nagpur")
