from django.shortcuts import render
from django.http import HttpResponse
 
from .models import Candidate, Poll, Choice
import datetime
 
# Create your views here.
def index(request):
    candidates = Candidate.objects.all()
    context = {'candidates':candidates}
        #context에 모든 어린이 정보를 저장
    return render(request, 'elections/index.html', context)
        #context안에 있는 어린이 정보를 index.html로 전달
 
def areas(request, area):
    today = datetime.datetime.now()
    try :
        poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte=today) # get에 인자로 조건을 전달해줍니다. 
        candidates = Candidate.objects.filter(area = area) # Candidate의 area와 매개변수 area가 같은 객체만 불러오기
    except:
        poll = None
        candidates = None
    context = {'candidates': candidates,
    'area' : area,
    'poll' : poll }
    return render(request, 'elections/area.html', context)
 
def polls(request, poll_id):
    poll = Poll.objects.get(pk = poll_id)#Poll객체를 구분하는 녀석은 poll_id이므로 PK지정
    selection = request.POST['choice']
 
    try:
        #choice모델을 불러와서 1을 증가시킨다 
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()
 
    return HttpResponse("finish")
