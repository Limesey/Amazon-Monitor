from datetime import datetime

class RichEmbed:

    def __init__(self, title = None, description = None):
        self.title = title
        self.description = description
        self.color = 0
        self.timestamp = None
        self.footer = {
            "icon_url": None,
            "text": None
        }
        self.thumbnail = {
            "url": None
        }
        self.image = {
            "url": None
        }

        self.author = {
            "name": None,
            "url": None,
            "icon_url": None
        }

        self.fields = []

    def set_colour(self, colour = None):
        self.color = colour or 0

    def add_field(self, name: str, value: str, inline = None):
        field = {
            "name": name,
            "value": value,
            "inline": inline
        }

        self.fields.append(field)

    def set_footer(self, text: str, url: str):
        self["text"] = text
        self.footer["icon_url"] = url

    def set_timestamp(self):
        self.timestamp = datetime.utcnow()