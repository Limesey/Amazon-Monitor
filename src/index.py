print("Initializing monitors . . .")

from modules.util import get_setting
from modules.monitor import *
from modules.discord import webhook
from modules.discord.embeds import RichEmbed

from modules.amazon import *

print("Loading configuration . . .")

hook_url = get_setting("webhookUrl")
headless = get_setting("headless")
interval = get_setting("updateInterval")
seller_notifiers = get_setting("sellerNotifiers")
mentions_config = get_setting("notifications")
proxies = get_setting("proxies")

print("Initializing Webhook . . .")
hook = webhook.webhook(hook_url)

def notify(product_data, on_sale, seller_name):
    mention = None
    title = None

    url = product_data["url"]
    name = product_data["product_name"]

    description = f"[{name}]({url})"

    if(on_sale):
        title = f"**BACK IN STOCK - {seller_name}**"
    else:
        title = f"**OUT OF STOCK - {seller_name}**"

    if(mentions_config["enabled"]):
        mention = mentions_config["mentions"]

    message = hook.new_message(mention)
    embed = RichEmbed(title, description)
    embed.add_field("Price", product_data["price"])
    embed.thumbnail["url"] = product_data["thumbnail"]
    embed.set_colour(16750848)

    hook.add_embed(message, embed)
    hook.send(message)

def is_in_list(seller, product_id):
    result = False
    product = None

    for item in seller_notifiers:
        if(item["id"] == product_id):
            product = item
            break

    for item in product["sellers"]:
        if(item == seller):
            result = True
            break

    return result

def on_seller_added(seller, product_data = None):
    seller_name = seller["name"]
    product_id = product_data["product_id"]

    is_wanted_seller = is_in_list(seller_name, product_id)

    #print(f"Added seller '{seller_name}'. Is wanted seller: {is_wanted_seller}")

    if(is_wanted_seller):
        product_data["price"] = seller["price"]
        notify(product_data, True, seller_name)

def on_seller_removed(seller, product_data = None):
    seller_name = seller["name"]
    product_id = product_data["product_id"]

    is_wanted_seller = is_in_list(seller_name, product_id)

    #print(f"Removed seller '{seller_name}'. Is wanted seller: {is_wanted_seller}")

    if(is_wanted_seller):
        product_data["price"] = seller["price"]
        notify(product_data, False, seller_name)

for product in seller_notifiers:
    m = monitor(headless, interval, product["id"], proxies)
    m.on("seller_added", on_seller_added)
    m.on("seller_removed", on_seller_removed)