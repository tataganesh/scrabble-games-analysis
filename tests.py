import gcg_parser
import os
GCG_FILES_PATH = 'gcg_files'
example_files = ['10001.gcg', '10004.gcg', '10009.gcg', '10239.gcg']

file_texts = dict()
for file_name in example_files:
	file_path = os.path.join(GCG_FILES_PATH, file_name)
	file_texts[file_name] = open(file_path, 'r').read().splitlines()


def test_playername_extraction():
	file_player_mapping = {'10001.gcg': 'Noah Walton', '10004.gcg': 'jack', '10009.gcg': 'Zev Kaufman', '10239.gcg':'Jeremy Hildebrand'}
	for file_name, file_lines in file_texts.iteritems():
		line = file_lines[0]
		actual_player_name = file_player_mapping[file_name]
		extracted_player_name = gcg_parser.get_player_name(line)
		assert extracted_player_name == actual_player_name