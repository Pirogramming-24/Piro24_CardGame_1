from accounts.models import User
from .models import Game
from django.contrib import messages
import random as rd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
def main(request):
    return render(request, "games/main.html")

def select_five_cards():
    numbers = range(1,11)
    selected_numbers = rd.sample(numbers,5)
    selected_numbers.sort()
    return selected_numbers

def generateGame(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    pk = request.user.pk
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

        Attacker = request.user
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
        return redirect('games:gameList')
    
    return render(request,'games/startPage.html',context)


def gameList(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    pk = request.user.pk
    Games = Game.objects.filter(Q(Attacker=request.user)|Q(Defender=request.user)).order_by('id')
    for idx, game in enumerate(Games, start=1):
        game.display_order = idx
    context = {
        'Games':Games,
        'user_id':pk,
        'user_name':request.user.nickname,
        'user_score' : request.user.score
    }
    if request.method == "POST":
        game_id = request.POST.get('btn')
        print(game_id)
        game_DB = Game.objects.get(id=game_id)
        game_DB.delete()
        return redirect('games:gameList')
    return render(request,'games/gameList.html',context)

def ranking(request):
    top_users = User.objects.exclude(is_superuser=True).order_by('-score')[:3]
    users = User.objects.exclude(is_superuser=True).order_by('-score')
    context = {
        'users':users,
        'top_users':top_users
    }
    return render(request,'games/ranking.html',context)



# 1. 반격하기 기능
def counter_attack(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.user != game.Defender or game.isGameOngoing == False:
        return redirect('games:detail', pk=pk)
    
    display_order = request.GET.get("order", game.pk)

    if 'five_cards' not in request.session:
        request.session['five_cards'] = select_five_cards() 
    fiveCards = request.session['five_cards']
    
    if request.method == 'POST':
        with transaction.atomic():
            selected_card = int(request.POST.get('selected_card'))
            game.DefenderCard = selected_card
            
            attacker_card = game.AttackerCard
            defender_card = game.DefenderCard

            if attacker_card == defender_card:
                game.Winner = None
            
            else:
                if game.isBiggerScoreWin:
                    if attacker_card > defender_card:
                        game.Winner = game.Attacker
                    else:
                        game.Winner = game.Defender
                else:
                    if attacker_card > defender_card:
                        game.Winner = game.Defender
                    else:
                        game.Winner = game.Attacker
            
            if game.Winner:
                if game.Winner == game.Attacker:
                    winner_obj = game.Attacker
                    loser_obj = game.Defender
                    winner_score = attacker_card
                    loser_score = defender_card
                else:
                    winner_obj = game.Defender
                    loser_obj = game.Attacker
                    winner_score = defender_card
                    loser_score = attacker_card
                
                winner_obj.score += winner_score
                loser_obj.score -= loser_score

                winner_obj.save()
                loser_obj.save()

            game.isGameOngoing = False
            game.save()

            if 'five_cards' in request.session:
                    del request.session['five_cards']
        
        response = redirect('games:detail', pk=pk)
        response['Location'] += f'?order={display_order}'
        return response

    else:
        context = {
            'game': game,
            'fiveCards': fiveCards,
            'display_order': display_order,
        }
        return render(request, 'games/gameCounter.html', context)

def detail(request, pk):
    game = get_object_or_404(Game, pk=pk)

    display_order = request.GET.get("order", game.pk)
    common_context = {
        'game': game,
        'display_order': display_order, 
    }

    if request.method == "POST":
        if request.user == game.Attacker and game.isGameOngoing:
            game.delete()
            return redirect('games:gameList')
        
    # case1. 종료된 게임
    if not game.isGameOngoing :
        score_change = 0
        if game.Winner:
            if request.user == game.Attacker:
                my_card_value = game.AttackerCard
            else:
                my_card_value = game.DefenderCard
            
            if game.Winner == request.user:
                score_change = my_card_value
            else:
                score_change = -my_card_value
        
        common_context['score_change'] = score_change 
        common_context['state'] = 'result'
        
        return render(request, 'games/gameDetail.html', common_context)

    # 상황 2: 게임 진행 중 (Ongoing)
    else:
        if request.user == game.Attacker:
            common_context['state'] = 'waiting'
            return render(request, 'games/gameDetail.html', common_context)
        
        elif request.user == game.Defender:
            common_context['state'] = 'counter_ready'
            return render(request, 'games/gameDetail.html', common_context)

    # url로 들어오려는 시도 제거
    return redirect('games:gameList')
