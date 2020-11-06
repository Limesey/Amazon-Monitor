import threading
import time
from random import choice

from selenium import webdriver
from modules.amazon import amazon
from modules.cache import get_cache
from modules.cache import save_cache

def create_browser(headless : bool, proxy = None):
    options = webdriver.FirefoxOptions()

    if(proxy):
        webdriver.DesiredCapabilities.FIREFOX["proxy"] = {
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy,
            "proxyType": "MANUAL",
        }

    if(headless):
        options.add_argument("--headless")

    print("Monitor starting using proxy: {}".format(proxy))

    return webdriver.Firefox(None, options=options)

class monitor:
    def __init__(self, headless : bool, interval : float, product : str, proxies = None):
        proxy = None

        if(proxies):
            proxy = choice(proxies)

        self.browser = create_browser(headless, proxy)
        self.update_interval = interval or 60
        self.product_id = product
        self._events = {
            "seller_added": [],
            "seller_removed": [],
            "update": [self.__on_update],
        }
        self.__closed = False

        try:
            t = threading.Thread(target=self.update)
            print("Monitor successfully started.")
            #t.daemon = True
            t.start()
            while True: time.sleep(100)
        except (KeyboardInterrupt, SystemExit):
            print("Received keyboard interrupt, quitting threads!")
            self.__closed = True

    def update(self):
        amzon = amazon(self.browser)

        while(self.product_id is not None):
            if(self.__closed):
                self.browser.close()
                break

            print("Running")
            product_id = self.product_id
            thumbnail = None
            url = None
            name = None
            product_data = None
            cache = get_cache(product_id)

            if(cache):
                thumbnail = cache["thumbnail"]
                url = cache["url"]
                name = cache["product_name"]
            
            if(not name):
                product_data = amzon.get_product(product_id)

            data = {
                "product_id": product_id,
                "product_name": name or product_data["name"],
                "url": url or amzon.product_link_from_id(product_id),
                "price": None,
                "thumbnail": thumbnail or product_data["thumbnail"],

                "sellers": []
            }

            data["sellers"] = amzon.get_sellers(product_id)
            self.trigger("update", data)

            time.sleep(self.update_interval)

    # Self note: __ makes a function private
    def __on_update(self, data, removeLater = None):
        product_id = data["product_id"]
        cache_data = get_cache(data["product_id"])

        if(not cache_data):
            save_cache(product_id, data)
        else:
            for seller in data["sellers"]:
                if(not seller in cache_data["sellers"]):
                    self.trigger("seller_added", seller, data)
            
            for seller in cache_data["sellers"]:
                if(not seller in data["sellers"]):
                    self.trigger("seller_removed", seller, data)

        save_cache(product_id, data)

    # Event programming
    def on(self, event_name : str, callback : any):
        if(event_name in self._events):
            self._events[event_name].append(callback)
    
    # TO DO:
    # Improve argument passing
    def trigger(self, event_name : str, args = None, product = None):
        if(event_name in self._events):
            event = self._events[event_name]

            for callback in event:
                callback(args, product)