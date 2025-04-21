import requests
import json
import time
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Xero and Slack credentials from environment variables
XERO_CLIENT_ID = os.getenv("CF15468A353C46588071B43CC1636C67")
XERO_CLIENT_SECRET = os.getenv("UK2LT80ZGozBy7ZHEf-oRP5hD6vgdPo6kQa-5QvOoIpjWEPf")
XERO_TENANT_ID = os.getenv("2820b5d5-fc3b-4f8c-9ecc-213482005224")
XERO_REFRESH_TOKEN = os.getenv("u9fFPDzhxr_vL4rCdO5BRcosP6I97B7zYwxVEnzbs9M")
SLACK_WEBHOOK_URL = os.getenv("https://hooks.slack.com/services/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")

print(f"Client ID: {XERO_CLIENT_ID}") 
print(f"Client Secret: {XERO_CLIENT_SECRET}") 
print(f"Tenant ID: {XERO_TENANT_ID}") 
print(f"Refresh Token: {XERO_REFRESH_TOKEN}") 
print(f"Slack Webhook URL: {SLACK_WEBHOOK_URL}")

# Temporary storage for pending invoices (in memory for simplicity)
pending_invoices = {}

def get_xero_access_token():
    # Function to refresh and get a new access token from Xero
    token_url = "https://identity.xero.com/connect/token"
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": XERO_REFRESH_TOKEN,
    }
    response = requests.post(token_url, data=token_data, auth=HTTPBasicAuth(XERO_CLIENT_ID, XERO_CLIENT_SECRET))
    if response.status_code == 200:
        tokens = response.json()
        return tokens['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.text}")

def fetch_invoices(access_token):
    # Function to fetch invoices from Xero
    invoice_url = f"https://api.xero.com/api.xro/2.0/Invoices"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Xero-tenant-id": XERO_TENANT_ID,
    }
    response = requests.get(invoice_url, headers=headers)
    if response.status_code == 200:
        return response.json()["Invoices"]
    else:
        raise Exception(f"Failed to fetch invoices: {response.text}")

def fetch_payments(access_token):
    # Function to fetch payments from Xero
    payment_url = f"https://api.xero.com/api.xro/2.0/Payments"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Xero-tenant-id": XERO_TENANT_ID,
    }
    response = requests.get(payment_url, headers=headers)
    if response.status_code == 200:
        return response.json()["Payments"]
    else:
        raise Exception(f"Failed to fetch payments: {response.text}")

def send_slack_notification(message):
    payload = {'text': message}
    response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise Exception(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

def main():
    while True:
        try:
            # Refresh access token
            access_token = get_xero_access_token()
            
            # Fetch and send notifications for new invoices
            invoices = fetch_invoices(access_token)
            for invoice in invoices:
                if invoice['Status'] == 'AUTHORISED':  # Check if the invoice is authorised
                    pending_invoices[invoice['InvoiceNumber']] = invoice
                    send_slack_notification(f"New Invoice Created: {invoice['InvoiceNumber']}")
            
            # Fetch payments and update pending invoices status
            payments = fetch_payments(access_token)
            for payment in payments:
                invoice_number = payment['Invoice']['InvoiceNumber']
                if invoice_number in pending_invoices:
                    send_slack_notification(f"Payment Received: {payment['PaymentID']} for Invoice: {invoice_number}")
                    del pending_invoices[invoice_number]
            
            # Sleep for a specified time before checking again
            time.sleep(300)  # Check every 5 minutes
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)  # Wait for a minute before retrying

if __name__ == "__main__":
    main()
