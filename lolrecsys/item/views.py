from django.shortcuts import render

import requests
import sys,os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.shortcuts import render
from user import forms

from utils.item_recommendation import get_item_recommendations
from utils.user_recommendation import get_champ_icon_url,chunker

from user.forms import userForm
from item.forms import itemForm

# Create your views here.
def item_rec(request):

    userform = userForm()
    itemform = itemForm()

    champion_name = request.POST.get('champion', "")
    
    print(champion_name)
    top_champion_list = get_item_recommendations(champion_name)
    top_champion_list_icon_list = get_champ_icon_url(top_champion_list)

    user_choice_champ = top_champion_list[0]
    user_choice_champ_icon = top_champion_list_icon_list[0]

    champ_list = list(zip(range(0,len(top_champion_list)+1),top_champion_list, top_champion_list_icon_list))

    champ_list.pop(0)

    champ_list_chunks = chunker(champ_list)

    context = {
        'champ_list_chunks':champ_list_chunks,
        'user_choice_champ':user_choice_champ,
        'user_choice_champ_icon':user_choice_champ_icon,
        'userform': userform,
        'itemform': itemform,
    }

    return render(request,'item/items_rec.html', context)

