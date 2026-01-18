from accounts.models import User
from django.shortcuts import render
from .models import Game
from django.contrib import messages
from django.shortcuts import redirect
import random as rd

# Create your views here.

def select_five_cards():
    numbers = range(1,11)
    selected_numbers = rd.sample(numbers,5)
    selected_numbers.sort()
    return selected_numbers

def generateGame(request,pk):
    if 'five_cards' not in request.session:
        print('new')
        request.session['five_cards'] = select_five_cards()
    fiveCards = request.session['five_cards']
    Defenders = User.objects.exclude(is_superuser=True).exclude(id=pk)

    context = {
        'fiveCards' : fiveCards,
        'Defenders' : Defenders
    }

    if request.method == "POST" and request.POST.get('submit') == 'submit':
        print('press button')
        defender_id = request.POST.get('defender_radio')

        if defender_id == None:
            messages.error(request,"반격자를 선택해주세요")
            print("반격자를 선택해주세요")
            return redirect(request.path)
        AttackerCard = request.POST.get('card_radio')
        if AttackerCard == None:
            messages.error(request,"카드를 선택해주세요")
            print("카드를 선택해주세요")
            return redirect(request.path)

        Attacker = User.objects.get(id=pk)
        Defender = User.objects.get(id=defender_id)
        isBiggerScoreWin = rd.choice([True,False])
        isGameOngoing = True
        Game.objects.create(
            Attacker = Attacker,
            AttackerCard = AttackerCard,
            Defender = Defender,
            isBiggerScoreWin = isBiggerScoreWin,
            isGameOngoing = isGameOngoing
        )
        del request.session['five_cards']
        print('delete')
    
    return render(request,'games/startPage.html',context)