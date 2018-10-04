import os
BASE_URL = 'http://www.cross-tables.com/'
GCG_FOLDER_PATH = 'gcg_files'
REST_ENDPOINT = BASE_URL + "rest/"
if not os.path.exists(GCG_FOLDER_PATH):
	os.mkdir(GCG_FOLDER_PATH)


def extract_player_table(player_table):
	rows = player_table.findChildren('tr')
	name_address = get_div_text(rows[0], 'playername')
	name, address = name_address.split("|")
	second_row_cells = rows[1].findChildren('td')
	ratings = get_div_text(second_row_cells[0], 'stat')
	ratings_list = ratings.split("/")
	if len(ratings_list) > 1:
		twl_rating, csw_rating = int(ratings_list[0]), int(ratings_list[1])
	else:
		twl_rating = int(ratings)
		csw_rating = 0
	div_ranking_twl = get_div_text(second_row_cells[1], 'stat')
	div_ranking_csw = get_div_text(second_row_cells[1], 'stat cswrating')
	ranking_twl = 0
	ranking_csw = 0
	if div_ranking_twl is not None:
		ranking_twl = int(div_ranking_twl[:-2])
	if div_ranking_csw is not None:
		ranking_csw = int(div_ranking_csw[:-2])
	lifetime_record = get_div_text(second_row_cells[2], 'stat')
	print lifetime_record
	lifetime_record_list = re.split('-| ', lifetime_record)
	lifetime_record_list[3] = float(lifetime_record_list[3][1:-1])
	lifetime_record_list[:3] = [int(stat) for stat in lifetime_record_list[:3]]
	print lifetime_record_list
	print name.strip(), address.strip(), twl_rating, csw_rating, ranking_twl, ranking_csw