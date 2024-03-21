import requests

url = "https://api.exchange.coinbase.com/products/"

class CryptoPriceService:

    def getPrice(self, pair):
        endpoint = url + pair.replace("/", "-") + "/book" # TODO: make this volume easy to be changed
        r = requests.get(url = endpoint)
        return r.json()
    


if __name__ == '__main__':
    price = CryptoPriceService().getPrice("btc/usd")
    print(price)
    print(price['bids'][0][0])
    print(price['asks'][0][0])