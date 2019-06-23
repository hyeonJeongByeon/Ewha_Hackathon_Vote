from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Candidate, Poll, Choice
import datetime
from django.db.models import Sum
 
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
 
    #return HttpResponse("finish")
    return HttpResponseRedirect("/areas/{}/results".format(poll.area))
 
def results(request, area):
    candidates = Candidate.objects.filter(area = area)
    polls = Poll.objects.filter(area = area)
    poll_results = []
    
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
 
        ##==poll.id에 해당하는 투표수 출력==##
        total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes'))
        #초이스에서 투표에 해당하는 초이스를 가져와서 모두 더해준다
        result['total_votes'] = total_votes['votes__sum']
 
        rates=[] #지지율
        for candidate in candidates:
            try:
                choice = Choice.objects.get(poll_id = poll.id,
                    candidate_id = candidate.id)
                rates.append(round(choice.votes * 100 / result['total_votes'], 1))
            except:#투표를 하나도 못받았을 경우. choice=0일때
                rates.append(0)
        result['rates'] = rates #result안에 rates라는 키로 rates값을 넣음
        poll_results.append(result)
 
    context = {'candidates': candidates, 'area':area,
     'poll_results': poll_results}
    return render(request, 'elections/result.html', context)
