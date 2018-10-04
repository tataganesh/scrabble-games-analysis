from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import pickle
import re
import os
from pprint import pprint
from conf import BASE_URL, GCG_FOLDER_PATH, REST_ENDPOINT
import json
import traceback
from IPython import embed
LAST_OFFSET = 25302
DIFFERENCE = 100


def get_div_text(parent_object, class_name):
	div_object = parent_object.find('div', {'class': class_name})
	if div_object is None:
		return None
	return div_object.text


def get_players_details(players_links):
	details = list()
	for player_link in players_links:
		player_url_suffix = player_link.get("href")
		player_id = player_url_suffix.split("=", 1)[-1]
		response = requests.get(REST_ENDPOINT + "player.php?player=" + player_id)
		player_details = json.loads(response.text)
		player_details = player_details['player']
		player_details["wins"] = player_details.pop("w")
		player_details["losses"] = player_details.pop("l")
		player_details["ties"] = player_details.pop("t")
		details.append(player_details)
	return details


def get_game_details(game_link):
	game_details = dict()
	game_url_suffix = game_link.get("href")
	game_details["annotation_id"] = game_url_suffix.split("=", 1)[-1]
	annotated_game_url = BASE_URL + game_url_suffix
	response = requests.get(annotated_game_url)
	game_details_html = response.text
	soup = BeautifulSoup(game_details_html, "html.parser")
	game_details["gcg_file_path"] = os.path.join(GCG_FOLDER_PATH, str(game_details["annotation_id"]) + '.gcg')
	if not os.path.exists(game_details["gcg_file_path"]):
		print "Saving gcg file"
		gcg_file_tag = soup.select_one("a[href*=annotated/selfgcg]")
		gcg_file_link = BASE_URL + gcg_file_tag.get("href")
		response = requests.get(gcg_file_link)
		with open(game_details["gcg_file_path"], 'w+') as f:
			f.write(response.text)
	else:
		print "GCG file already present"
	return game_details


with open("current_offset", 'rb') as fp:
	current_offset = pickle.load(fp)

if not os.path.exists(GCG_FOLDER_PATH):
	os.mkdir(GCG_FOLDER_PATH)


client = MongoClient()
db = client.cross_tables
player = db.player
game = db.game
index_collection = db.index
offset = index_collection.find_one()
starting_offset = offset['offset']
row_index = offset["row_index"]

pagination_pages = range(starting_offset, LAST_OFFSET, DIFFERENCE)
for current_offset in pagination_pages:
	offset["offset"] = current_offset
	index_collection.save(offset)
	print "Current offset - ", current_offset
	response = requests.get('http://www.cross-tables.com/annolistself.php?offset=' + str(current_offset))
	html = response.text
	soup = BeautifulSoup(html, "html.parser")
	table = soup.find('table', id="xtdatatable")
	rows = table.findChildren('tr')
	for index, row in enumerate(rows[row_index:], row_index):
		offset["row_index"] = index
		index_collection.save(offset)
		if row.get('id') == "headerrow":
			continue
		print "Current Row - ", index
		all_row_links = row.findAll('a')
		try:
			game_details = get_game_details(all_row_links[0])
			player1_details, player2_details = get_players_details(all_row_links[1:])
		except:
			print traceback.format_exc()
			continue
		game_details["player1_id"] = player1_details[u'playerid']
		game_details["player2_id"] = player2_details[u'playerid']
		player.update(player1_details, player1_details, upsert=True)
		player.update(player2_details, player2_details, upsert=True)
		game.update(game_details, game_details, upsert=True)
	print "\n##############################################\n"

