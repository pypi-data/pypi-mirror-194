import hashlib
import hmac
import json
import requests


class Orchard:
    def __init__(self, secret_key, client_key, base_url):
        self.secret_key = secret_key
        self.client_key = client_key
        self.base_url = base_url

    def send_payment(self, payload):
        endpoint = "sendRequest"
        response = self.process_request(endpoint, payload)
        return response.json()

    def send_sms(self, payload):
        endpoint = "sendSms"
        response = self.process_request(endpoint, payload)
        return response.json()

    def check_wallet_balance(self, payload):
        endpoint = "check_wallet_balance"
        response = self.process_request(endpoint, payload)
        return response.json()

    def account_inquiry(self, payload):
        endpoint = "sendRequest"
        response = self.process_request(endpoint, payload)
        return response.json()

    def airtime_topup(self, payload):
        endpoint = "sendRequest"
        response = self.process_request(endpoint, payload)
        return response

    def hosted_checkout(self, payload):
        endpoint = "third_party_request"
        response = self.process_request(endpoint, payload)
        return response.json()

    def generate_signature(self, payload):
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            json.dumps(payload).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def process_request(self, endpoint, payload):
        response = requests.post(
            "{}/{}".format(self.base_url, endpoint),
            data=json.dumps(payload),
            verify=True,
            headers={
                "Authorization": "{}:{}".format(
                    self.client_key, self.generate_signature(payload)
                )
            },
        )
        return response
