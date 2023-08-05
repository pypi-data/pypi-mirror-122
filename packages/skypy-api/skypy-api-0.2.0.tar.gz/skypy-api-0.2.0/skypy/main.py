import requests
import json
import os, sys

class skypy:
  """ The skypy class for the module. Uses a api key that you can find by running /api on mc.hypixel.net """
  def __init__(self, key):
    global apikey
    apikey = str(key)
    try:
      r = requests.get("https://api.hypixel.net/key?key="+ key)
    except:
      sys.exit(0)
    returns = json.loads(r.text)
    if not returns["success"]:
      print("Invalid API Key! Please note that you cant use some modules now!")

  class bazaar:
    """ The bazaar class was made to get bazaar values from certain items. """
    def __init__(self):
      pass

    def fetchAllProducts(self):
      """ Fetches all products and returns them as a JSON string. """
      r = requests.get("https://api.hypixel.net/skyblock/bazaar")
      return json.loads(r.text)

    def fetchProduct(self, itemname):
      """ Fetches a specific product and returns his data as a JSON string. """
      r = requests.get("https://api.hypixel.net/skyblock/bazaar")
      bazaarProducts = json.loads(r.text)
      bazaarProducts = bazaarProducts["products"]
      try:
        return bazaarProducts[itemname]
      except:
        return False
  class auction:
    """ The auction class is there to get auction informations. It requires the Hypixel api key (log into mc.hypixel.net and type /api in chat)."""
    def __init__(self):
      pass

    def getAuctionByPlayer(self, uuid):
      """ Gets the auction by a player uuid. """
      # payload = {'key': apikey, 'player': uuid}
      r = requests.get("https://api.hypixel.net/skyblock/auction?key=" + apikey + "&player=" + uuid)
      returns = json.loads(r.text)
      if not returns["success"]:
        print("Failed! Make sure, that you api key and the uuid is correct!")
      else:
        return returns["auctions"]

    def getAuctionByPlayerName(self, player):
      """ Uses the Mojang API to get the uuid of a player. """
      r = requests.get("https://api.mojang.com/users/profiles/minecraft/" + player)
      returns = json.loads(r.text)
      try:
        playeruuid = returns["id"]
        return self.getAuctionByPlayer(playeruuid)
      except:
        print("Invalid Playername!")

    def getAuction(self, auctionid):
      """ Gets an auction by its ID. """
      r = requests.get("https://api.hypixel.net/skyblock/auction?key=" + apikey + "&uuid=" + auctionid)
      returns = json.loads(r.text)
      if not returns["success"]:
        print("Failed! Make sure, that you api key and the auction-id is correct!")
      else:
        return returns["auctions"]