import requests
import json

class webhook:
    def __init__(self, url=str):
        self.url = url

    def new_message(self, message = None):
        data = {
            "content": message,
            "embeds": []
        }

        return data

    def add_embed(self, message, embed):
        message["embeds"].append(embed)

    def send(self, data):
        embeds = []

        for embed in data["embeds"]:
            embeds.append(embed.__dict__)

            timestamp = embed.timestamp

            if(timestamp is not None):
                embed.timestamp = timestamp.__str__()

        data["embeds"] = embeds


        return requests.post(self.url, data=json.dumps(data), headers={"Content-Type": "application/json"})