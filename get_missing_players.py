from pymongo import MongoClient
from conf import REST_ENDPOINT
import json
import requests
client = MongoClient()
db = client.cross_tables
player = db.player
game = db.game






games_cursor = game.find()
for i, game in enumerate(games_cursor):
	players = [game["player1_id"], game["player2_id"]]
	print i
	for player_id in players:
		print "Current player id"
		print player_id

		cursor = player.find({"playerid": player_id})
		if cursor.count() == 0:
			response = requests.get(REST_ENDPOINT + "player.php?player=" + player_id)
			print "here"
			player_details = json.loads(response.text)
			print player_details
			player_details = player_details['player']
			player_details["wins"] = player_details.pop("w")
			player_details["losses"] = player_details.pop("l")
			player_details["ties"] = player_details.pop("t")
			player.update(player_details, player_details, upsert=True)