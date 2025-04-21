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
XERO_REFRESH