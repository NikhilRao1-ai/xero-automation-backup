import requests
import json

# Slack webhook URL
slack_webhook_url = 'https://hooks.slack.com/services/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'

# The message you want to send
message = {"text": "Hello, World!"}

# Send the message
response = requests.post(slack_webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})

# Check for success
if response.status_code == 200:
    print('Message sent successfully!')
else:
    print(f'Failed to send message: {response.text}')
