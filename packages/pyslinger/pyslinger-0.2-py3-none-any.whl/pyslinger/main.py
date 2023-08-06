import requests
import json
import os

def sling(msg, webhook=None):
    webhook = os.environ.get('PINGER_WEBHOOK') if not webhook else webhook
    data = {}
    data["text"] = "\n".join(str(k) + ": " + str(v) for k, v in msg.items())
    requests.post(webhook, data=json.dumps(data))

if __name__ == "__main__":
    sling({'text': 'test message'})