import requests
import json

PROXIES = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}


class BurpCollaboratorClient():

    BURP_DOMAIN = "polling.burpcollaborator.net"

    def __init__(self, colabo_key, colabo_subdomain):
        self.colabo_key = colabo_key
        self.colabo_subdomain = colabo_subdomain

    def poll(self):
        params = {"biid": self.colabo_key}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

        response = requests.get(
            "https://" + self.BURP_DOMAIN + "/burpresults", params=params, headers=headers, proxies=PROXIES, verify=False)

        if response.status_code != 200:
            raise Error("Failed to poll Burp Collaborator")

        result_parsed = json.loads(response.text)
        return result_parsed.get("responses", [])
