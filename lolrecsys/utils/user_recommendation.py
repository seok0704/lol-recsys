import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','lolrecsys.settings')

import django
# Import settings
django.setup()

from django.conf import settings

import json
import requests
import numpy as np
from riotwatcher import LolWatcher, ApiError
import re

RIOT_API_KEY = settings.RIOT_API_KEY
watcher = LolWatcher(RIOT_API_KEY)


#########Readin json/npz files###########
current_path = os.path.dirname(os.path.abspath(__file__))

#Get Json file for mapping CHAMP ID from API with Champ Name 
API_CHAMP_LIST_FILE_DIR = os.path.join(current_path, 'data/api_champion_list_dict.json')

with open(API_CHAMP_LIST_FILE_DIR) as f:
  api_champion_list_dict = json.load(f)

#Get Json file for mapping with champ name with train matrix
CHAMP_LIST_FILE_DIR = os.path.join(current_path, 'data/champion_list_dict.json')

with open(CHAMP_LIST_FILE_DIR) as f:
  champion_list_dict = json.load(f)

CHAMP_ID_NAME_DIR = os.path.join(current_path, 'data/champ_id_to_names.json')

with open(CHAMP_ID_NAME_DIR) as f:
  champion_id_name_list = json.load(f)

#Get npz file for iisimilarity
IISIMILARITY_FILE_DIR = os.path.join(current_path, 'data/iisimilarity.npz')

iisimilarity = np.load(IISIMILARITY_FILE_DIR)['arr_0']




def get_summoner_info(region,username):
    summoner_info = watcher.summoner.by_name(region,username)

    return summoner_info

def get_ranked_info(region,summoner_info):
    ranked_stats=watcher.league.by_summoner(region,summoner_info['id'])
    
    return ranked_stats

def get_total_games(region,ranked_stats):
    total_games = 0

    for ranked_mode in ranked_stats:
        total_games += ranked_mode['wins'] + ranked_mode['losses']

    return total_games

def map_api_id_to_champ(champion_count):
    #Convert API ID to Similarity Index
    champion_count = dict((api_champion_list_dict[str(key)], value) for (key, value) in champion_count.items() if str(key) in api_champion_list_dict.keys()) 

    return champion_count


def champion_count_list(region, summoner_info, total_games):

    champion_count={}
    for idx in range(0,total_games,100):
        if idx+100 > total_games:
            #Get all ranked and flex 5v5 ranked matches that the player has played
            match_lists = watcher.match.matchlist_by_account(region, summoner_info['accountId'],queue=[420,440],begin_index=idx, end_index=total_games)
        else:
            match_lists = watcher.match.matchlist_by_account(region, summoner_info['accountId'],queue=[420,440],begin_index=idx, end_index=idx+100)

        for match in match_lists['matches']:
            champion_id = match['champion']
            champion_name = champion_id
            #champion_list[champion_list['Champion_ID']==champion_id].index[0]

            if champion_name in champion_count.keys():
                champion_count[champion_name] +=1/total_games
            else:
                champion_count[champion_name] =1/total_games
    champion_count = map_api_id_to_champ(champion_count)
    return champion_count

def create_userVector(champion_count):

    num_champs = len(champion_list_dict)

    matrix = np.zeros((num_champs))

    for champion,count in champion_count.items():
        champ_id = champion_list_dict[champion]
        matrix[champ_id] = count

    return matrix

def get_predictions(userVector, iisimilarity):
    temp_matrix = np.zeros(userVector.shape)
    temp_matrix[userVector.nonzero()] = 1
    normalizer = np.matmul(iisimilarity, temp_matrix)
    normalizer[normalizer == 0] = 1e-5
    
    predictionUser = np.matmul(iisimilarity, userVector)/normalizer
    
    return predictionUser

def get_top_n_recs(prediction, userVector):
    recs = []
    for i in range(len(prediction)):
        if float(userVector[i]) < 0.05: #Recommend if user played < 0.05%
            champ_name = list(champion_list_dict.keys())[list(champion_list_dict.values()).index(i)]
            recs.append((champ_name, prediction[i]))
            # recs.append((i, result[i])) #leave this to verify things actually working
    recs = sorted(recs, key=lambda tup: tup[1], reverse=True)

    return [rec[0] for rec in recs]

def get_user_recommendations(region, summoner_info, ranked_stats,topk=99):
    #Get total games played by the user in the current season
    total_games = get_total_games(region,ranked_stats)
    
    #Create list of games played per champion for the user
    champion_count = champion_count_list(region, summoner_info,total_games)
    
    #Create user vector
    user_vector = create_userVector(champion_count)
    
    #Make predictions using iisimilarity and user vector
    predictions = get_predictions(user_vector, iisimilarity)
    
    recommend_list = get_top_n_recs(predictions, user_vector)
    
    return recommend_list[:topk]


def get_solo_ranked(ranked_stats):
    if ranked_stats:
        for ranked_stat in ranked_stats:
            if ranked_stat['queueType']=='RANKED_SOLO_5x5':
                ranked_solo = ranked_stat
    else:
        ranked_solo = "Unranked"
    return ranked_solo


def get_version(region):
    version = watcher.data_dragon.versions_for_region(region)
    version = version['v']

    return version


def get_profile_icon(region, profile_icon_id):
    version = get_version(region)
    profile_icon_url = "http://ddragon.leagueoflegends.com/cdn/" + version + "/img/profileicon/" + str(profile_icon_id) + ".png"

    return profile_icon_url

def get_champ_icon(champ_name):
    champ_id = champion_id_name_list[champ_name]
        
    champ_url = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + champ_id + "_0.jpg"

    return champ_url

def get_champ_icon_url(champ_list):
    champ_icon_url = []
    for champ in champ_list:
        champ_icon_url.append(get_champ_icon(champ))
    return champ_icon_url

def get_tier(solo_ranked):
    if solo_ranked != 'Unranked':
        tier = solo_ranked['tier'].title()
    else:
        tier = 'Unranked'
    return tier

def chunker(champ_list):
    chunks_champ_list = []
    for idx in range(0,len(champ_list),3):
        chunks_champ_list.append(champ_list[idx:idx+3])

    return chunks_champ_list

