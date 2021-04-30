import requests
import sys,os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from django import forms
import json


CHAMP_LIST_FILE_DIR = os.path.join(BASE_DIR, 'utils/data/champion_list_dict.json')

with open(CHAMP_LIST_FILE_DIR) as f:
  champion_list_dict = json.load(f)

CHAMPION_CHOICES =[]
for key in champion_list_dict.keys():
    CHAMPION_CHOICES.append((key,key))

class itemForm(forms.Form):
    champion = forms.CharField(widget=forms.Select(choices=CHAMPION_CHOICES,attrs={'class':'search-field mr-sm-2 username','name':'champ_name'}),label='')