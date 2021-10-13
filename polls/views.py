
#from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Question


# Create your views here.
# 클라이언트로부터 request를 받게 되면 여러가지 정보가 담겨 있을 것이다. 이를 다시 저장/추출/다운로드 등의 response를 해주는 것.
def index(request):
    # return HttpResponse("백엔드 걸음마중...")

    # Question 데이터를 pub_date 순으로 정렬해 5개까지만 데이터를 가지고 올 것이며, 이 데이터들을 ','로 연결하고 이를 response 한다.
    # 하지만, 아래 코드에는 페이지 디자인이 하드코딩되었다는 문제가 있다. 
    '''
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
    '''
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html') # 템플릿을 로드해서 리스폰스한다.
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
   #return HttpResponse(template.render(context, request))

    


def detail(request, question_id):
    #return HttpResponse("You're looking at question %s.", question_id)
    # response or 404를 주기 위해 try/except를 사용했다.
    # 하지만 Django에서는 더 쉬운 방법인 get_object_or_404()를 제공한다.
    '''
    try:
       question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(requests, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s" % question_id)