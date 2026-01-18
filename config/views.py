from django.shortcuts import render

def ranking(request):
    leaderboard = [
        {"rank":1,"nickname":"user1","score":5200},
        {"rank":2,"nickname":"user2","score":4800},
        {"rank":3,"nickname":"user3","score":3900},
        {"rank":4,"nickname":"user4","score":3700},
        {"rank":5,"nickname":"user5","score":2800},
    ]
    return render(request, "ranking.html", {"leaderboard": leaderboard})
