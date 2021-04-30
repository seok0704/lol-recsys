from django.shortcuts import render
from user.forms import userForm
from item.forms import itemForm

from utils.user_recommendation import (get_user_recommendations, 
                                get_summoner_info, get_ranked_info,get_profile_icon,
                                get_solo_ranked,get_champ_icon_url,get_tier, chunker )

def user_rec(request):

    userform = userForm()
    itemform = itemForm()

    username = request.POST.get("username","")
    region = request.POST.get("region","")

    summoner_info = get_summoner_info(region, username)
    ranked_info = get_ranked_info(region, summoner_info)
    solo_ranked = get_solo_ranked(ranked_info)

    champ_name_list = get_user_recommendations(region, summoner_info, ranked_info)
    champ_icon_list = get_champ_icon_url(champ_name_list)

    champ_list = list(zip(range(1,len(champ_name_list)+1),champ_name_list, champ_icon_list))

    champ_list_chunks = chunker(champ_list)

    tier = get_tier(solo_ranked)

    summoner_level = summoner_info['summonerLevel']
    username = summoner_info['name']
    profile_icon = get_profile_icon(region, summoner_info['profileIconId'])

    context = {
        'champ_list_chunks':champ_list_chunks,
        'username':username,
        'profile_icon':profile_icon,
        'summoner_level':summoner_level,
        'tier':tier,
        'userform':userform,
        'itemform':itemform,
    }

    return render(request,'user/users_rec.html', context)