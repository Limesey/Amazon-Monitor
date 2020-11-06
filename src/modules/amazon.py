from bs4 import BeautifulSoup

class amazon:
    def __init__(self, browser, store = None):
        self.store = store or ".co.uk"
        self.browser = browser

    def get_product(self, id):
        product_data = {
            "name": None,
            "url": None,
            "price": None,
            "thumbnail": None,
        }

        browser = self.browser
        url = self.product_link_from_id(id)

        if(not browser.current_url == url):
            browser.get(url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        soup = BeautifulSoup(soup.prettify(), "html.parser")

        product_data["name"] = soup.find("span", {"id": "productTitle"}).get_text().strip()
        product_data["url"] = url

        img = soup.find("img", {"class": "a-dynamic-image a-stretch-horizontal"})

        if(img):
            product_data["thumbnail"] = img["src"]

        # TO DO:
        # Get price

        return product_data

    def get_sellers(self, id):
        sellers = []
        browser = self.browser

        url = self.sellers_link_from_id(id)

        if(not browser.current_url == url):
            browser.get(url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        soup = BeautifulSoup(soup.prettify(), "html.parser")

        rows = soup.findAll("div", {"class": "a-row a-spacing-mini olpOffer"})

        for i in range(len(rows)):
            row = rows[i]

            seller = {
                "name": None,
                "price": None,
                "condition": None,
                "shipping" : None,
            }

            name_container = row.findChild("h3", {"class": "olpSellerName"})
            name = name_container.get_text().strip()

            if(name == ""):
                name = name_container.img["alt"]

            seller["name"] = name
            seller["price"] = row.findChild("span", {"class": "olpOfferPrice"}).get_text().strip().strip()
            seller["condition"] = row.findChild("span", {"class": "olpCondition"}).get_text().strip()

            shipping = row.findChild("p", {"class": "olpShippingInfo"}).findChild("span", {"class": "a-color-secondary"}).get_text().replace("\n", "").replace("  ", "")
            seller["shipping"] = shipping

            sellers.append(seller)

        return sellers

    def product_link_from_id(self, id = str):
        return f"https://amazon{self.store}/dp/{id}"

    def sellers_link_from_id(self, id = str):
        return f"https://amazon{self.store}/gp/offer-listing/{id}"
