import json
import os
import pickle
from lib.abstract_data_types import Matrix


def open_json(path):
    try:
        with open(path, 'r') as json_file: return json.load(json_file)
    except FileNotFoundError as error:
        return None

def open_pickle(path):
    try:
        with open(path, 'rb') as f: return pickle.load(f)
    except FileNotFoundError as error:
        return None



def load_maps():
    if os.path.exists('assets/data/maps'):
        with os.scandir('assets/data/maps') as files:
            maps = [file for file in files if file.is_file() and file.name.endswith('.tiles.pickle')]
            if not maps: raise AssertionError('error loading mazes')
            
            mazes = dict()
            for maze in maps:
                name = maze.name.replace(".tiles.pickle", "").upper()
                tile_map = Matrix(open_pickle(maze.path))
                entities_map = open_pickle(maze.path.replace(".tiles.pickle", ".entities.pickle"))
                innocent_map = open_pickle(maze.path.replace(".tiles.pickle", ".innocents.pickle"))

                mazes[name] = (tile_map, entities_map, innocent_map)

            return mazes

    else: raise AssertionError('error loading mazes')


def load_dialogs(language="en"):
    ORIGINAL_PATH = 'assets/data/dialogs_en.json'
    new_path = ORIGINAL_PATH.replace('_en', f'_{language}')
    if os.path.exists(new_path): return open_json(new_path)
    else: return open_json(ORIGINAL_PATH)


INNOCENTS = open_json('assets/data/innocents.json')
DIALOGS = load_dialogs()
MAZES = load_maps()

