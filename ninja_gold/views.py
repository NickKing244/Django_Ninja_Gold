from django.shortcuts import render, redirect
from datetime import datetime
from pytz import timezone
import random, pytz

def index(request):
    if 'gold' not in request.session or 'activities' not in request.session:
        request.session['gold'] = 0
        request.session['activities'] = []
    context = {
        "activities": request.session['activities']
    }
    return render(request, 'index.html', context)

def process_money(request):
    if request.method == 'POST':
        my_gold = request.session['gold']
        location = request.POST['location']
        activities = request.session['activities']
        if location == 'farm':
            gold_this_turn = random.randint(10, 20)
            my_gold += gold_this_turn
            request.session['gold'] = my_gold
        elif location == 'cave':
            gold_this_turn = random.randint(5, 10)
            my_gold += gold_this_turn
            request.session['gold'] = my_gold
        elif location == 'house':
            gold_this_turn = random.randint(2, 5)
            my_gold += gold_this_turn
            request.session['gold'] = my_gold
        elif location == 'casino':
            gold_this_turn = random.randint(-50, 50)
            my_gold += gold_this_turn
            request.session['gold'] = my_gold

        date_format='%m/%d/%Y %H:%M:%S %Z'
        date = datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Eastern'))
        myTime = date.strftime(date_format)

        if gold_this_turn >= 0:
            str = f"Earned {gold_this_turn} gold from the {location} {myTime}"
        else:
            str = f"Entered a Casino and Lost {gold_this_turn} gold {myTime}"

        activities.insert(0, str)
        request.session['activities'] = activities
    return redirect("/")

def reset(request):
    request.session['gold'] = 0
    del request.session['activities']
    return redirect("/")