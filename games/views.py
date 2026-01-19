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
def counter_attack(request, pk) :
    game = get_object_or_404(Game, pk=pk)

    # 예외 : 방어자가 아니거나 이미 종료된 게임이면 list페이지로 redirect
    if request.user != game.Defender or game.isGameOngoing == False:
        return redirect('games:detail', pk=pk)
    
    # 랜덤 숫자 5개 얻기
    if 'five_cards' not in request.session:
        request.session['five_cards'] = select_five_cards() 
    fiveCards = request.session['five_cards']
    
    # 2. 게임 결과 판정 로직
    if request.method == 'POST':
        # DB연산 중 꼬인경우 롤백
        with transaction.atomic():
            # 선택한 숫자 저장
            selected_card = int(request.POST.get('selected_card'))
            game.DefenderCard = selected_card
            
            # 게임 결과 결정
            attacker_card = game.AttackerCard
            defender_card = game.DefenderCard

            # case 1 - 무승부인 경우
            if attacker_card == defender_card :
                game.Winner = None
            
            # case 2 - 숫자가 서로 다른 경우
            else :
                if game.isBiggerScoreWin: # 큰 숫자가 이기는 룰인 경우
                    if attacker_card > defender_card:
                        game.Winner = game.Attacker
                    else:
                        game.Winner = game.Defender
                else: # 작은 숫자가 이기는 룰인 경우
                    if attacker_card > defender_card:
                        game.Winner = game.Defender
                    else:
                        game.Winner = game.Attacker
            
            # 3. 점수 계산 및 저장 로직
            if game.Winner : # 무승부인 경우는 제외
                if game.Winner == game.Attacker:
                    winner_obj = game.Attacker # 승자 지정
                    loser_obj = game.Defender # 패자 지정
                    winner_score = attacker_card # 승자의 카드 숫자
                    loser_score = defender_card  # 패자의 카드 숫자
                else:
                    winner_obj = game.Defender
                    loser_obj = game.Attacker
                    winner_score = defender_card
                    loser_score = attacker_card
                
                # 승자, 패자 점수 반영
                winner_obj.score += winner_score
                loser_obj.score -= loser_score

                # 승자, 패자 정보 저장
                winner_obj.save()
                loser_obj.save()

            # 게임 진행 상태를 종료로 변경 및 저장
            game.isGameOngoing = False
            game.save()

            if 'five_cards' in request.session:
                    del request.session['five_cards']
        return redirect('games:detail', pk=pk)
    else :
        display_order = request.GET.get("order", game.pk)

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
