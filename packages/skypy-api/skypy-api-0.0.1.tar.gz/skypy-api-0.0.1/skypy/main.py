import requests
import json

class skypy:

  def __init__(self):
    pass



  class bazaar:
    def __init__(self):
      pass

    def fetchAllProducts(self):
      r = requests.get("https://api.hypixel.net/skyblock/bazaar")
      return json.loads(r.text)

    def fetchProduct(self, itemname):
      r = requests.get("https://api.hypixel.net/skyblock/bazaar")
      bazaarProducts = json.loads(r.text)
      bazaarProducts = bazaarProducts["products"]
      try:
        return bazaarProducts[itemname]
      except:
        return False