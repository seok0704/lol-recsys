import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

current_path = os.path.dirname(os.path.abspath(__file__))

import json
import requests
import numpy as np

IISIMILARITY_FILE_DIR = os.path.join(current_path, 'data/iisimilarity.npz')

iisimilarity = np.load(IISIMILARITY_FILE_DIR)['arr_0']

#Get Json file for mapping with champ name with train matrix
CHAMP_LIST_FILE_DIR = os.path.join(current_path, 'data/champion_list_dict.json')

with open(CHAMP_LIST_FILE_DIR) as f:
  champion_list_dict = json.load(f)


def get_item_recommendations(champion_name, k=100):
    # Pick top K based on predicted rating
    champion_id = champion_list_dict[champion_name]
    itemVector = iisimilarity[champion_id,:]
    topK = itemVector.argsort()[::-1][:k]
    
    topK_champ = list(map(lambda x:list(champion_list_dict.keys())[list(champion_list_dict.values()).index(x)],topK))

    return topK_champ
