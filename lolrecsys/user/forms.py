from django import forms

REGION_CHOICES = [
    ('na1','NA'),
    ('euw1','EUW'),
    ('eun1','EUN1'),
    ('JP1','JP'),
    ('KR','KR'),
]

class userForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Summoner','name':'username','class':'search-field mr-sm-2 username'}),label ='')
    region = forms.CharField(widget=forms.Select(choices=REGION_CHOICES,attrs={'class':'search-field mr-sm-2 region','name':'region'}),label='')