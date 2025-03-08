import csv
import os
import re
from datetime import datetime

# Get the absolute path to the data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Path to the src folder
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "claims.csv")

def submit_claim(policy_number, claim_amount, date_of_incident):
    if not validate_claim(policy_number, claim_amount, date_of_incident):
        return "Invalid claim details"
    
    claim_id = get_next_claim_id()
    claim = {
        "claim_id": claim_id,
        "policy_number": policy_number,
        "claim_amount": claim_amount,
        "date_of_incident": date_of_incident,
        "status": "Submitted",
        "payout_amount": 0.0,
        "rejection_reason": ""
    }
    save_claim(claim)
    return "Claim submitted successfully"

def validate_claim(policy_number, claim_amount, date_of_incident):
    # Validate policy number (example: must be alphanumeric and 10 characters long)
    if not re.match(r'^[A-Za-z0-9]{10}$', policy_number):
        return False
    
    # Validate claim amount (example: must be a positive number)
    if not isinstance(claim_amount, (int, float)) or claim_amount <= 0:
        return False
    
    # Validate date of incident (example: must be a valid date in the past)
    try:
        incident_date = datetime.strptime(date_of_incident, "%Y-%m-%d")
        if incident_date >= datetime.now():
            return False
    except ValueError:
        return False
    
    return True

def get_next_claim_id():
    if not os.path.exists(DATA_FILE):
        return 1
    with open(DATA_FILE, "r") as file:
        reader = csv.DictReader(file)
        claims = list(reader)
    return len(claims) + 1

def save_claim(claim):
    # Create the data directory if it doesn't exist
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # Check if the file exists
    file_exists = os.path.exists(DATA_FILE)
    
    # Append the claim to the file
    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=claim.keys())
        if not file_exists:
            writer.writeheader()  # Write header if the file is new
        writer.writerow(claim)  # Write the claim as a new row