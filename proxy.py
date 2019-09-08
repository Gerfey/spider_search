import requests
import random
import json


class Proxy:

    def __init__(self):
        self.base_url = 'http://pubproxy.com/api/proxy?https=true&country=RU'

    def generate(self):
        response = requests.get(self.base_url)

        try:
            json_proxy = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            with open('files/proxy.json', "r") as file:
                read_data = file.read()
                file.close()
            json_proxy = json.loads(read_data)

        proxy_data = json_proxy['data'][random.randint(0, len(json_proxy['data']) - 1)]

        return {"https": f"{proxy_data['ipPort']}"}
