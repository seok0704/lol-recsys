from django.shortcuts import render
import sys, os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user.forms import userForm

from item.forms import itemForm

#The index page
def index(request):
    userform = userForm()
    itemform = itemForm()
    return render(request, 'index.html',{'userform':userform,'itemform':itemform})
